import os
from smart_router import SmartRouter

class Linter:
    """
    Singularity AGI Linter Module (Autonomous Capabilities)
    Performs proactive bug detection and syntax checking before deployment.
    """
    
    def __init__(self, router: SmartRouter):
        self.router = router

    def scan_project(self, project_path: str, blueprint: dict):
        """
        Scans the project for syntax errors, common bugs, and security risks.
        """
        print(f"[*] Starting proactive bug detection for: {project_path}")
        
        # Scan files for basic syntax issues
        for file_info in blueprint.get("files", []):
            file_path = os.path.join(project_path, file_info["path"])
            if not os.path.exists(file_path):
                continue
                
            with open(file_path, "r") as f:
                code = f.read()
                
            issues = self._scan_file(file_info["path"], code)
            if issues:
                print(f"[!] Found issues in: {file_info['path']}. Fixing...")
                self._apply_fix(file_path, code, issues)

    def _scan_file(self, path: str, code: str) -> str:
        """
        Uses the Smart Router to detect potential bugs in a file.
        """
        prompt = f"""
        You are the 'Singularity Bug Detection Agent'. 
        Analyze the following code for common bugs, security vulnerabilities, or syntax errors.
        
        File: {path}
        Code:
        {code}
        
        Identify any CRITICAL issues. If none, output 'NONE'.
        Otherwise, list the issues briefly.
        """
        
        issues = self.router.call_llm(prompt, task_type="general")
        return "" if "NONE" in issues.upper() else issues

    def _apply_fix(self, file_path: str, code: str, issues: str):
        """
        Prompts the AI to fix the identified bugs.
        """
        prompt = f"""
        The following file has these bugs: {issues}.
        
        Current Code:
        {code}
        
        Provide the corrected source code. Output ONLY the code.
        """
        
        fixed_code = self.router.call_llm(prompt, task_type="coding")
        
        # Strip markdown code blocks
        if fixed_code.startswith("```"):
            lines = fixed_code.split("\n")
            fixed_code = "\n".join(lines[1:-1])
            
        with open(file_path, "w") as f:
            f.write(fixed_code)
        print(f"[+] Fixed issues in: {file_path}")
