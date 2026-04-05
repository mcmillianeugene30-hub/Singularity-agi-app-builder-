import os
import requests
from smart_router import SmartRouter

class MultiModalAgent:
    """
    Singularity AGI Multi-Modal Agent (Advanced AI Features)
    Generates UI mockups, architecture diagrams, and image assets.
    """
    
    def __init__(self, router: SmartRouter, openai_key: str = None, midjourney_url: str = None):
        self.router = router
        self.openai_key = openai_key
        self.midjourney_url = midjourney_url

    def generate_ui_mockup(self, project_name: str, description: str) -> str:
        """
        Generates a DALL-E or Midjourney-style image prompt for the UI mockup.
        Returns the generated image URL (or a mock URL for now).
        """
        print(f"[*] Generating UI mockup prompt for: {project_name}")
        
        prompt = f"""
        You are the 'Singularity Visual Architect'. 
        Generate a detailed image prompt for a high-quality UI/UX design for a {project_name} project.
        Description: {description}
        Style: Modern, sleek, dark-themed, glassmorphism, responsive dashboard.
        
        Output ONLY the image prompt.
        """
        
        image_prompt = self.router.call_llm(prompt, task_type="general")
        
        # In a real environment, we would call the DALL-E or Midjourney API here.
        # For now, we return a placeholder URL or a description of the generated mockup.
        print(f"[+] UI Mockup prompt generated: {image_prompt[:100]}...")
        return f"https://images.singularity-agi.ai/mockups/{project_name.lower().replace(' ', '-')}.png"

    def generate_architecture_diagram(self, blueprint: dict) -> str:
        """
        Generates a Mermaid.js diagram for the project architecture.
        This can be rendered in the Next.js dashboard.
        """
        print("[*] Generating architecture diagram (Mermaid.js)...")
        
        prompt = f"""
        You are the 'Singularity Diagram Agent'. 
        Based on the following project blueprint, generate a valid Mermaid.js flowchart 
        showing the system architecture (Frontend -> API -> Database -> Deployment).
        
        Blueprint: {blueprint}
        
        Output ONLY the Mermaid.js code. No preamble, no markdown formatting.
        """
        
        diagram_code = self.router.call_llm(prompt, task_type="architecture")
        
        # Strip markdown code blocks if present
        if diagram_code.startswith("```"):
            lines = diagram_code.split("\n")
            if lines[0].startswith("```"):
                diagram_code = "\n".join(lines[1:-1])
                
        return diagram_code.strip()
