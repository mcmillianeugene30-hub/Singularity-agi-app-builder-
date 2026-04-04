import os
from smart_router import SmartRouter

class DocsGenerator:
    """
    Singularity AGI Autonomous Docs Generator
    Generates tailored documentation for every app built.
    """
    
    def __init__(self, router: SmartRouter):
        self.router = router

    def generate_docs(self, project_path: str, blueprint: dict):
        """
        Generates a comprehensive README.md and API.md for the generated project.
        """
        print(f"[*] Generating autonomous documentation for: {blueprint.get('project_name')}")
        
        prompt = f"""
        You are the 'Singularity Documentation Agent'. 
        Based on the following project blueprint, generate a high-quality, professional README.md.
        
        Project Blueprint: {blueprint}
        
        The README should include:
        1. Project Name and Description.
        2. Features.
        3. Setup instructions (Next.js, Supabase).
        4. Environment variables required.
        5. A section on 'Built with Singularity AGI'.
        
        Output ONLY the raw markdown for the README.md file.
        """
        
        readme_content = self.router.call_llm(prompt, task_type="general")
        
        # Strip markdown code blocks
        if readme_content.startswith("```"):
            lines = readme_content.split("\n")
            readme_content = "\n".join(lines[1:-1])
            
        readme_path = os.path.join(project_path, "README.md")
        with open(readme_path, "w") as f:
            f.write(readme_content)
            
        print(f"[+] README.md generated at {readme_path}")
