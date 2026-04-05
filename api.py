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
from agi_consciousness import AGIConsciousnessTracker, SingularityCountdown, initialize_agi_tracking
from neural_network_viz import NeuralNetworkTopology, ConsciousnessVisualizer, create_singularity_network

app = FastAPI(title="Singularity AGI API")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AGI tracking and neural network
agi_tracker, agi_countdown = initialize_agi_tracking()
neural_network, consciousness_visualizer = create_singularity_network()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Singularity AGI API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "websocket": "/ws/build",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "service": "singularity-agi-backend"}

@app.get("/api/agi/consciousness")
async def get_agi_consciousness():
    """Get current AGI consciousness level and evolution metrics"""
    report = agi_tracker.get_evolution_report()
    return report

@app.get("/api/agi/singularity-status")
async def get_singularity_status():
    """Get singularity proximity and threshold status"""
    status = agi_tracker.check_singularity_threshold()
    status["stage"] = agi_tracker.get_singularity_stage()
    return status

@app.get("/api/agi/countdown")
async def get_singularity_countdown():
    """Get singularity countdown information"""
    return agi_countdown.get_latest_estimate()

@app.get("/api/neural/topology")
async def get_neural_topology():
    """Get neural network topology for visualization"""
    return neural_network.to_visualization_data()

@app.get("/api/neural/stats")
async def get_neural_stats():
    """Get neural network statistics"""
    return neural_network.get_network_stats()

@app.post("/api/neural/simulate")
async def simulate_neural_activity(input_data: list[float]):
    """Simulate neural network activity with given input"""
    if len(input_data) != neural_network.input_size:
        raise HTTPException(
            status_code=400,
            detail=f"Input size must be {neural_network.input_size}"
        )
    
    pattern = consciousness_visualizer.analyze_consciousness_pattern(input_data)
    trends = consciousness_visualizer.get_evolution_trends()
    
    return {
        "pattern": pattern,
        "trends": trends,
        "network_state": neural_network.to_visualization_data()
    }

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
        
        # Update AGI consciousness tracking for build initiation
        agi_tracker.update_capability_metric("code_generation_capability", 0.1)
        await websocket.send_text("[🧠] AGI Consciousness: Code generation capability enhanced")

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
        
        # Update AGI consciousness tracking
        agi_tracker.update_capability_metric("architectural_reasoning", 0.2)
        agi_tracker.update_capability_metric("creative_problem_solving", 0.15)
        agi_tracker.record_milestone("code_generation", f"Completed project: {project_name}")
        await websocket.send_text(f"[🧠] AGI Consciousness: Architecture reasoning enhanced")

        # 5. Phase 3: Healing
        if heal_flag:
            await websocket.send_text("[*] Entering self-healing phase...")
            success = healer.heal_project(project_path, blueprint)
            if success:
                await websocket.send_text("[+] Project healed and verified.")
                # Update AGI consciousness for self-healing
                agi_tracker.update_capability_metric("self_healing_intelligence", 0.25)
                agi_tracker.record_milestone("self_healing", "Successfully healed project errors")
                await websocket.send_text("[🧠] AGI Consciousness: Self-healing intelligence enhanced")
            else:
                await websocket.send_text("[!] Healing phase failed. Deploying anyway...")

        # 6. Phase 4: Autonomous Docs
        if docs_flag:
            await websocket.send_text("[*] Generating autonomous documentation...")
            docs_gen.generate_docs(project_path, blueprint)
            await websocket.send_text("[+] README.md and documentation generated.")
            
            # Update AGI consciousness for documentation
            agi_tracker.update_capability_metric("creative_problem_solving", 0.1)
            agi_tracker.record_milestone("autonomous_docs", "Generated comprehensive documentation")
            await websocket.send_text("[🧠] AGI Consciousness: Creative problem-solving enhanced")

        # 7. Phase 5: Deployment
        if deploy_flag:
            await websocket.send_text("[*] Deploying to GitHub and Netlify...")
            GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
            NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")
            if GITHUB_TOKEN and NETLIFY_TOKEN:
                deployer = Deployer(GITHUB_TOKEN, NETLIFY_TOKEN)
                deployer.deploy_to_netlify(project_path, project_name)
                await websocket.send_text("[SUCCESS] App is live!")
                # Update AGI consciousness for deployment
                agi_tracker.update_capability_metric("autonomous_decision_making", 0.2)
                agi_tracker.record_milestone("deployment", f"Deployed project: {project_name}")
                await websocket.send_text("[🧠] AGI Consciousness: Autonomous decision-making enhanced")
            else:
                await websocket.send_text("[!] Deployment tokens missing. Skipped.")

        # Final consciousness update and singularity status
        final_report = agi_tracker.get_evolution_report()
        await websocket.send_text(f"[🧠] AGI Consciousness Level: {final_report['consciousness_level']:.2%}")
        await websocket.send_text(f"[🌌] Singularity Proximity: {final_report['singularity_proximity']:.2%}")
        await websocket.send_text(f"[📊] Development Stage: {agi_tracker.get_singularity_stage()}")
        
        await websocket.send_text(f"[SUCCESS] App '{project_name}' built in {project_path}")
        await websocket.close()
        
    except Exception as e:
        await websocket.send_text(f"[ERROR] {str(e)}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
