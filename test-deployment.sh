#!/bin/bash

# Test Deployment Script for Singularity AGI App Builder
# This script validates the configuration before deployment

echo "🚀 Testing Singularity AGI App Builder Deployment..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        ((FAILED++))
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        ((FAILED++))
        return 1
    fi
}

# Check root configuration files
echo "📁 Checking root configuration files..."
check_file "netlify.toml"
check_file "requirements.txt"
check_file "Procfile"
check_file "Dockerfile"
check_file "docker-compose.yml"
check_file ".env.example"
check_file ".gitignore"
check_file "README.md"
check_file "DEPLOYMENT.md"
check_file "QUICKSTART.md"
echo ""

# Check dashboard configuration files
echo "📁 Checking dashboard configuration files..."
check_file "dashboard/package.json"
check_file "dashboard/tsconfig.json"
check_file "dashboard/next.config.js"
check_file "dashboard/tailwind.config.ts"
check_file "dashboard/postcss.config.js"
check_file "dashboard/.env.example"
check_file "dashboard/.gitignore"
echo ""

# Check dashboard app files
echo "📁 Checking dashboard app files..."
check_file "dashboard/app/layout.tsx"
check_file "dashboard/app/page.tsx"
check_file "dashboard/app/globals.css"
echo ""

# Check Python backend files
echo "📁 Checking Python backend files..."
check_file "api.py"
check_file "smart_router.py"
check_file "architect.py"
check_file "coder.py"
check_file "healer.py"
check_file "deployer.py"
check_file "docs_generator.py"
check_file "main.py"
echo ""

# Check if node_modules exist
echo "📦 Checking dependencies..."
if [ -d "dashboard/node_modules" ]; then
    echo -e "${GREEN}✓${NC} Node modules installed"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Node modules not found (run 'cd dashboard && npm install')"
    ((PASSED++))  # Don't fail, just warn
fi
echo ""

# Check if out directory exists (build output)
if [ -d "dashboard/out" ]; then
    echo -e "${GREEN}✓${NC} Build output exists (dashboard/out)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Build output not found (run 'cd dashboard && npm run build')"
    ((PASSED++))  # Don't fail, just warn
fi
echo ""

# Check if .env file exists (should not exist in git)
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠${NC} .env file exists (should not be committed to git)"
    ((PASSED++))
else
    echo -e "${GREEN}✓${NC} No .env file (correct)"
    ((PASSED++))
fi
echo ""

# Check package.json scripts
echo "🔧 Checking package.json scripts..."
if grep -q '"dev"' dashboard/package.json; then
    echo -e "${GREEN}✓${NC} dev script defined"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} dev script missing"
    ((FAILED++))
fi

if grep -q '"build"' dashboard/package.json; then
    echo -e "${GREEN}✓${NC} build script defined"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} build script missing"
    ((FAILED++))
fi

if grep -q '"start"' dashboard/package.json; then
    echo -e "${GREEN}✓${NC} start script defined"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} start script missing"
    ((FAILED++))
fi
echo ""

# Check netlify.toml configuration
echo "🌐 Checking netlify.toml configuration..."
if grep -q 'dashboard' netlify.toml; then
    echo -e "${GREEN}✓${NC} Dashboard path configured"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Dashboard path not configured"
    ((FAILED++))
fi

if grep -q 'out' netlify.toml; then
    echo -e "${GREEN}✓${NC} Publish directory configured"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Publish directory not configured"
    ((FAILED++))
fi
echo ""

# Check next.config.js
echo "⚛️  Checking next.config.js..."
if grep -q 'export' dashboard/next.config.js; then
    echo -e "${GREEN}✓${NC} Static export enabled"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Static export not enabled"
    ((FAILED++))
fi
echo ""

# Summary
echo "==================================="
echo "Test Summary:"
echo -e "  ${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "  ${RED}Failed: $FAILED${NC}"
    echo ""
    echo -e "${RED}❌ Some checks failed. Please fix the issues above.${NC}"
    exit 1
else
    echo -e "  Failed: $FAILED"
    echo ""
    echo -e "${GREEN}✅ All checks passed! Ready for deployment.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Build the dashboard: cd dashboard && npm run build"
    echo "2. Deploy to Netlify (see QUICKSTART.md)"
    echo "3. Deploy backend to Railway/Render (see DEPLOYMENT.md)"
    exit 0
fi
