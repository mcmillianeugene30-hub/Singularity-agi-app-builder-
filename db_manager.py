import os
import requests
import psycopg2
from typing import Optional

class DatabaseManager:
    """
    Singularity AGI Database Manager (Phase 5)
    Automates Supabase and Neon Database orchestration.
    """
    
    def __init__(self, neon_api_key: str = None, supabase_url: str = None, supabase_service_key: str = None):
        self.neon_api_key = neon_api_key
        self.supabase_url = supabase_url
        self.supabase_service_key = supabase_service_key

    def setup_neon_branch(self, project_id: str, branch_name: str = "dev") -> Optional[str]:
        """
        Creates a new Neon database branch for development/healing.
        Returns the connection string for the new branch.
        """
        if not self.neon_api_key:
            print("[!] Neon API key missing. Skipping branching.")
            return None

        print(f"[*] Creating Neon branch '{branch_name}' for project: {project_id}")
        try:
            url = f"https://console.neon.tech/api/v2/projects/{project_id}/branches"
            headers = {
                "Authorization": f"Bearer {self.neon_api_key}",
                "Content-Type": "application/json"
            }
            payload = {"branch": {"name": branch_name}}
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            branch_id = response.json()["branch"]["id"]
            
            # Get connection string for the branch
            conn_url = f"https://console.neon.tech/api/v2/projects/{project_id}/branches/{branch_id}/endpoints"
            conn_res = requests.get(conn_url, headers=headers)
            conn_res.raise_for_status()
            
            # Simplified: Returns the first endpoint's host
            host = conn_res.json()["endpoints"][0]["host"]
            print(f"[+] Neon branch created: {host}")
            return host
        except Exception as e:
            print(f"[!] Neon branching failed: {e}")
            return None

    def execute_sql(self, connection_string: str, sql_schema: str):
        """
        Executes the Architect's SQL schema against a live Postgres database.
        """
        print("[*] Executing database schema...")
        try:
            conn = psycopg2.connect(connection_string)
            cur = conn.cursor()
            cur.execute(sql_schema)
            conn.commit()
            cur.close()
            conn.close()
            print("[+] Database schema applied successfully.")
            return True
        except Exception as e:
            print(f"[!] SQL execution failed: {e}")
            return False

    def setup_supabase_auth(self, project_id: str):
        """
        Configures Supabase Auth (e.g., enabling Email/Password) via their management API.
        """
        if not self.supabase_service_key:
            return
            
        print(f"[*] Configuring Supabase Auth for project: {project_id}")
        # In a real implementation, we would call the Supabase Management API here.
        # For now, we assume standard defaults.
        pass

    def get_db_stats(self, connection_string: str) -> dict:
        """
        Retrieves table counts and storage size for the dashboard.
        """
        try:
            conn = psycopg2.connect(connection_string)
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';")
            table_count = cur.fetchone()[0]
            cur.close()
            conn.close()
            return {"tables": table_count, "status": "Healthy"}
        except:
            return {"tables": 0, "status": "Error"}
