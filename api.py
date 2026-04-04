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

app = FastAPI(title="Singularity AGI API")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "service": "singularity-agi-backend"}

class BuildRequest(BaseModel):
    prompt: str
    deploy: bool = False
    heal: bool = True
    docs: bool = True

@app.websocket("/ws/build")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Receive build request
    data = await websocket.receive_text()
    request_data = json.loads(data)
    prompt = request_data.get("prompt")
    deploy_flag = request_data.get("deploy", False)
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

        # 3. Phase 1: Planning
        await websocket.send_text(f"[*] Planning your app: '{prompt}'...")
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
        if deploy_flag:
            await websocket.send_text("[*] Deploying to GitHub and Netlify...")
            GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
            NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")
            if GITHUB_TOKEN and NETLIFY_TOKEN:
                deployer = Deployer(GITHUB_TOKEN, NETLIFY_TOKEN)
                deployer.deploy_to_netlify(project_path, project_name)
                await websocket.send_text("[SUCCESS] App is live!")
            else:
                await websocket.send_text("[!] Deployment tokens missing. Skipped.")

        await websocket.send_text(f"[SUCCESS] App '{project_name}' built in {project_path}")
        await websocket.close()
        
    except Exception as e:
        await websocket.send_text(f"[ERROR] {str(e)}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
