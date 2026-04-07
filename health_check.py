#!/usr/bin/env python3
"""
Health Check Script for Singularity AGI
Verifies that all required dependencies and services are available
"""
import sys
import os
from typing import List, Tuple

def check_import(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """Check if a Python module can be imported"""
    try:
        __import__(module_name)
        return True, f"✓ {module_name}"
    except ImportError:
        pkg = package_name or module_name
        return False, f"✗ {module_name} (install with: pip install {pkg})"

def check_env_var(var_name: str) -> Tuple[bool, str]:
    """Check if an environment variable is set"""
    value = os.getenv(var_name)
    if value:
        masked = value[:4] + "..." if len(value) > 7 else "..."
        return True, f"✓ {var_name} = {masked}"
    return False, f"✗ {var_name} (not set)"

def main():
    print("=" * 60)
    print("🏥 Singularity AGI Health Check")
    print("=" * 60)

    checks_passed = 0
    checks_failed = 0

    # Check Python version
    print("\n📋 Python Environment:")
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 10:
        print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        checks_passed += 1
    else:
        print(f"✗ Python {python_version.major}.{python_version.minor} (requires 3.10+)")
        checks_failed += 1

    # Check required modules
    print("\n📦 Required Python Modules:")
    modules = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn[standard]"),
        ("pydantic", "pydantic"),
        ("requests", "requests"),
        ("websockets", "websockets"),
        ("supabase", "supabase"),
        ("dotenv", "python-dotenv"),
    ]

    for module, package in modules:
        success, msg = check_import(module, package)
        print(msg)
        if success:
            checks_passed += 1
        else:
            checks_failed += 1

    # Check optional modules
    print("\n📦 Optional Python Modules:")
    optional_modules = [
        ("httpx", "httpx"),
        ("structlog", "structlog"),
    ]

    for module, package in optional_modules:
        success, msg = check_import(module, package)
        print(msg)
        if success:
            checks_passed += 1

    # Check environment variables
    print("\n🔑 Environment Variables:")
    required_vars = ["OPENROUTER_API_KEY", "GROQ_API_KEY", "GEMINI_API_KEY"]
    for var in required_vars:
        success, msg = check_env_var(var)
        print(msg)
        if success:
            checks_passed += 1
        else:
            checks_failed += 1

    # Check optional variables
    print("\n🔑 Optional Environment Variables:")
    optional_vars = [
        "GITHUB_TOKEN",
        "NETLIFY_TOKEN",
        "SUPABASE_URL",
        "NEON_API_KEY",
    ]
    for var in optional_vars:
        success, msg = check_env_var(var)
        print(msg)
        if success:
            checks_passed += 1

    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  Passed: {checks_passed}")
    print(f"  Failed: {checks_failed}")
    print("=" * 60)

    if checks_failed == 0:
        print("\n✅ All checks passed! You're ready to go!")
        return 0
    else:
        print(f"\n⚠️  {checks_failed} check(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
