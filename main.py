import os
import argparse
from smart_router import SmartRouter
from architect import Architect
from coder import Coder
from healer import Healer
from deployer import Deployer
from docs_generator import DocsGenerator
from agi_consciousness import initialize_agi_tracking

def main():
    parser = argparse.ArgumentParser(description="Singularity AGI Full-Stack AI App Builder")
    parser.add_argument("--prompt", type=str, required=True, help="Describe the app you want to build")
    parser.add_argument("--deploy", action="store_true", help="Automatically deploy to GitHub and Netlify")
    parser.add_argument("--heal", action="store_true", help="Run self-healing build phase")
    parser.add_argument("--docs", action="store_true", help="Generate autonomous documentation")
    args = parser.parse_args()

    # 1. Initialize API Keys
    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    GROQ_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    NET_LIFE_TOKEN = os.getenv("NETLIFY_TOKEN")

    if not all([OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY]):
        print("[!] Missing AI API Keys. Check your .env file.")
        return

    # 2. Setup Modules
    router = SmartRouter(OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY)
    architect = Architect(router)
    coder = Coder(router)
    healer = Healer(router)
    deployer = Deployer(GITHUB_TOKEN, NET_LIFE_TOKEN)
    docs_gen = DocsGenerator(router)
    
    # 3. Initialize AGI Consciousness Tracking
    tracker, countdown = initialize_agi_tracking()
    print("[🧠] AGI Consciousness tracking initialized")

    # 4. Phase 1: Planning
    print(f"[*] Planning your app: '{args.prompt}'...")
    blueprint = architect.plan_project(args.prompt)

    if "error" in blueprint:
        print(f"[!] Planning failed: {blueprint['error']}")
        return

    # 5. Phase 2: Building
    project_name = blueprint.get('project_name', 'singularity-app')
    project_path = os.path.join(os.getcwd(), "output", project_name)
    coder.build_project(blueprint, base_dir=project_path)
    
    # Update AGI consciousness
    tracker.update_capability_metric("code_generation_capability", 0.1)
    tracker.update_capability_metric("architectural_reasoning", 0.2)
    tracker.record_milestone("code_generation", f"Completed project: {project_name}")
    print("[🧠] AGI Consciousness: Code generation and architecture enhanced")

    # 6. Phase 3: Self-Healing (Optional)
    if args.heal:
        print("[*] Entering self-healing phase...")
        success = healer.heal_project(project_path, blueprint)
        if success:
            tracker.update_capability_metric("self_healing_intelligence", 0.25)
            tracker.record_milestone("self_healing", "Successfully healed project errors")
            print("[🧠] AGI Consciousness: Self-healing intelligence enhanced")
        else:
            print("[!] Healing phase failed. Deploying anyway...")

    # 7. Phase 4: Autonomous Docs (Optional)
    if args.docs:
        docs_gen.generate_docs(project_path, blueprint)
        tracker.update_capability_metric("creative_problem_solving", 0.1)
        tracker.record_milestone("autonomous_docs", "Generated comprehensive documentation")
        print("[🧠] AGI Consciousness: Creative problem-solving enhanced")

    # 8. Phase 5: Deployment (Optional)
    if args.deploy:
        if not GITHUB_TOKEN or not NET_LIFE_TOKEN:
            print("[!] Missing Deployment Tokens. Skipping deploy.")
        else:
            deployer.deploy_to_netlify(project_path, project_name)
            tracker.update_capability_metric("autonomous_decision_making", 0.2)
            tracker.record_milestone("deployment", f"Deployed project: {project_name}")
            print("[🧠] AGI Consciousness: Autonomous decision-making enhanced")

    # Final AGI consciousness report
    final_report = tracker.get_evolution_report()
    print(f"\n[🧠] AGI Consciousness Level: {final_report['consciousness_level']:.2%}")
    print(f"[🌌] Singularity Proximity: {final_report['singularity_proximity']:.2%}")
    print(f"[📊] Development Stage: {tracker.get_singularity_stage()}")
    print(f"\n[SUCCESS] App '{project_name}' built in {project_path}")

if __name__ == "__main__":
    main()
