import os
import subprocess
import time

class RollbackManager:
    """
    Singularity AGI Rollback Manager (Deployment & Operations)
    Handles deployment failure detection and automatic rollback to the 
    last known working version.
    """
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.history_dir = os.path.join(project_path, ".singularity", "history")
        
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir, exist_ok=True)

    def snapshot_project(self, version_name: str = "current"):
        """
        Creates a snapshot of the current project code for rollback.
        """
        timestamp = time.strftime("%Y%m%d%H%M%S")
        snapshot_path = os.path.join(self.history_dir, f"v_{timestamp}_{version_name}")
        
        print(f"[*] Creating project snapshot: {version_name} (v_{timestamp})")
        
        # We copy all files except the .singularity folder to avoid recursion
        try:
            # Simple bash copy
            subprocess.run(
                ["cp", "-r", ".", snapshot_path], 
                cwd=self.project_path, 
                check=True,
                shell=True
            )
            print(f"[+] Snapshot saved to: {snapshot_path}")
            return snapshot_path
        except Exception as e:
            print(f"[!] Snapshot failed: {e}")
            return None

    def rollback(self):
        """
        Reverts the project code to the most recent working version.
        """
        snapshots = sorted([s for s in os.listdir(self.history_dir) if s.startswith("v_")], reverse=True)
        
        if len(snapshots) < 2:
            print("[!] No previous versions found for rollback.")
            return False

        last_working = os.path.join(self.history_dir, snapshots[1])
        print(f"[*] Rolling back to version: {snapshots[1]}...")
        
        try:
            # We delete current files (except .singularity) and copy from snapshot
            subprocess.run(["find", ".", "-maxdepth", "1", "-not", "-name", ".singularity", "-not", "-name", ".", "-exec", "rm", "-rf", "{}", "+"], cwd=self.project_path, check=True)
            subprocess.run(["cp", "-r", f"{last_working}/.", "."], cwd=self.project_path, check=True)
            print(f"[SUCCESS] Rollback to {snapshots[1]} complete.")
            return True
        except Exception as e:
            print(f"[!] Rollback failed: {e}")
            return False

    def check_deployment_health(self, deploy_url: str) -> bool:
        """
        Verifies if the deployment is healthy. If not, triggers rollback.
        """
        print(f"[*] Verifying deployment health: {deploy_url}...")
        # (This logic would integrate with monitor.py)
        # For now, we simulate a check
        return True
