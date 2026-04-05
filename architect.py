import json
from smart_router import SmartRouter
from typing import List, Optional
from supabase import create_client, Client

class Architect:
    """
    Singularity AGI Architect Module
    Decomposes a user requirement into a structured project plan.
    """
    
    def __init__(self, router: SmartRouter, supabase_client: Client = None):
        self.router = router
        self.supabase = supabase_client

    def _retrieve_patterns(self, user_prompt: str) -> str:
        if not self.supabase:
            return ""
        print("[*] Retrieving successful patterns from Supabase...")
        try:
            keywords = user_prompt.split()[:5]
            query = self.supabase.table("projects").select("prompt, blueprint") \
                .eq("status", "live") \
                .gte("rating", 4)
            for word in keywords:
                query = query.ilike("prompt", f"%{word}%")
            results = query.limit(3).execute()
            if not results.data:
                return ""
            context = "Previous successful patterns:\n"
            for row in results.data:
                context += f"- Prompt: {row['prompt']}\n- Blueprint: {row['blueprint']}\n"
            return context
        except Exception as e:
            print(f"[!] Pattern retrieval failed: {e}")
            return ""

    def plan_project(self, user_prompt: str, deploy_target: str = "netlify") -> dict:
        patterns = self._retrieve_patterns(user_prompt)
        
        system_prompt = f"""
        You are the 'Singularity Architect'. Generate a JSON blueprint for a full-stack app.
        Deploy Target: {deploy_target}
        {patterns}
        
        Stack Rules:
        - Small/Landing: Next.js + Tailwind + Supabase (Netlify/Vercel)
        - Data/API heavy: FastAPI + Postgres (Railway/Render)
        
        You MUST output ONLY valid JSON. No preamble, no commentary, no markdown code blocks.
        
        Required JSON Structure:
        {{
          "project_name": "app-slug",
          "files": [
            {{"path": "app/page.tsx", "description": "file content details"}},
            {{"path": "package.json", "description": "dependencies"}}
          ],
          "database_schema": "SQL schema",
          "env_vars": ["KEY1", "KEY2"]
        }}
        """
        
        response = self.router.call_llm(f"{system_prompt}\n\nUser Request: {user_prompt}", task_type="architecture")
        
        # Aggressive JSON extraction
        json_str = response
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        else:
            # Try to find the first '{' and last '}'
            start = json_str.find('{')
            end = json_str.rfind('}')
            if start != -1 and end != -1:
                json_str = json_str[start:end+1]
            
        try:
            return json.loads(json_str)
        except Exception as e:
            print(f"[!] Architect failed to generate valid JSON: {e}")
            print(f"[*] Raw Response: {response}")
            return {"error": "Failed to generate project plan."}
