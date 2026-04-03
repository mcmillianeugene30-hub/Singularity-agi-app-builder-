import os
from smart_router import SmartRouter

class Coder:
    """
    Singularity AGI Coder Module
    Generates the actual source code for each file in the project blueprint.
    """
    
    def __init__(self, router: SmartRouter):
        self.router = router

    def generate_file(self, project_blueprint: dict, file_info: dict) -> str:
        """
        Generates the code for a specific file path.
        """
        prompt = f"""
        You are the 'Singularity Coder'. Write the full source code for the file: '{file_info['path']}'.
        The file's purpose: {file_info['description']}
        Context: Part of a Next.js/Supabase project called '{project_blueprint.get('project_name', 'Unnamed App')}'.
        Database Schema: {project_blueprint.get('database_schema', 'None provided.')}
        Output ONLY the raw code. No preamble, no comments about what you are doing.
        """
        
        # Use Groq for speed if it's a standard component, or Gemini for high context if it's complex logic
        task_type = "coding" if "page" in file_info['path'] else "general"
        code = self.router.call_llm(prompt, task_type=task_type)
        
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
            os.makedirs(base_dir)
            
        print(f"[*] Starting build for project: {project_blueprint.get('project_name')}")
        
        for file_info in project_blueprint.get('files', []):
            path = os.path.join(base_dir, file_info['path'])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            print(f"[*] Generating: {file_info['path']}")
            code = self.generate_file(project_blueprint, file_info)
            
            with open(path, "w") as f:
                f.write(code)
                
        print(f"[*] Project build complete in: {base_dir}")
