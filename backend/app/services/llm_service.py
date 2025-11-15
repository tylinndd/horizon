"""
OpenRouter LLM Service
"""
import httpx
from app.core.config import settings
from typing import Optional, Dict


class LLMService:
    """Service for interacting with OpenRouter LLM API"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.base_url = "https://openrouter.ai/api/v1"
    
    async def query(
        self,
        prompt: str,
        context: Optional[Dict] = None
    ) -> str:
        """Query the LLM with a prompt"""
        if not self.api_key:
            raise ValueError("OpenRouter API key not configured")
        
        # Build messages
        messages = [{"role": "user", "content": prompt}]
        
        # Add context if provided
        if context:
            context_str = self._format_context(context)
            messages.insert(0, {
                "role": "system",
                "content": f"Context: {context_str}"
            })
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://horizon.app",  # Optional: for OpenRouter analytics
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            return result["choices"][0]["message"]["content"]
    
    def _format_context(self, context: Dict) -> str:
        """Format context dictionary into a string"""
        parts = []
        for key, value in context.items():
            parts.append(f"{key}: {value}")
        return "\n".join(parts)

