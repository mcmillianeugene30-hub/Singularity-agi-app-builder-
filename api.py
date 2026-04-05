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

from monitor import Monitor

app = FastAPI(title="Singularity AGI API")
monitor = Monitor()

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
    deploy: str = "netlify" # Options: netlify, railway, fly
    heal: bool = True
    docs: bool = True

@app.get("/monitor")
async def get_monitor_status():
    """
    Return the live status of all monitored apps.
    """
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
    
    # 1. Setup Keys
    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    GROQ_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    
    if not all([OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY]):
        await websocket.send_text("[!] Missing AI API Keys. Build halted.")
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
