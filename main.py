import os
import argparse
from smart_router import SmartRouter
from architect import Architect
from coder import Coder
from deployer import Deployer

def main():
    parser = argparse.ArgumentParser(description="Singularity AGI Full-Stack AI App Builder")
    parser.add_argument("--prompt", type=str, required=True, help="Describe the app you want to build")
    parser.add_argument("--deploy", action="store_true", help="Automatically deploy to GitHub and Netlify")
    args = parser.parse_args()

    # 1. Initialize API Keys (from environment)
    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    GROQ_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")

    if not all([OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY]):
        print("[!] Missing AI API Keys. Check your .env file.")
        return

    # 2. Setup Smart Router & Modules
    router = SmartRouter(OPENROUTER_KEY, GROQ_KEY, GEMINI_KEY)
    architect = Architect(router)
    coder = Coder(router)
    deployer = Deployer(GITHUB_TOKEN, NETLIFY_TOKEN)

    # 3. Phase 1: Planning
    print(f"[*] Planning your app: '{args.prompt}'...")
    blueprint = architect.plan_project(args.prompt)
    
    if "error" in blueprint:
        print(f"[!] Planning failed: {blueprint['error']}")
        return

    # 4. Phase 2: Building
    project_name = blueprint.get('project_name', 'singularity-app')
    project_path = os.path.join(os.getcwd(), "output", project_name)
    coder.build_project(blueprint, base_dir=project_path)

    # 5. Phase 3: Deployment (Optional)
    if args.deploy:
        if not GITHUB_TOKEN or not NETLIFY_TOKEN:
            print("[!] Missing Deployment Tokens. Skipping deploy.")
        else:
            deployer.deploy_to_netlify(project_path, project_name)
            
    print(f"\n[SUCCESS] App '{project_name}' built in {project_path}")
    if args.deploy:
        print(f"Check your GitHub and Netlify accounts for the live site.")

if __name__ == "__main__":
    main()
