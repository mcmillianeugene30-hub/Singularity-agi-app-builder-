import os
import time

class MigrationEngine:
    """
    Singularity AGI Migration Engine (Phase 5)
    Tracks and applies schema updates for the generated projects.
    """
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.migrations_dir = os.path.join(project_path, "migrations")
        
        if not os.path.exists(self.migrations_dir):
            os.makedirs(self.migrations_dir, exist_ok=True)

    def generate_migration(self, sql_schema: str) -> str:
        """
        Creates a new migration file with a timestamp.
        """
        timestamp = time.strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_initial_schema.sql"
        migration_path = os.path.join(self.migrations_dir, filename)
        
        print(f"[*] Generating migration: {filename}")
        
        with open(migration_path, "w") as f:
            f.write("-- Singularity AGI Migration File\n")
            f.write(f"-- Created: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(sql_schema)
            
        print(f"[+] Migration file saved to: {migration_path}")
        return migration_path

    def get_all_migrations(self) -> list:
        """
        Returns a sorted list of all migration file paths.
        """
        migrations = sorted([f for f in os.listdir(self.migrations_dir) if f.endswith(".sql")])
        return [os.path.join(self.migrations_dir, m) for m in migrations]
