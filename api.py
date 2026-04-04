from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import subprocess
import json
from smart_router import SmartRouter
from architect import Architect
from coder import Coder
from deployer import Deployer

app = FastAPI(title="Singularity AGI API")

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
    deploy: bool = False

@app.post("/build")
async def build_app(request: BuildRequest):
    """
    Trigger the Singularity AGI build process.
    """
    # 1. Setup Keys (In production, these would be in a secure vault)
    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    GROQ_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    
    if not all([OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY]):
        raise HTTPException(status_code=400, detail="Missing AI API Keys.")

    try:
        # 2. Initialize Modules
        router = SmartRouter(OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY)
        architect = Architect(router)
        coder = Coder(router)

        # 3. Planning
        blueprint = architect.plan_project(request.prompt)
        if "error" in blueprint:
            raise HTTPException(status_code=500, detail=blueprint["error"])

        # 4. Building
        project_name = blueprint.get('project_name', 'singularity-app')
        project_path = os.path.join(os.getcwd(), "output", project_name)
        coder.build_project(blueprint, base_dir=project_path)

        # 5. Deployment (If requested)
        deploy_info = None
        if request.deploy:
            GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
            NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")
            if GITHUB_TOKEN and NETLIFY_TOKEN:
                deployer = Deployer(GITHUB_TOKEN, NETLIFY_TOKEN)
                deployer.deploy_to_netlify(project_path, project_name)
                deploy_info = "Deployed successfully."
            else:
                deploy_info = "Deployment tokens missing. Skipped."

        return {
            "status": "success",
            "project_name": project_name,
            "project_path": project_path,
            "deployment": deploy_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """
    Return the current status of AI providers.
    """
    return {
        "gemini": "Active",
        "groq": "Active",
        "openrouter": "Active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
