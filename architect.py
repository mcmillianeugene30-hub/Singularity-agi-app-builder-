import json
from smart_router import SmartRouter

from typing import List, Optional
from supabase import create_client, Client

class Architect:
    """
    Singularity AGI Architect Module
    Decomposes a user requirement into a structured project plan.
    Supports Continuous Learning from successful patterns in Supabase.
    """
    
    def __init__(self, router: SmartRouter, supabase_client: Client = None):
        self.router = router
        self.supabase = supabase_client

    def _retrieve_patterns(self, user_prompt: str) -> str:
        """
        Queries the platform database (Supabase) for similar past projects
        that were successful. Returns them as context for the Architect.
        """
        if not self.supabase:
            return ""

        print("[*] Retrieving successful patterns from Supabase...")
        try:
            # We use a simple keyword search for similar prompts
            # In a real app, this would use pgvector or semantic search
            keywords = user_prompt.split()[:5]
            query = self.supabase.table("projects").select("prompt, blueprint").eq("status", "live")
            
            for word in keywords:
                query = query.ilike("prompt", f"%{word}%")
            
            results = query.limit(3).execute()
            
            if not results.data:
                return ""
            
            context = "Here are patterns from previous SUCCESSFUL builds to use as inspiration:\n"
            for row in results.data:
                context += f"- Prompt: {row['prompt']}\n- Blueprint: {row['blueprint']}\n"
            
            print(f"[+] Retrieved {len(results.data)} successful patterns.")
            return context
        except Exception as e:
            print(f"[!] Pattern retrieval failed: {e}")
            return ""

    def plan_project(self, user_prompt: str, deploy_target: str = "netlify") -> dict:
        """
        Creates a JSON blueprint for the project.
        """
        # 1. Continuous Learning: Retrieve past successful patterns
        patterns = self._retrieve_patterns(user_prompt)
        
        # 2. Adaptive Architecture: Dynamic stack selection based on requirements
        system_prompt = f"""
        You are the 'Singularity Architect'. Given a user's app idea, you must output a JSON blueprint for a full-stack app.
        The app will be deployed to: {deploy_target}.
        
        {patterns}
        
        Adaptive Stack Selection:
        - If the app is simple, use Next.js + Tailwind + Supabase.
        - If the app is data-heavy or needs Python, suggest a FastAPI/Flask backend.
        - If the app is a simple landing page, use Vite + React.
        - Always include the necessary config files (e.g., netlify.toml, railway.json, fly.toml, Dockerfile).
        
        The JSON must follow this structure:
        ...

          ],
          "database_schema": "SQL to create tables in Supabase",
          "env_vars": ["NEXT_PUBLIC_SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_ANON_KEY", ...]
        }
        Only output valid JSON. No preamble.
        """
        
        response = self.router.call_llm(f"{system_prompt}\n\nUser Request: {user_prompt}", task_type="architecture")
        
        # Strip potential markdown formatting
        if response.startswith("```json"):
            response = response.strip("```json").strip("```").strip()
            
        try:
            return json.loads(response)
        except Exception as e:
            print(f"[!] Architect failed to generate valid JSON: {e}")
            return {"error": "Failed to generate project plan."}

# Example:
# architect = Architect(router)
# plan = architect.plan_project("A dashboard for tracking personal workouts with progress charts.")
