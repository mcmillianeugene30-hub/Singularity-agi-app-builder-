import os
from smart_router import SmartRouter

class ReasoningEngine:
    """
    Singularity AGI Reasoning Engine (Advanced AI Features)
    Explains the 'WHY' behind architectural decisions and provides 
    personalized suggestions based on user context.
    """
    
    def __init__(self, router: SmartRouter):
        self.router = router

    def explain_blueprint(self, user_prompt: str, blueprint: dict) -> str:
        """
        Generates a natural language explanation of the project architecture.
        """
        print("[*] Generating architectural reasoning...")
        
        prompt = f"""
        You are the 'Singularity Architect Reasoning Engine'. 
        Explain why you made certain architectural decisions for this project:
        
        User Request: {user_prompt}
        Blueprint: {blueprint}
        
        Cover:
        1. Choice of tech stack and why it fits the request.
        2. Database schema design and relationship logic.
        3. Key component choices and their role in the UX.
        4. Security and performance considerations.
        
        Output in natural, professional language.
        """
        
        # Use OpenRouter's reasoning-enabled models for deep thinking
        reasoning = self.router.call_llm(prompt, task_type="architecture")
        return reasoning

    def suggest_features(self, user_prompt: str, blueprint: dict) -> list:
        """
        Suggests additional features the user might need based on their prompt.
        """
        print("[*] Generating predictive feature suggestions...")
        
        prompt = f"""
        You are the 'Singularity Predictive Suggestion Engine'.
        Given the following app idea and its current blueprint, suggest 3 advanced features
        that would significantly enhance the app's value.
        
        User Request: {user_prompt}
        Current Blueprint: {blueprint}
        
        Format as a simple list of strings.
        """
        
        suggestions_raw = self.router.call_llm(prompt, task_type="general")
        # Simplified parsing
        suggestions = [s.strip("- ").strip() for s in suggestions_raw.split("\n") if s.strip()]
        return suggestions[:3]
