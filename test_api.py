#!/usr/bin/env python
"""
Test script to verify the API configuration and basic functionality.
Run this before deploying to production.
"""

import os
import sys

def check_env_var(name, required=True):
    """Check if an environment variable is set."""
    value = os.getenv(name)
    if required and not value:
        print(f"❌ {name}: NOT SET (required)")
        return False
    elif value:
        # Mask sensitive values for display
        if "KEY" in name or "TOKEN" in name:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {name}: {masked}")
        else:
            print(f"✅ {name}: {value}")
        return True
    else:
        print(f"⚠️  {name}: NOT SET (optional)")
        return True

def main():
    print("=" * 60)
    print("Singularity AGI - API Configuration Test")
    print("=" * 60)
    print()

    # Test imports
    print("Testing module imports...")
    try:
        import api
        print("✅ api module loaded")
    except Exception as e:
        print(f"❌ Failed to load api module: {e}")
        return False

    try:
        from smart_router import SmartRouter
        print("✅ SmartRouter loaded")
    except Exception as e:
        print(f"❌ Failed to load SmartRouter: {e}")
        return False

    print()
    print("Checking environment variables...")
    print("-" * 60)

    all_good = True

    # AI Provider Keys
    print("\n🤖 AI Provider Keys:")
    all_good &= check_env_var("OPENROUTER_API_KEY")
    check_env_var("OPENROUTER_API_KEY_1", required=False)
    check_env_var("OPENROUTER_API_KEY_2", required=False)
    check_env_var("OPENROUTER_API_KEY_3", required=False)

    all_good &= check_env_var("GROQ_API_KEY")
    check_env_var("GROQ_API_KEY_1", required=False)
    check_env_var("GROQ_API_KEY_2", required=False)
    check_env_var("GROQ_API_KEY_3", required=False)

    all_good &= check_env_var("GEMINI_API_KEY")
    check_env_var("GEMINI_API_KEY_1", required=False)
    check_env_var("GEMINI_API_KEY_2", required=False)
    check_env_var("GEMINI_API_KEY_3", required=False)

    check_env_var("OPENAI_API_KEY", required=False)

    # Deployment Tokens
    print("\n🚀 Deployment Tokens:")
    all_good &= check_env_var("GITHUB_TOKEN")
    check_env_var("NETLIFY_TOKEN", required=False)
    check_env_var("VERCEL_TOKEN", required=False)
    check_env_var("RAILWAY_TOKEN", required=False)
    check_env_var("RENDER_API_KEY", required=False)

    # Database Configuration
    print("\n💾 Database Configuration:")
    check_env_var("SUPABASE_URL", required=False)
    check_env_var("SUPABASE_SERVICE_KEY", required=False)
    check_env_var("NEON_API_KEY", required=False)

    # Application Configuration
    print("\n⚙️  Application Configuration:")
    check_env_var("PORT", required=False)
    check_env_var("WORKERS", required=False)
    check_env_var("ENVIRONMENT", required=False)
    check_env_var("ALLOWED_ORIGINS", required=False)

    print()
    print("=" * 60)

    if all_good:
        print("✅ All required environment variables are set!")
        print("   The API is ready for deployment.")
        return True
    else:
        print("❌ Some required environment variables are missing.")
        print("   Please set them before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
