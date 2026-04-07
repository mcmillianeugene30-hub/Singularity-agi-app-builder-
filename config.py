"""
Production Configuration Module for Singularity AGI
Centralizes configuration management for different environments
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Server Configuration
    PORT: int = 8000
    WORKERS: int = 1
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"

    # CORS Configuration
    ALLOWED_ORIGINS: str = "*"

    # AI Provider Keys
    OPENROUTER_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Deployment Tokens
    GITHUB_TOKEN: Optional[str] = None
    NETLIFY_TOKEN: Optional[str] = None
    VERCEL_TOKEN: Optional[str] = None
    RAILWAY_TOKEN: Optional[str] = None
    RENDER_API_KEY: Optional[str] = None

    # Database Configuration
    SUPABASE_URL: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None
    NEON_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT.lower() in ("development", "dev", "local")

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT.lower() in ("production", "prod")

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        if self.ALLOWED_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    def get_all_keys(self, prefix: str) -> List[str]:
        """Get all keys with a given prefix (supports rotation)"""
        keys = []
        main_key = getattr(self, prefix, None)
        if main_key:
            keys.append(main_key)

        # Look for numbered keys (PREFIX_1, PREFIX_2, etc.)
        i = 1
        while True:
            key_name = f"{prefix}_{i}"
            key_value = os.getenv(key_name)
            if not key_value:
                break
            keys.append(key_value)
            i += 1

        return keys

    def validate_required_keys(self) -> bool:
        """Validate that required API keys are present"""
        required_keys = ["OPENROUTER_API_KEY", "GROQ_API_KEY", "GEMINI_API_KEY"]
        missing_keys = [key for key in required_keys if not getattr(self, key, None)]

        if missing_keys:
            print(f"[!] Missing required API keys: {', '.join(missing_keys)}")
            return False

        return True


# Global settings instance
settings = Settings()
