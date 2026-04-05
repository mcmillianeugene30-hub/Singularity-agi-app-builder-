# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install build essentials for psycopg2 and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy all platform files
COPY . .

# Expose the port (Render provides $PORT)
ENV PORT=8000
EXPOSE $PORT

# Start the FastAPI server
CMD ["python", "api.py"]
