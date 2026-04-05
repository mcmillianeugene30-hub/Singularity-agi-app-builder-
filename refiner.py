import os
from smart_router import SmartRouter

class Refiner:
    """
    Singularity AGI Refiner Module (Autonomous Capabilities)
    Proactively analyzes and optimizes generated code for performance, 
    cleanliness, and best practices.
    """
    
    def __init__(self, router: SmartRouter):
        self.router = router

    def refine_project(self, project_path: str, blueprint: dict):
        """
        Analyzes the generated project and applies proactive optimizations.
        """
        print(f"[*] Starting proactive refinement for: {project_path}")
        
        # We target key files like page.tsx, layout.tsx, and API routes
        files_to_refine = [f for f in blueprint.get("files", []) if any(x in f["path"] for x in ["page", "api", "lib"])]
        
        for file_info in files_to_refine:
            file_path = os.path.join(project_path, file_info["path"])
            if not os.path.exists(file_path):
                continue
                
            with open(file_path, "r") as f:
                original_code = f.read()
                
            print(f"[*] Refining: {file_info['path']}...")
            refined_code = self._get_refinement(file_info["path"], original_code, blueprint)
            
            if refined_code and refined_code != original_code:
                with open(file_path, "w") as f:
                    f.write(refined_code)
                print(f"[+] Refined: {file_info['path']}")
            else:
                print(f"[-] No refinements suggested for: {file_info['path']}")

    def _get_refinement(self, path: str, code: str, blueprint: dict) -> str:
        """
        Sends code to the Smart Router for proactive optimization suggestions.
        """
        prompt = f"""
        You are the 'Singularity Refiner Agent'. 
        Analyze the following code for a {blueprint.get('project_name')} project.
        
        File: {path}
        Current Code:
        {code}
        
        Identify opportunities for:
        1. Performance optimization (e.g., unnecessary re-renders, slow queries).
        2. Clean code (e.g., redundant logic, better variable naming).
        3. Security hardening.
        4. Modern best practices (e.g., React hooks, Supabase best practices).
        
        Output ONLY the improved, full source code for the file. 
        If no improvements are needed, output the original code exactly.
        No preamble, no markdown formatting.
        """
        
        # Use Gemini for deep reasoning and optimization
        refined = self.router.call_llm(prompt, task_type="architecture")
        
        # Strip markdown code blocks if present
        if refined.startswith("```"):
            lines = refined.split("\n")
            if lines[0].startswith("```"):
                refined = "\n".join(lines[1:-1])
                
        return refined.strip()
