import os
from smart_router import SmartRouter

class Coder:
    """
    Singularity AGI Multi-Agent Coder
    Uses specialized sub-agents for Frontend, Backend, and Security.
    """
    
    def __init__(self, router: SmartRouter):
        self.router = router

    def _get_agent_prompt(self, file_path: str, description: str, blueprint: dict) -> str:
        """
        Routes the file to the correct specialized sub-agent.
        """
        # Frontend Agent
        if any(ext in file_path for ext in [".tsx", ".jsx", ".css", ".html"]):
            return f"""
            You are the 'Singularity Frontend Agent'. You are a master of Next.js 14+, Tailwind CSS, and Framer Motion.
            Write the full source code for: '{file_path}'.
            Purpose: {description}
            Context: Part of project '{blueprint.get('project_name')}'
            Requirements: Use modern, accessible UI components. Ensure mobile responsiveness.
            """
        
        # Backend & Database Agent
        elif any(ext in file_path for ext in [".ts", ".js", ".py", ".sql"]) or "api" in file_path or "lib" in file_path:
            return f"""
            You are the 'Singularity Backend Agent'. You are a master of Node.js, Python, Supabase, and SQL.
            Write the full source code for: '{file_path}'.
            Purpose: {description}
            Database Schema: {blueprint.get('database_schema')}
            Requirements: Ensure high performance, efficient queries, and error handling.
            """
        
        # Security Agent
        elif any(s in file_path for s in ["auth", "middleware", "security", "config"]):
            return f"""
            You are the 'Singularity Security Agent'. You are a master of Auth.js, JWT, and application security.
            Write the full source code for: '{file_path}'.
            Purpose: {description}
            Requirements: Secure authentication, proper role-based access control, and environment variable protection.
            """
        
        # Default General Agent
        return f"You are the 'Singularity Coder'. Write the full source code for: '{file_path}'. Purpose: {description}"

    def generate_file(self, project_blueprint: dict, file_info: dict) -> str:
        """
        Generates code using specialized agents.
        """
        agent_prompt = self._get_agent_prompt(file_info['path'], file_info['description'], project_blueprint)
        
        full_prompt = f"""
        {agent_prompt}
        Output ONLY the raw code. No preamble, no markdown formatting (if possible, else use code blocks).
        """
        
        # Use Groq for speed if it's a standard component, or Gemini for high context
        task_type = "coding" if ".tsx" in file_info['path'] else "general"
        code = self.router.call_llm(full_prompt, task_type=task_type)
        
        # Strip markdown code blocks if present
        if code.startswith("```"):
            lines = code.split("\n")
            if lines[0].startswith("```"):
                code = "\n".join(lines[1:-1])
                
        return code

    def build_project(self, project_blueprint: dict, base_dir: str = "/workspace/generated_app"):
        """
        Iterates through the blueprint and writes files to disk.
        """
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)
            
        print(f"[*] Starting multi-agent build for: {project_blueprint.get('project_name')}")
        
        for file_info in project_blueprint.get('files', []):
            path = os.path.join(base_dir, file_info['path'])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            print(f"[*] Generating ({file_info['path']})...")
            code = self.generate_file(project_blueprint, file_info)
            
            with open(path, "w") as f:
                f.write(code)
                
        print(f"[*] Multi-agent build complete.")
