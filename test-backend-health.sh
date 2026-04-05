#!/bin/bash

# Backend Health Test Script
# Tests various endpoints of the Singularity AGI API backend

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default backend URL (can be overridden with first argument)
BACKEND_URL=${1:-"http://localhost:8000"}

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Singularity AGI Backend Health Test${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}Testing backend at: ${BACKEND_URL}${NC}"
echo ""

# Test 1: Root endpoint
echo -e "${BLUE}Test 1: Root Endpoint (/)${NC}"
echo -e "${YELLOW}Expected: API information with endpoints list${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓ Status: 200 OK${NC}"
    echo -e "${GREEN}Response:${NC}"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
else
    echo -e "${RED}✗ Status: $HTTP_CODE${NC}"
    echo -e "${RED}Response: $BODY${NC}"
fi
echo ""

# Test 2: Health endpoint
echo -e "${BLUE}Test 2: Health Endpoint (/health)${NC}"
echo -e "${YELLOW}Expected: {\"status\":\"healthy\",\"service\":\"singularity-agi-backend\"}${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/health")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓ Status: 200 OK${NC}"
    echo -e "${GREEN}Response:${NC}"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"

    # Validate response structure
    STATUS=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', ''))" 2>/dev/null)
    SERVICE=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin).get('service', ''))" 2>/dev/null)

    if [ "$STATUS" = "healthy" ] && [ "$SERVICE" = "singularity-agi-backend" ]; then
        echo -e "${GREEN}✓ Health check validated: Backend is healthy${NC}"
    else
        echo -e "${RED}✗ Health check failed: Unexpected response structure${NC}"
    fi
else
    echo -e "${RED}✗ Status: $HTTP_CODE${NC}"
    echo -e "${RED}Response: $BODY${NC}"
fi
echo ""

# Test 3: Docs endpoint (if available)
echo -e "${BLUE}Test 3: API Documentation (/docs)${NC}"
echo -e "${YELLOW}Expected: FastAPI automatic documentation${NC}"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${BACKEND_URL}/docs")

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓ Status: 200 OK${NC}"
    echo -e "${GREEN}✓ API documentation is available at: ${BACKEND_URL}/docs${NC}"
else
    echo -e "${YELLOW}⚠ Status: $HTTP_CODE${NC}"
    echo -e "${YELLOW}⚠ API documentation may not be enabled${NC}"
fi
echo ""

# Test 4: WebSocket endpoint (basic connectivity test)
echo -e "${BLUE}Test 4: WebSocket Endpoint (/ws/build)${NC}"
echo -e "${YELLOW}Expected: WebSocket upgrade supported${NC}"

if command -v wscat &> /dev/null; then
    echo -e "${GREEN}⚠ wscat found, but WebSocket requires interactive connection${NC}"
    echo -e "${YELLOW}To test WebSocket manually, run:${NC}"
    echo -e "${YELLOW}  wscat -c ${BACKEND_URL/http/ws}/ws/build${NC}"
else
    echo -e "${YELLOW}⚠ wscat not found. Install with: npm install -g wscat${NC}"
    echo -e "${YELLOW}Then test with: wscat -c ${BACKEND_URL/http/ws}/ws/build${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Backend URL: ${BACKEND_URL}${NC}"
echo -e "${GREEN}Root endpoint: ${BACKEND_URL}/${NC}"
echo -e "${GREEN}Health endpoint: ${BACKEND_URL}/health${NC}"
echo -e "${GREEN}WebSocket: ${BACKEND_URL/http/ws}/ws/build${NC}"
echo -e "${GREEN}Docs: ${BACKEND_URL}/docs${NC}"
echo ""
echo -e "${BLUE}To test a different backend:${NC}"
echo -e "${YELLOW}  ./test-backend-health.sh https://your-backend.onrender.com${NC}"
echo ""
