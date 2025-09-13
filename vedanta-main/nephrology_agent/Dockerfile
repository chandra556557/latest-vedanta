# Enterprise Nephrology AI Agent - Multi-stage Docker Build
# Optimized for production deployment with security and performance

# Stage 1: Base Python image with security updates
FROM python:3.11-slim-bullseye as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Create non-root user for security
RUN groupadd -r nephroai && useradd -r -g nephroai nephroai

# Install system dependencies and security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    sqlite3 \
    libsqlite3-dev \
    nginx \
    supervisor \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies installation
FROM base as dependencies

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements_enterprise.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_enterprise.txt

# Stage 3: Application build
FROM dependencies as application

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs \
    /app/uploads \
    /app/data \
    /app/backups \
    /app/static \
    /app/templates \
    /var/log/nephroai \
    /var/run/nephroai

# Copy configuration files
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/entrypoint.sh /entrypoint.sh

# Set permissions
RUN chmod +x /entrypoint.sh && \
    chown -R nephroai:nephroai /app && \
    chown -R nephroai:nephroai /var/log/nephroai && \
    chown -R nephroai:nephroai /var/run/nephroai

# Initialize database
RUN sqlite3 /app/data/nephroai.db < database_schema.sql && \
    chown nephroai:nephroai /app/data/nephroai.db

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose ports
EXPOSE 8000 8501 80

# Switch to non-root user
USER nephroai

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

# Metadata
LABEL maintainer="NephroAI Team <team@nephroai.com>" \
      version="2.0.0" \
      description="Enterprise Nephrology AI Agent" \
      org.opencontainers.image.title="NephroAI Enterprise" \
      org.opencontainers.image.description="Advanced AI-powered nephrology consultation platform" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.vendor="NephroAI" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/nephroai/enterprise" \
      org.opencontainers.image.documentation="https://docs.nephroai.com"