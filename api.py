from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import asyncio
from smart_router import SmartRouter
from architect import Architect
from coder import Coder
from healer import Healer
from deployer import Deployer
from docs_generator import DocsGenerator

from supabase import create_client, Client
from monitor import Monitor
from db_manager import DatabaseManager
from migration_engine import MigrationEngine

# 1. Initialize Supabase Platform Database (https://agi-app-builder.netlify.app/)
PLATFORM_URL = os.getenv("SUPABASE_URL")
PLATFORM_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(PLATFORM_URL, PLATFORM_KEY)

app = FastAPI(title="Singularity AGI API")
monitor = Monitor()

@app.get("/projects")
async def get_all_projects():
    """
    Fetch all projects from the platform database.
    """
    response = supabase.table("projects").select("*").order("created_at", desc=True).execute()
    return response.data

@app.websocket("/ws/build")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Receive build request
    data = await websocket.receive_text()
    request_data = json.loads(data)
    prompt = request_data.get("prompt")
    deploy_target = request_data.get("deploy", "netlify")
    heal_flag = request_data.get("heal", True)
    docs_flag = request_data.get("docs", True)
    
    # 2. Register Project in Platform Database
    project_entry = supabase.table("projects").insert({
        "name": "Initializing...",
        "prompt": prompt,
        "status": "building",
        "deploy_platform": deploy_target
    }).execute()
    project_id = project_entry.data[0]["id"]

    async def log_to_db(msg, type="info"):
        await websocket.send_text(msg)
        supabase.table("build_logs").insert({
            "project_id": project_id,
            "message": msg,
            "type": type
        }).execute()

    # 1. Setup Keys
    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    GROQ_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    
    if not all([OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY]):
        await log_to_db("[!] Missing AI API Keys. Build halted.", "error")
        await websocket.close()
        return

    try:
        # 3. Initialize Modules
        router = SmartRouter(OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY)
        architect = Architect(router)
        coder = Coder(router)
        healer = Healer(router)
        docs_gen = DocsGenerator(router)
        
        # Deployer with all possible tokens
        deployer = Deployer(
            os.getenv("GITHUB_TOKEN"), 
            os.getenv("NETLIFY_TOKEN"),
            os.getenv("RAILWAY_TOKEN"),
            os.getenv("FLY_TOKEN")
        )

        # 4. Phase 1: Planning
        await log_to_db(f"[*] Planning your app ({deploy_target}): '{prompt}'...")
        blueprint = architect.plan_project(prompt)
        
        if "error" in blueprint:
            await log_to_db(f"[!] Planning failed: {blueprint['error']}", "error")
            supabase.table("projects").update({"status": "failed"}).eq("id", project_id).execute()
            await websocket.close()
            return
        
        project_name = blueprint.get('project_name', 'singularity-app')
        await log_to_db(f"[+] Project blueprint generated: {project_name}")
        supabase.table("projects").update({"name": project_name, "blueprint": blueprint}).eq("id", project_id).execute()

        # 5. Phase 2: Building
        project_path = os.path.join(os.getcwd(), "output", project_name)
        # Initialize Migration Engine for this project
        migrator = MigrationEngine(project_path)
        
        await log_to_db(f"[*] Starting multi-agent build for: {project_name}")
        coder.build_project(blueprint, base_dir=project_path)
        await log_to_db(f"[+] Multi-agent build complete.")

        # 6. Phase 3: Database Orchestration
        await log_to_db("[*] Starting database orchestration (Supabase/Neon)...")
        sql_schema = blueprint.get("database_schema", "")
        if sql_schema:
            migrator.generate_migration(sql_schema)
            # Example: Apply to a dev branch if Neon is configured
            dev_conn = db_manager.setup_neon_branch(project_name, branch_name="dev")
            if dev_conn:
                db_manager.execute_sql(dev_conn, sql_schema)
                await log_to_db("[+] Dev database branch created and schema applied.")
            else:
                await log_to_db("[!] Database connection not found. Schema saved to migrations/ folder.", "warning")

        # 7. Phase 4: Healing
        if heal_flag:
            await log_to_db("[*] Entering self-healing phase...")
            success = healer.heal_project(project_path, blueprint)
            if success:
                await log_to_db("[+] Project healed and verified.")
            else:
                await log_to_db("[!] Healing phase failed. Deploying anyway...", "warning")

        # 8. Phase 5: Autonomous Docs
        if docs_flag:
            await log_to_db("[*] Generating autonomous documentation...")
            docs_gen.generate_docs(project_path, blueprint)
            await log_to_db("[+] README.md and documentation generated.")

        # 9. Phase 6: Deployment
        await log_to_db(f"[*] Deploying to {deploy_target}...")
        
        deploy_url = ""
        if deploy_target == "railway":
            deployer.deploy_to_railway(project_path, project_name)
            deploy_url = f"https://{project_name}.up.railway.app"
        elif deploy_target == "fly":
            deployer.deploy_to_fly(project_path, project_name)
            deploy_url = f"https://{project_name}.fly.dev"
        else: # Default: netlify
            deployer.deploy_to_netlify(project_path, project_name)
            deploy_url = f"https://{project_name}.netlify.app"

        # Update Project Status to Live
        supabase.table("projects").update({
            "status": "live",
            "deploy_url": deploy_url
        }).eq("id", project_id).execute()

        await log_to_db(f"[SUCCESS] App '{project_name}' is live at {deploy_url}", "success")
        await websocket.close()
        
    except Exception as e:
        await log_to_db(f"[ERROR] {str(e)}", "error")
        supabase.table("projects").update({"status": "failed"}).eq("id", project_id).execute()
        await websocket.close()

            return
        
        await websocket.send_text(f"[+] Project blueprint generated: {blueprint.get('project_name')}")

        # 4. Phase 2: Building
        project_name = blueprint.get('project_name', 'singularity-app')
        project_path = os.path.join(os.getcwd(), "output", project_name)
        
        # Initialize Migration Engine for this project
        migrator = MigrationEngine(project_path)
        
        await websocket.send_text(f"[*] Starting multi-agent build for: {project_name}")
        coder.build_project(blueprint, base_dir=project_path)
        await websocket.send_text(f"[+] Multi-agent build complete.")

        # 5. Phase 3: Database Orchestration (New)
        await websocket.send_text("[*] Starting database orchestration (Supabase/Neon)...")
        sql_schema = blueprint.get("database_schema", "")
        if sql_schema:
            migrator.generate_migration(sql_schema)
            # Example: Apply to a dev branch if Neon is configured
            dev_conn = db_manager.setup_neon_branch(project_name, branch_name="dev")
            if dev_conn:
                db_manager.execute_sql(dev_conn, sql_schema)
                await websocket.send_text("[+] Dev database branch created and schema applied.")
            else:
                await websocket.send_text("[!] Database connection not found. Schema saved to migrations/ folder.")

        # 6. Phase 4: Healing
        if heal_flag:
            await websocket.send_text("[*] Entering self-healing phase...")
            success = healer.heal_project(project_path, blueprint)
            if success:
                await websocket.send_text("[+] Project healed and verified.")
            else:
                await websocket.send_text("[!] Healing phase failed. Deploying anyway...")

        # 7. Phase 5: Autonomous Docs
        if docs_flag:
            await websocket.send_text("[*] Generating autonomous documentation...")
            docs_gen.generate_docs(project_path, blueprint)
            await websocket.send_text("[+] README.md and documentation generated.")

        # 8. Phase 6: Deployment
        await websocket.send_text(f"[*] Deploying to {deploy_target}...")
        
        if deploy_target == "railway":
            deployer.deploy_to_railway(project_path, project_name)
            monitor.add_app(project_name, f"https://{project_name}.up.railway.app")
        elif deploy_target == "fly":
            deployer.deploy_to_fly(project_path, project_name)
            monitor.add_app(project_name, f"https://{project_name}.fly.dev")
        else: # Default: netlify
            deployer.deploy_to_netlify(project_path, project_name)
            monitor.add_app(project_name, f"https://{project_name}.netlify.app")

        await websocket.send_text(f"[SUCCESS] App '{project_name}' is live!")
        await websocket.close()
        
    except Exception as e:
        await websocket.send_text(f"[ERROR] {str(e)}")
        await websocket.close()

        return

    try:
        # 2. Initialize Modules
        router = SmartRouter(OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY)
        architect = Architect(router)
        coder = Coder(router)
        healer = Healer(router)
        docs_gen = DocsGenerator(router)
        
        # Deployer with all possible tokens
        deployer = Deployer(
            os.getenv("GITHUB_TOKEN"), 
            os.getenv("NETLIFY_TOKEN"),
            os.getenv("RAILWAY_TOKEN"),
            os.getenv("FLY_TOKEN")
        )

        # 3. Phase 1: Planning
        await websocket.send_text(f"[*] Planning your app ({deploy_target}): '{prompt}'...")
        blueprint = architect.plan_project(prompt)
        
        if "error" in blueprint:
            await websocket.send_text(f"[!] Planning failed: {blueprint['error']}")
            await websocket.close()
            return
        
        await websocket.send_text(f"[+] Project blueprint generated: {blueprint.get('project_name')}")

        # 4. Phase 2: Building
        project_name = blueprint.get('project_name', 'singularity-app')
        project_path = os.path.join(os.getcwd(), "output", project_name)
        
        await websocket.send_text(f"[*] Starting multi-agent build for: {project_name}")
        coder.build_project(blueprint, base_dir=project_path)
        await websocket.send_text(f"[+] Multi-agent build complete.")

        # 5. Phase 3: Healing
        if heal_flag:
            await websocket.send_text("[*] Entering self-healing phase...")
            success = healer.heal_project(project_path, blueprint)
            if success:
                await websocket.send_text("[+] Project healed and verified.")
            else:
                await websocket.send_text("[!] Healing phase failed. Deploying anyway...")

        # 6. Phase 4: Autonomous Docs
        if docs_flag:
            await websocket.send_text("[*] Generating autonomous documentation...")
            docs_gen.generate_docs(project_path, blueprint)
            await websocket.send_text("[+] README.md and documentation generated.")

        # 7. Phase 5: Deployment
        await websocket.send_text(f"[*] Deploying to {deploy_target}...")
        
        if deploy_target == "railway":
            deployer.deploy_to_railway(project_path, project_name)
            monitor.add_app(project_name, f"https://{project_name}.up.railway.app")
        elif deploy_target == "fly":
            deployer.deploy_to_fly(project_path, project_name)
            monitor.add_app(project_name, f"https://{project_name}.fly.dev")
        else: # Default: netlify
            deployer.deploy_to_netlify(project_path, project_name)
            monitor.add_app(project_name, f"https://{project_name}.netlify.app")

        await websocket.send_text(f"[SUCCESS] App '{project_name}' is live!")
        await websocket.close()
        
    except Exception as e:
        await websocket.send_text(f"[ERROR] {str(e)}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
