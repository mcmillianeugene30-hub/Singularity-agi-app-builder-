import time
import os
import requests
from typing import List, Dict, Any, Optional

class SmartRouter:
    """
    Singularity AGI Smart Router (2026 Edition)
    Now supports Multi-Key Rotation for Gemini, Groq, and OpenRouter.
    """
    
    def __init__(self, openrouter_keys: List[str], groq_keys: List[str], gemini_keys: List[str]):
        self.key_pool = {
            "openrouter": openrouter_keys,
            "groq": groq_keys,
            "gemini": gemini_keys
        }
        self.current_indices = {
            "openrouter": 0,
            "groq": 0,
            "gemini": 0
        }
        self.status = {
            "gemini": {"rpd": 250 * len(gemini_keys), "rpm": 20 * len(gemini_keys), "last_reset": time.time()},
            "groq": {"rpd": 1000 * len(groq_keys), "rpm": 30 * len(groq_keys), "last_reset": time.time()},
            "openrouter": {"rpd": 50 * len(openrouter_keys), "rpm": 20 * len(openrouter_keys), "last_reset": time.time()}
        }

    def _get_current_key(self, provider: str) -> str:
        idx = self.current_indices[provider]
        return self.key_pool[provider][idx]

    def _rotate_key(self, provider: str) -> bool:
        """
        Rotates to the next key in the pool for a specific provider.
        Returns False if all keys for this provider have been tried in this cycle.
        """
        self.current_indices[provider] = (self.current_indices[provider] + 1) % len(self.key_pool[provider])
        # If we wrapped around, it means we've tried all keys
        if self.current_indices[provider] == 0:
            print(f"[!] All keys for {provider} hit rate limits.")
            return False
        print(f"[*] Rotating to key #{self.current_indices[provider] + 1} for {provider}")
        return True

    def _get_best_provider(self, task_type: str) -> str:
        if task_type == "architecture":
            if self.status["gemini"]["rpd"] > 0: return "gemini"
            if self.status["groq"]["rpd"] > 0: return "groq"
        
        if self.status["groq"]["rpd"] > 0: return "groq"
        if self.status["gemini"]["rpd"] > 0: return "gemini"
        if self.status["openrouter"]["rpd"] > 0: return "openrouter"
        raise Exception("All free tiers exhausted across all keys.")

    def call_llm(self, prompt: str, task_type: str = "general") -> str:
        provider = self._get_best_provider(task_type)
        print(f"[*] Using provider: {provider} (Key #{self.current_indices[provider] + 1})")
        
        try:
            if provider == "gemini": return self._call_gemini(prompt)
            elif provider == "groq": return self._call_groq(prompt, task_type)
            elif provider == "openrouter": return self._call_openrouter(prompt)
        except Exception as e:
            if "429" in str(e) or "limit" in str(e).lower() or "quota" in str(e).lower():
                if self._rotate_key(provider):
                    return self.call_llm(prompt, task_type) # Try again with new key
            
            print(f"[!] Error with {provider}: {e}")
            self.status[provider]["rpd"] = 0 
            return self.call_llm(prompt, task_type)

    def _call_gemini(self, prompt: str):
        key = self._get_current_key("gemini")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']

    def _call_groq(self, prompt: str, task_type: str):
        key = self._get_current_key("groq")
        model = "llama-3.3-70b-versatile" if task_type == "architecture" else "llama-3.1-8b-instant"
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {key}"}
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200: raise Exception(f"HTTP {response.status_code}: {response.text}")
        return response.json()['choices'][0]['message']['content']

    def _call_openrouter(self, prompt: str):
        key = self._get_current_key("openrouter")
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key}",
            "HTTP-Referer": "https://singularity-agi.ai",
            "X-Title": "Singularity AGI"
        }
        payload = {
            "model": "google/gemini-2.0-flash-001", 
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200: raise Exception(f"HTTP {response.status_code}: {response.text}")
        return response.json()['choices'][0]['message']['content']
