# Use official Python image
FROM python:3.10-slim

# Set metadata
LABEL maintainer="Singularity AGI"
LABEL description="Production-ready backend for Singularity AGI Full-Stack AI App Builder"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000 \
    ENVIRONMENT=production \
    LOG_LEVEL=INFO

# Install build essentials and system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy application code
COPY --chown=appuser:appuser . .

# Create output directory with proper permissions
RUN mkdir -p /app/output && \
    mkdir -p /app/logs && \
    chown -R appuser:appuser /app/output /app/logs

# Switch to non-root user
USER appuser

# Health check with better error handling
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Expose port
EXPOSE 8000

# Start the FastAPI server with production configuration
# Using gunicorn for production with uvicorn workers
CMD ["gunicorn", "api:app", \
     "--workers", "1", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "300", \
     "--keepalive", "5", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
