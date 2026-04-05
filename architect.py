import json
from smart_router import SmartRouter

class Architect:
    """
    Singularity AGI Architect Module
    Decomposes a user requirement into a structured project plan.
    """
    
    def __init__(self, router: SmartRouter):
        self.router = router

    def plan_project(self, user_prompt: str, deploy_target: str = "netlify") -> dict:
        """
        Creates a JSON blueprint for the project.
        """
        system_prompt = f"""
        You are the 'Singularity Architect'. Given a user's app idea, you must output a JSON blueprint for a full-stack app.
        The app will be deployed to: {deploy_target}.
        
        If deploy_target is 'railway', include a 'railway.json' in the files.
        If deploy_target is 'fly', include a 'fly.toml' and 'Dockerfile' in the files.
        If deploy_target is 'netlify', include a 'netlify.toml' in the files.
        
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
