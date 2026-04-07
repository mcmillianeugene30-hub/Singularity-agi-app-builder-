import os
import argparse
from typing import List
from dotenv import load_dotenv
from smart_router import SmartRouter
from architect import Architect
from coder import Coder
from healer import Healer
from deployer import Deployer
from docs_generator import DocsGenerator
from db_manager import DatabaseManager
from migration_engine import MigrationEngine
from refiner import Refiner
from linter import Linter
from reasoning_engine import ReasoningEngine
from multimodal import MultiModalAgent
from rollback import RollbackManager
from plugin_manager import PluginManager
from supabase import create_client, Client

def get_all_keys(prefix: str) -> List[str]:
    keys = []
    main_key = os.getenv(prefix)
    if main_key:
        keys.append(main_key)
    i = 1
    while True:
        key = os.getenv(f"{prefix}_{i}")
        if not key:
            break
        keys.append(key)
        i += 1
    return keys

def main():
    load_dotenv() # Load variables from .env
    parser = argparse.ArgumentParser(description="Singularity AGI Full-Stack AI App Builder")
    parser.add_argument("--prompt", type=str, required=True, help="Describe the app you want to build")
    parser.add_argument("--deploy", action="store_true", help="Automatically deploy to GitHub and Netlify")
    parser.add_argument("--heal", action="store_true", help="Run self-healing build phase")
    parser.add_argument("--docs", action="store_true", help="Generate autonomous documentation")
    parser.add_argument("--db", action="store_true", help="Automate database setup (Supabase/Neon)")
    parser.add_argument("--refine", action="store_true", help="Autonomous: Self-Refining Code")
    parser.add_argument("--lint", action="store_true", help="Autonomous: Auto-Bug Detection")
    parser.add_argument("--reason", action="store_true", help="Advanced: Code Reasoning & Suggestions")
    parser.add_argument("--multimodal", action="store_true", help="Advanced: Multi-Modal (Mockups/Diagrams)")
    args = parser.parse_args()

    # 1. Initialize API Keys
    OPENROUTER_KEYS = get_all_keys("OPENROUTER_API_KEY")
    GROQ_KEYS = get_all_keys("GROQ_API_KEY")
    GEMINI_KEYS = get_all_keys("GEMINI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    NET_LIFE_TOKEN = os.getenv("NETLIFY_TOKEN")
    NEON_API_KEY = os.getenv("NEON_API_KEY")
    PLATFORM_URL = os.getenv("SUPABASE_URL")
    PLATFORM_KEY = os.getenv("SUPABASE_SERVICE_KEY")

    if not (OPENROUTER_KEYS and GROQ_KEYS and GEMINI_KEYS):
        print("[!] Missing AI API Keys. Check your .env file.")
        return

    # Initialize Supabase client for Continuous Learning
    supabase = None
    if PLATFORM_URL and PLATFORM_KEY:
        supabase = create_client(PLATFORM_URL, PLATFORM_KEY)

    # 2. Setup Modules
    router = SmartRouter(OPENROUTER_KEYS, GROQ_KEYS, GEMINI_KEYS)
    architect = Architect(router, supabase_client=supabase)
    coder = Coder(router)
    healer = Healer(router)
    deployer = Deployer(GITHUB_TOKEN, NET_LIFE_TOKEN)
    docs_gen = DocsGenerator(router)
    db_manager = DatabaseManager(NEON_API_KEY)
    refiner = Refiner(router)
    linter = Linter(router)
    reasoning_engine = ReasoningEngine(router)
    multimodal_agent = MultiModalAgent(router)
    plugin_mgr = PluginManager(supabase_client=supabase)

    # 3. Phase 1: Planning
    print(f"[*] Planning your app: '{args.prompt}'...")
    blueprint = architect.plan_project(args.prompt)
    
    if "error" in blueprint:
        print(f"[!] Planning failed: {blueprint['error']}")
        return

    # 4. Phase 2: Building
    project_name = blueprint.get('project_name', 'singularity-app')
    project_path = os.path.join(os.getcwd(), "output", project_name)
    
    # Initialize Rollback Manager (New)
    rollback_mgr = RollbackManager(project_path)
    rollback_mgr.snapshot_project("initial_build")
    
    coder.build_project(blueprint, base_dir=project_path)

    # 5. Phase 3: Auto-Bug Detection (New)
    if args.lint:
        linter.scan_project(project_path, blueprint)

    # 6. Phase 4: Self-Refining Code (New)
    if args.refine:
        refiner.refine_project(project_path, blueprint)

    # 7. Phase 5: Database Orchestration (Optional)
    if args.db:
        print("[*] Starting database orchestration...")
        migrator = MigrationEngine(project_path)
        sql_schema = blueprint.get("database_schema")
        if sql_schema:
            migrator.generate_migration(sql_schema)
            # Execute schema...
            pass

    # 8. Advanced: Reasoning & Multi-Modal (New)
    if args.reason:
        reasoning_engine.explain_blueprint(args.prompt, blueprint)
        reasoning_engine.suggest_features(args.prompt, blueprint)
    
    if args.multimodal:
        multimodal_agent.generate_ui_mockup(project_name, args.prompt)
        multimodal_agent.generate_architecture_diagram(blueprint)

    # 9. Phase 6: Self-Healing (Optional)

    if args.heal:
        print("[*] Entering self-healing phase...")
        success = healer.heal_project(project_path, blueprint)
        if not success:
            print("[!] Healing phase failed. Deploying anyway...")

    # 9. Phase 7: Autonomous Docs (Optional)
    if args.docs:
        docs_gen.generate_docs(project_path, blueprint)

    # 10. Phase 8: Deployment (Optional)
    if args.deploy:
        if not GITHUB_TOKEN or not NET_LIFE_TOKEN:
            print("[!] Missing Deployment Tokens. Skipping deploy.")
        else:
            deployer.deploy_to_netlify(project_path, project_name)
            
    print(f"\n[SUCCESS] App '{project_name}' built in {project_path}")

if __name__ == "__main__":
    main()
