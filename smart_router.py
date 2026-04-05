import time
import os
import requests
from typing import List, Dict, Any, Optional

class SmartRouter:
    """
    Singularity AGI Smart Router (2026 Edition)
    """
    
    def __init__(self, openrouter_key: str, groq_key: str, gemini_key: str):
        self.keys = {"openrouter": openrouter_key, "groq": groq_key, "gemini": gemini_key}
        self.status = {
            "gemini": {"rpd": 250, "rpm": 20, "last_reset": time.time()},
            "groq": {"rpd": 1000, "rpm": 30, "last_reset": time.time()},
            "openrouter": {"rpd": 50, "rpm": 20, "last_reset": time.time()}
        }

    def _get_best_provider(self, task_type: str) -> str:
        # For architecture, prefer Gemini (High Context) or high-end Groq
        if task_type == "architecture":
            if self.status["gemini"]["rpd"] > 0: return "gemini"
            if self.status["groq"]["rpd"] > 0: return "groq"
        
        if self.status["groq"]["rpd"] > 0: return "groq"
        if self.status["gemini"]["rpd"] > 0: return "gemini"
        if self.status["openrouter"]["rpd"] > 0: return "openrouter"
        raise Exception("All free tiers exhausted.")

    def call_llm(self, prompt: str, task_type: str = "general") -> str:
        provider = self._get_best_provider(task_type)
        print(f"[*] Using provider: {provider}")
        try:
            if provider == "gemini": return self._call_gemini(prompt)
            elif provider == "groq": return self._call_groq(prompt, task_type)
            elif provider == "openrouter": return self._call_openrouter(prompt)
        except Exception as e:
            print(f"[!] Error with {provider}: {e}")
            self.status[provider]["rpd"] = 0 
            return self.call_llm(prompt, task_type)

    def _call_gemini(self, prompt: str):
        # Use the most compatible endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.keys['gemini']}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            # Try fallback to flash if pro fails
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.keys['gemini']}"
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']

    def _call_groq(self, prompt: str, task_type: str):
        # Use versatile model for architecture/complex tasks
        model = "llama-3.3-70b-versatile" if task_type == "architecture" else "llama-3.1-8b-instant"
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.keys['groq']}"}
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200: raise Exception(f"HTTP {response.status_code}: {response.text}")
        return response.json()['choices'][0]['message']['content']

    def _call_openrouter(self, prompt: str):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.keys['openrouter']}",
            "HTTP-Referer": "https://singularity-agi.ai",
            "X-Title": "Singularity AGI"
        }
        # Use a reliable free model that supports coding/reasoning
        payload = {
            "model": "google/gemini-2.0-flash-001", 
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200: raise Exception(f"HTTP {response.status_code}: {response.text}")
        return response.json()['choices'][0]['message']['content']
