import os
import json
from smart_router import SmartRouter
from supabase import Client

class Evolver:
    """
    Singularity AGI Evolver Module (Self-Improvement Loop & Version Evolution)
    Analyzes failed builds and user feedback to evolve the builder's logic.
    """
    
    def __init__(self, router: SmartRouter, supabase: Client):
        self.router = router
        self.supabase = supabase

    def evolve_system(self):
        """
        Periodically run to improve the builder's internal instructions.
        1. Fetch failed projects or low ratings.
        2. Analyze root causes using AI reasoning.
        3. Suggest prompt or logic updates.
        """
        print("[*] Starting Version Evolution analysis...")
        
        # Fetch low-rated or failed projects
        try:
            low_quality = self.supabase.table("projects") \
                .select("prompt, blueprint, feedback, status") \
                .or_("status.eq.failed,rating.lt.3") \
                .limit(5).execute()
            
            if not low_quality.data:
                print("[+] System performance is optimal. No evolution needed.")
                return

            analysis_prompt = f"""
            You are the 'Singularity Evolution Agent'.
            Analyze the following failed or low-rated build attempts:
            {json.dumps(low_quality.data)}
            
            Identify common failure patterns or architectural weaknesses.
            Suggest 3 specific improvements to the 'Architect' or 'Coder' system prompts
            to prevent these issues in the future.
            
            Output your analysis and evolved instruction snippets.
            """
            
            evolution_report = self.router.call_llm(analysis_prompt, task_type="architecture")
            print(f"[+] Evolution Report Generated:\n{evolution_report[:500]}...")
            
            # In a fully autonomous AGI, this would then patch the .py files 
            # or update an 'instructions.json' file used by all agents.
            self._save_evolution_milestone(evolution_report)
            
        except Exception as e:
            print(f"[!] Evolution cycle failed: {e}")

    def _save_evolution_milestone(self, report: str):
        """
        Saves the evolution report to the platform database.
        """
        self.supabase.table("build_logs").insert({
            "message": f"SYSTEM EVOLUTION: {report[:200]}...",
            "type": "info"
        }).execute()
        print("[+] Evolution milestone saved to database.")
