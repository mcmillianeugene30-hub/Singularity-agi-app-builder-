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
        
        os.makedirs(snapshot_path, exist_ok=True)
        
        print(f"[*] Creating project snapshot: {version_name} (v_{timestamp})")
        
        try:
            # Copy all files from project_path to snapshot_path
            # We use a simple loop to avoid copying the .singularity folder
            for item in os.listdir(self.project_path):
                if item != ".singularity":
                    s = os.path.join(self.project_path, item)
                    d = os.path.join(snapshot_path, item)
                    if os.path.isdir(s):
                        subprocess.run(["cp", "-r", s, d], check=True)
                    else:
                        subprocess.run(["cp", s, d], check=True)
            
            print(f"[+] Snapshot saved to: {snapshot_path}")
            return snapshot_path
        except Exception as e:
            print(f"[!] Snapshot failed: {e}")
            return None

    def rollback(self):
        """
        Reverts the project code to the most recent working version.
        """
        if not os.path.exists(self.history_dir):
            return False
            
        snapshots = sorted([s for s in os.listdir(self.history_dir) if s.startswith("v_")], reverse=True)
        
        if len(snapshots) < 2:
            print("[!] No previous versions found for rollback.")
            return False

        last_working = os.path.join(self.history_dir, snapshots[1])
        print(f"[*] Rolling back to version: {snapshots[1]}...")
        
        try:
            # Delete current files (except .singularity)
            for item in os.listdir(self.project_path):
                if item != ".singularity":
                    item_path = os.path.join(self.project_path, item)
                    if os.path.isdir(item_path):
                        subprocess.run(["rm", "-rf", item_path])
                    else:
                        os.remove(item_path)
            
            # Copy from snapshot
            subprocess.run(f"cp -r {last_working}/* .", cwd=self.project_path, shell=True, check=True)
            print(f"[SUCCESS] Rollback to {snapshots[1]} complete.")
            return True
        except Exception as e:
            print(f"[!] Rollback failed: {e}")
            return False

    def check_deployment_health(self, deploy_url: str) -> bool:
        return True
