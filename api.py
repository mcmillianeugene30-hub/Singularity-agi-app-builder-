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
from refiner import Refiner
from linter import Linter
from reasoning_engine import ReasoningEngine
from multimodal import MultiModalAgent
from rollback import RollbackManager
from plugin_manager import PluginManager
from supabase import create_client, Client
from monitor import Monitor
from db_manager import DatabaseManager
from migration_engine import MigrationEngine

# 1. Initialize Supabase Platform Database (https://agi-app-builder.netlify.app/)
PLATFORM_URL = os.getenv("SUPABASE_URL")
PLATFORM_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(PLATFORM_URL, PLATFORM_KEY)

# 1. Initialize Advanced AI Modules
reasoning_engine = ReasoningEngine(SmartRouter(os.getenv("OPENROUTER_API_KEY"), os.getenv("GROQ_API_KEY"), os.getenv("GEMINI_API_KEY")))
multimodal_agent = MultiModalAgent(SmartRouter(os.getenv("OPENROUTER_API_KEY"), os.getenv("GROQ_API_KEY"), os.getenv("GEMINI_API_KEY")))

app = FastAPI(title="Singularity AGI API")
monitor = Monitor()
db_manager = DatabaseManager(
    os.getenv("NEON_API_KEY"),
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BuildRequest(BaseModel):
    prompt: str
    deploy: str = "netlify"
    heal: bool = True
    docs: bool = True
    refine: bool = True
    lint: bool = True

class RateRequest(BaseModel):
    project_id: str
    rating: int
    feedback: str = ""

@app.post("/rate")
async def rate_project(request: RateRequest):
    """
    Feedback Integration: Users rate generated apps.
    """
    try:
        supabase.table("projects").update({
            "rating": request.rating,
            "feedback": request.feedback
        }).eq("id", request.project_id).execute()
        return {"status": "success", "message": "Feedback recorded."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects")
async def get_all_projects():
    """Fetch all projects from the platform database."""
    response = supabase.table("projects").select("*").order("created_at", desc=True).execute()
    return response.data

@app.get("/monitor")
async def get_monitor_status():
    """Return the live status of all monitored apps."""
    return monitor.get_dashboard_summary()

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
    refine_flag = request_data.get("refine", True)
    lint_flag = request_data.get("lint", True)
    reason_flag = request_data.get("reason", True) # Advanced: Reasoning Engine
    multimodal_flag = request_data.get("multimodal", True) # Advanced: Multi-Modal
    
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
        architect = Architect(router, supabase_client=supabase)
        coder = Coder(router)
        healer = Healer(router)
        docs_gen = DocsGenerator(router)
        refiner = Refiner(router)
        linter = Linter(router)
        
        deployer = Deployer(
            os.getenv("GITHUB_TOKEN"), 
            os.getenv("NETLIFY_TOKEN"),
            os.getenv("RAILWAY_TOKEN"),
            os.getenv("VERCEL_TOKEN")
        )

        # 4. Phase 1: Planning
        await log_to_db(f"[*] Planning your app ({deploy_target})...")
        blueprint = architect.plan_project(prompt, deploy_target=deploy_target)
        
        # 5. Advanced: Code Reasoning & Suggestions (New)
        if reason_flag:
            await log_to_db("[*] Generating architectural reasoning and suggestions...")
            explanation = reasoning_engine.explain_blueprint(prompt, blueprint)
            suggestions = reasoning_engine.suggest_features(prompt, blueprint)
            await websocket.send_text(json.dumps({"type": "reasoning", "explanation": explanation, "suggestions": suggestions}))
            await log_to_db(f"[+] Reasoning complete. Suggestions generated.")

        # 6. Advanced: Multi-Modal Generation (New)
        if multimodal_flag:
            await log_to_db("[*] Generating UI mockup and architecture diagram...")
            mockup_url = multimodal_agent.generate_ui_mockup(blueprint.get('project_name', 'App'), prompt)
            diagram_code = multimodal_agent.generate_architecture_diagram(blueprint)
            await websocket.send_text(json.dumps({"type": "multimodal", "mockup": mockup_url, "diagram": diagram_code}))
            await log_to_db("[+] Multi-modal assets generated.")

        # 7. Phase 2: Building
        project_path = os.path.join(os.getcwd(), "output", project_name)
        migrator = MigrationEngine(project_path)
        
        await log_to_db(f"[*] Starting multi-agent build for: {project_name}")
        # Initialize Rollback Manager for safety (New)
        rollback_mgr = RollbackManager(project_path)
        rollback_mgr.snapshot_project("initial_build")
        
        coder.build_project(blueprint, base_dir=project_path)
        await log_to_db(f"[+] Multi-agent build complete.")

        # 6. Phase 3: Auto-Bug Detection
        if lint_flag:
            await log_to_db("[*] Proactive bug detection and security scanning...")
            linter.scan_project(project_path, blueprint)
            await log_to_db("[+] Bug detection complete.")

        # 7. Phase 4: Self-Refining Code
        if refine_flag:
            await log_to_db("[*] Proactive code refinement and optimization...")
            refiner.refine_project(project_path, blueprint)
            await log_to_db("[+] Code refinement complete.")

        # 8. Phase 5: Database Orchestration
        await log_to_db("[*] Starting database orchestration...")
        sql_schema = blueprint.get("database_schema", "")
        if sql_schema:
            migrator.generate_migration(sql_schema)
            dev_conn = db_manager.setup_neon_branch(project_name, branch_name="dev")
            if dev_conn:
                db_manager.execute_sql(dev_conn, sql_schema)
                await log_to_db("[+] Database schema applied to dev branch.")
            else:
                await log_to_db("[!] Database connection missing. Schema saved to migrations/ folder.", "warning")

        # 9. Phase 6: Healing
        if heal_flag:
            await log_to_db("[*] Entering self-healing phase...")
            success = healer.heal_project(project_path, blueprint)
            if success:
                await log_to_db("[+] Project healed and verified.")
            else:
                await log_to_db("[!] Healing phase failed. Deploying anyway...", "warning")

        # 10. Phase 7: Autonomous Docs
        if docs_flag:
            await log_to_db("[*] Generating autonomous documentation...")
            docs_gen.generate_docs(project_path, blueprint)
            await log_to_db("[+] README.md and documentation generated.")

        # 11. Phase 8: Deployment
        await log_to_db(f"[*] Deploying to {deploy_target}...")
        deploy_url = ""
        if deploy_target == "railway":
            deployer.deploy_to_railway(project_path, project_name)
            deploy_url = f"https://{project_name}.up.railway.app"
        elif deploy_target == "vercel":
            deployer.deploy_to_vercel(project_path, project_name)
            deploy_url = f"https://{project_name}.vercel.app"
        else:
            deployer.deploy_to_netlify(project_path, project_name)
            deploy_url = f"https://{project_name}.netlify.app"

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
