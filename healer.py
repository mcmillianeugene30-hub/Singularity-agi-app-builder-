import os
import subprocess
from smart_router import SmartRouter

class Healer:
    """
    Singularity AGI Healer Module
    Runs builds/lints and auto-fixes errors using AI feedback loops.
    """
    
    def __init__(self, router: SmartRouter):
        self.router = router
        self.max_retries = 3

    def heal_project(self, project_path: str, blueprint: dict):
        """
        Main healing loop: Build -> Catch Error -> Prompt AI -> Fix -> Repeat.
        """
        print(f"[*] Starting healing phase for: {project_path}")
        
        for attempt in range(self.max_retries):
            print(f"[*] Healing Attempt {attempt + 1}/{self.max_retries}...")
            
            # 1. Run Build/Check
            success, error_log = self._run_check(project_path)
            
            if success:
                print("[+] Build successful! No healing required.")
                return True
            
            print(f"[!] Build failed. Error detected:\n{error_log[:500]}...")
            
            # 2. Analyze and Fix
            self._apply_fixes(project_path, blueprint, error_log)
            
        print("[!] Healing failed after max retries. Manual intervention may be needed.")
        return False

    def _run_check(self, project_path: str):
        """
        Executes npm run build to check for errors.
        """
        try:
            # We use shell=True to handle npm commands easily
            result = subprocess.run(
                ["npm", "run", "build"], 
                cwd=project_path, 
                capture_output=True, 
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                return True, ""
            else:
                return False, result.stderr + "\n" + result.stdout
        except Exception as e:
            return False, str(e)

    def _apply_fixes(self, project_path: str, blueprint: dict, error_log: str):
        """
        Sends the error to the Smart Router and rewrites the offending files.
        """
        prompt = f"""
        You are the 'Singularity Healer'. The following project build failed.
        
        Project Blueprint: {blueprint}
        Error Log:
        {error_log}
        
        Identify the file causing the error and provide the corrected version of that file.
        Output ONLY the corrected code for that specific file.
        Include a header like 'FILE: path/to/file' so I know where to write it.
        """
        
        # Use Gemini for high-context error analysis
        correction = self.router.call_llm(prompt, task_type="architecture")
        
        # Parse the correction and overwrite the file
        if "FILE:" in correction:
            try:
                parts = correction.split("FILE:", 1)[1].split("\n", 1)
                file_path_rel = parts[0].strip()
                corrected_code = parts[1].strip()
                
                # Strip markdown code blocks
                if corrected_code.startswith("```"):
                    lines = corrected_code.split("\n")
                    corrected_code = "\n".join(lines[1:-1])
                
                full_path = os.path.join(project_path, file_path_rel)
                print(f"[*] Applying fix to: {file_path_rel}")
                
                with open(full_path, "w") as f:
                    f.write(corrected_code)
            except Exception as e:
                print(f"[!] Failed to parse Healer correction: {e}")
        else:
            print("[!] Healer could not identify a specific file to fix.")
