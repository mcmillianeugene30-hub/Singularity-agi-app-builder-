#!/bin/bash
# Production startup script for Singularity AGI

set -e

echo "🚀 Starting Singularity AGI Backend..."
echo "========================================"

# Load environment variables
if [ -f .env ]; then
    echo "✓ Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠ Warning: .env file not found. Using environment variables."
fi

# Check required environment variables
if [ -z "$OPENROUTER_API_KEY" ] || [ -z "$GROQ_API_KEY" ] || [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: Missing required API keys. Please check your .env file."
    exit 1
fi

# Set defaults
export PORT=${PORT:-8000}
export WORKERS=${WORKERS:-1}
export ENVIRONMENT=${ENVIRONMENT:-production}
export PYTHONUNBUFFERED=${PYTHONUNBUFFERED:-1}

echo "✓ Configuration:"
echo "  - Port: $PORT"
echo "  - Workers: $WORKERS"
echo "  - Environment: $ENVIRONMENT"
echo "========================================"

# Start the application
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🚀 Starting production server with Gunicorn..."
    exec gunicorn api:app \
        --workers $WORKERS \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind 0.0.0.0:$PORT \
        --access-logfile - \
        --error-logfile - \
        --log-level ${LOG_LEVEL:-info} \
        --timeout 120 \
        --keepalive 5 \
        --max-requests 1000 \
        --max-requests-jitter 100
else
    echo "🚀 Starting development server with Uvicorn..."
    exec uvicorn api:app \
        --host 0.0.0.0 \
        --port $PORT \
        --log-level ${LOG_LEVEL:-info} \
        --reload
fi
