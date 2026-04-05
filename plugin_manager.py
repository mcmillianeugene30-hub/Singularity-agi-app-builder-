import os
import json
import requests
from typing import List, Optional

class PluginManager:
    """
    Singularity AGI Plugin & Template Manager (Developer Experience)
    Extends the builder with custom AI agents and community templates.
    """
    
    def __init__(self, platform_url: str = None, supabase_client = None):
        self.platform_url = platform_url
        self.supabase = supabase_client
        self.plugins_dir = os.path.join(os.getcwd(), "plugins")
        
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir, exist_ok=True)

    def load_community_template(self, template_id: str) -> Optional[dict]:
        """
        Fetches a shared app template from the Supabase Template Marketplace.
        """
        if not self.supabase:
            print("[!] Supabase client missing. Skipping template loading.")
            return None

        print(f"[*] Fetching community template: {template_id}")
        try:
            response = self.supabase.table("templates").select("*").eq("id", template_id).execute()
            if not response.data:
                print(f"[!] Template {template_id} not found.")
                return None
            
            template = response.data[0]
            print(f"[+] Loaded template: {template.get('name')}")
            return template["blueprint"]
        except Exception as e:
            print(f"[!] Template retrieval failed: {e}")
            return None

    def register_custom_plugin(self, plugin_name: str, plugin_code: str):
        """
        Saves a custom AI agent or tool to the local plugins directory.
        """
        plugin_path = os.path.join(self.plugins_dir, f"{plugin_name.lower().replace(' ', '_')}.py")
        
        print(f"[*] Registering custom plugin: {plugin_name}")
        
        with open(plugin_path, "w") as f:
            f.write(plugin_code)
            
        print(f"[+] Plugin saved to: {plugin_path}")
        return plugin_path

    def list_active_plugins(self) -> List[str]:
        """
        Returns a list of all locally registered plugins.
        """
        return [f for f in os.listdir(self.plugins_dir) if f.endswith(".py")]
