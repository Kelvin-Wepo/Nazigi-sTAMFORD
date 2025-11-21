# Production-grade Dockerfile for Nazigi Stamford Bus SMS Service
# Based on Python 3.10 slim image for smaller size

FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies required by psycopg2 and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose port (Render will override with $PORT)
EXPOSE 5000

# Health check (optional but recommended)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:${PORT:-5000}/')" || exit 1

# Run Gunicorn with production settings
# Render will set $PORT environment variable
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} \
             --workers 4 \
             --threads 2 \
             --timeout 120 \
             --access-logfile - \
             --error-logfile - \
             --log-level info \
             wsgi:app
