# Enterprise Nephrology AI Agent - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Enterprise Nephrology AI Agent in production environments. The system is designed for scalability, security, and high availability.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Configuration](#configuration)
4. [Deployment Options](#deployment-options)
5. [Security Configuration](#security-configuration)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Backup and Recovery](#backup-and-recovery)
8. [Scaling and Performance](#scaling-and-performance)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance](#maintenance)

## Prerequisites

### System Requirements

**Minimum Requirements:**
- CPU: 4 cores (2.4 GHz)
- RAM: 8 GB
- Storage: 100 GB SSD
- Network: 1 Gbps

**Recommended Requirements:**
- CPU: 8 cores (3.0 GHz)
- RAM: 16 GB
- Storage: 500 GB NVMe SSD
- Network: 10 Gbps

**Enterprise Requirements:**
- CPU: 16+ cores (3.2 GHz)
- RAM: 32+ GB
- Storage: 1+ TB NVMe SSD (RAID 10)
- Network: 10+ Gbps (redundant)

### Software Dependencies

- Docker 24.0+
- Docker Compose 2.20+
- Git 2.30+
- OpenSSL 1.1.1+
- Python 3.11+ (for development)

### Cloud Platform Support

- AWS (EC2, ECS, EKS)
- Google Cloud Platform (Compute Engine, GKE)
- Microsoft Azure (Virtual Machines, AKS)
- DigitalOcean (Droplets, Kubernetes)
- On-premises (VMware, Hyper-V, KVM)

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/nephroai/enterprise.git
cd enterprise/nephrology_agent
```

### 2. Environment Variables

Create a `.env` file with the following variables:

```bash
# Application Configuration
ENVIRONMENT=production
APP_NAME="Enterprise Nephrology AI Agent"
APP_VERSION=2.0.0
DEBUG=false
LOG_LEVEL=INFO

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional

# Security
JWT_SECRET_KEY=your_jwt_secret_key_here_minimum_32_characters
ENCRYPTION_KEY=your_encryption_key_here_32_bytes_base64
SECRET_KEY=your_django_secret_key_here

# Database Configuration
DATABASE_URL=postgresql://nephroai:password@postgres:5432/nephroai
REDIS_URL=redis://:password@redis:6379/0
REDIS_PASSWORD=your_redis_password_here
POSTGRES_PASSWORD=your_postgres_password_here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
NOTIFICATION_EMAIL=notifications@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
GRAFANA_PASSWORD=your_grafana_password_here

# Celery Configuration
FLOWER_USERNAME=admin
FLOWER_PASSWORD=your_flower_password_here

# Backup Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
S3_BACKUP_BUCKET=nephroai-backups

# SSL Configuration
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_PATH=/app/uploads

# Session Configuration
SESSION_TIMEOUT=86400  # 24 hours
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true

# CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_AUDIT_LOGGING=true
ENABLE_RATE_LIMITING=true
ENABLE_CACHING=true
ENABLE_COMPRESSION=true
```

### 3. SSL Certificate Setup

#### Option A: Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Copy certificates to Docker volume
sudo mkdir -p ./docker/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./docker/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./docker/ssl/key.pem
```

#### Option B: Self-Signed Certificate (Development)

```bash
mkdir -p ./docker/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ./docker/ssl/key.pem \
  -out ./docker/ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

## Configuration

### 1. Nginx Configuration

Create `docker/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream nephroai_backend {
        server nephroai-app:8000;
    }
    
    upstream nephroai_frontend {
        server nephroai-app:8501;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;
        
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
        
        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://nephroai_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Authentication endpoints
        location /auth/ {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://nephroai_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        # Streamlit frontend
        location / {
            proxy_pass http://nephroai_frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
        
        # Health check
        location /health {
            proxy_pass http://nephroai_backend/health;
            access_log off;
        }
        
        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 2. Supervisor Configuration

Create `docker/supervisord.conf`:

```ini
[supervisord]
nodaemon=true
user=nephroai
logfile=/var/log/nephroai/supervisord.log
pidfile=/var/run/nephroai/supervisord.pid

[program:fastapi]
command=uvicorn nephro_api_enterprise:app --host 0.0.0.0 --port 8000 --workers 4
directory=/app
user=nephroai
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/nephroai/fastapi.log

[program:streamlit]
command=streamlit run nephro_agent_enterprise.py --server.port 8501 --server.address 0.0.0.0
directory=/app
user=nephroai
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/nephroai/streamlit.log

[program:nginx]
command=nginx -g "daemon off;"
user=root
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/nephroai/nginx.log
```

## Deployment Options

### Option 1: Docker Compose (Recommended for Single Server)

```bash
# Create required directories
mkdir -p data logs uploads backups

# Set permissions
chmod 755 data logs uploads backups

# Deploy the stack
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f nephroai-app
```

### Option 2: Kubernetes Deployment

#### Prerequisites
- Kubernetes cluster (1.25+)
- kubectl configured
- Helm 3.0+

#### Deploy with Helm

```bash
# Add Helm repository
helm repo add nephroai https://charts.nephroai.com
helm repo update

# Create namespace
kubectl create namespace nephroai

# Deploy with Helm
helm install nephroai nephroai/enterprise \
  --namespace nephroai \
  --set image.tag=2.0.0 \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=yourdomain.com \
  --set postgresql.enabled=true \
  --set redis.enabled=true
```

#### Manual Kubernetes Deployment

```yaml
# kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nephroai
---
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nephroai-app
  namespace: nephroai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nephroai-app
  template:
    metadata:
      labels:
        app: nephroai-app
    spec:
      containers:
      - name: nephroai
        image: nephroai/enterprise:2.0.0
        ports:
        - containerPort: 8000
        - containerPort: 8501
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: nephroai-secrets
              key: gemini-api-key
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Option 3: AWS ECS Deployment

```bash
# Install AWS CLI and ECS CLI
pip install awscli ecs-cli

# Configure AWS credentials
aws configure

# Create ECS cluster
ecs-cli configure --cluster nephroai-cluster --region us-east-1
ecs-cli up --keypair your-keypair --capability-iam --size 2 --instance-type t3.large

# Deploy services
ecs-cli compose --file docker-compose.yml service up
```

## Security Configuration

### 1. Firewall Rules

```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw deny 8000/tcp   # Block direct API access
sudo ufw deny 8501/tcp   # Block direct Streamlit access
```

### 2. Security Hardening

#### Docker Security

```bash
# Run containers as non-root
# Enable user namespaces
echo '{"userns-remap": "default"}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker

# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1
```

#### System Security

```bash
# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Enable fail2ban
sudo apt-get install fail2ban
sudo systemctl enable fail2ban

# Configure automatic security updates
sudo apt-get install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. Data Encryption

#### Database Encryption

```sql
-- Enable PostgreSQL encryption
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/etc/ssl/certs/server.crt';
ALTER SYSTEM SET ssl_key_file = '/etc/ssl/private/server.key';
SELECT pg_reload_conf();
```

#### File System Encryption

```bash
# Encrypt data volumes
sudo cryptsetup luksFormat /dev/sdb
sudo cryptsetup luksOpen /dev/sdb nephroai_data
sudo mkfs.ext4 /dev/mapper/nephroai_data
sudo mount /dev/mapper/nephroai_data /opt/nephroai/data
```

## Monitoring and Logging

### 1. Prometheus Metrics

Create `docker/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'nephroai-app'
    static_configs:
      - targets: ['nephroai-app:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
    
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
      
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
      
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:80']
```

### 2. Grafana Dashboards

Import pre-built dashboards:
- System Overview (ID: 1860)
- Docker Monitoring (ID: 893)
- PostgreSQL Database (ID: 9628)
- Redis Monitoring (ID: 763)

### 3. Log Aggregation

#### ELK Stack Configuration

Create `docker/logstash/pipeline/logstash.conf`:

```ruby
input {
  beats {
    port => 5044
  }
  
  tcp {
    port => 5000
    codec => json
  }
}

filter {
  if [fields][service] == "nephroai" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
    }
    
    date {
      match => [ "timestamp", "ISO8601" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "nephroai-logs-%{+YYYY.MM.dd}"
  }
  
  stdout {
    codec => rubydebug
  }
}
```

## Backup and Recovery

### 1. Automated Backup Script

Create `docker/backup.sh`:

```bash
#!/bin/bash

set -e

# Configuration
BACKUP_DIR="/backup/output"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Database backup
echo "Starting database backup..."
pg_dump -h postgres -U nephroai -d nephroai > "$BACKUP_DIR/database_$DATE.sql"

# File system backup
echo "Starting file system backup..."
tar -czf "$BACKUP_DIR/files_$DATE.tar.gz" -C /backup/data .

# Upload to S3
if [ -n "$S3_BUCKET" ]; then
    echo "Uploading to S3..."
    aws s3 cp "$BACKUP_DIR/database_$DATE.sql" "s3://$S3_BUCKET/backups/"
    aws s3 cp "$BACKUP_DIR/files_$DATE.tar.gz" "s3://$S3_BUCKET/backups/"
fi

# Cleanup old backups
echo "Cleaning up old backups..."
find "$BACKUP_DIR" -name "*.sql" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed successfully"
```

### 2. Recovery Procedures

#### Database Recovery

```bash
# Stop application
docker-compose stop nephroai-app

# Restore database
docker-compose exec postgres psql -U nephroai -d nephroai < backup_file.sql

# Start application
docker-compose start nephroai-app
```

#### Full System Recovery

```bash
# Restore from S3
aws s3 sync s3://your-backup-bucket/backups/ ./backups/

# Restore database
docker-compose exec postgres psql -U nephroai -d nephroai < backups/database_latest.sql

# Restore files
tar -xzf backups/files_latest.tar.gz -C ./data/

# Restart services
docker-compose restart
```

## Scaling and Performance

### 1. Horizontal Scaling

#### Load Balancer Configuration

```nginx
upstream nephroai_backend {
    least_conn;
    server nephroai-app-1:8000 weight=1 max_fails=3 fail_timeout=30s;
    server nephroai-app-2:8000 weight=1 max_fails=3 fail_timeout=30s;
    server nephroai-app-3:8000 weight=1 max_fails=3 fail_timeout=30s;
}
```

#### Auto Scaling with Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml nephroai

# Scale services
docker service scale nephroai_nephroai-app=5
```

### 2. Performance Optimization

#### Database Optimization

```sql
-- PostgreSQL configuration
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
SELECT pg_reload_conf();
```

#### Redis Optimization

```redis
# Redis configuration
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

#### Application Optimization

```python
# Enable connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

## Troubleshooting

### Common Issues

#### 1. Application Won't Start

```bash
# Check logs
docker-compose logs nephroai-app

# Check environment variables
docker-compose exec nephroai-app env | grep -E "GEMINI|DATABASE"

# Test database connection
docker-compose exec nephroai-app python -c "import psycopg2; print('DB OK')"
```

#### 2. High Memory Usage

```bash
# Monitor memory usage
docker stats

# Check for memory leaks
docker-compose exec nephroai-app python -m memory_profiler app.py

# Restart services
docker-compose restart
```

#### 3. SSL Certificate Issues

```bash
# Check certificate validity
openssl x509 -in ./docker/ssl/cert.pem -text -noout

# Test SSL connection
openssl s_client -connect yourdomain.com:443

# Renew Let's Encrypt certificate
sudo certbot renew
```

### Performance Issues

#### 1. Slow API Responses

```bash
# Enable query logging
echo "log_statement = 'all'" >> postgresql.conf

# Analyze slow queries
SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC;

# Check Redis performance
redis-cli --latency-history
```

#### 2. High CPU Usage

```bash
# Profile application
docker-compose exec nephroai-app py-spy top --pid 1

# Check system resources
top -p $(docker-compose ps -q)

# Scale horizontally
docker-compose up --scale nephroai-app=3
```

## Maintenance

### Regular Maintenance Tasks

#### Daily
- Monitor system health
- Check error logs
- Verify backup completion
- Review security alerts

#### Weekly
- Update security patches
- Analyze performance metrics
- Clean up old logs
- Test disaster recovery

#### Monthly
- Update dependencies
- Review access logs
- Optimize database
- Security audit

### Maintenance Scripts

#### System Health Check

```bash
#!/bin/bash
# health_check.sh

echo "=== System Health Check ==="

# Check disk space
df -h | grep -E "(Filesystem|/dev/)"

# Check memory usage
free -h

# Check Docker containers
docker-compose ps

# Check application health
curl -f http://localhost/health || echo "Health check failed"

# Check database connection
docker-compose exec postgres pg_isready -U nephroai

# Check Redis
docker-compose exec redis redis-cli ping

echo "Health check completed"
```

#### Log Cleanup

```bash
#!/bin/bash
# cleanup_logs.sh

LOG_DIR="./logs"
RETENTION_DAYS=7

echo "Cleaning up logs older than $RETENTION_DAYS days..."

find "$LOG_DIR" -name "*.log" -mtime +$RETENTION_DAYS -delete
find "$LOG_DIR" -name "*.log.*" -mtime +$RETENTION_DAYS -delete

# Rotate current logs
docker-compose exec nephroai-app logrotate /etc/logrotate.conf

echo "Log cleanup completed"
```

### Update Procedures

#### Application Updates

```bash
# Pull latest changes
git pull origin main

# Backup current state
./docker/backup.sh

# Build new image
docker-compose build nephroai-app

# Rolling update
docker-compose up -d --no-deps nephroai-app

# Verify deployment
curl -f http://localhost/health
```

#### Security Updates

```bash
# Update base images
docker-compose pull

# Rebuild with security patches
docker-compose build --no-cache

# Deploy updates
docker-compose up -d

# Verify security
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image nephroai/enterprise:latest
```

## Support and Documentation

### Getting Help

- **Documentation**: https://docs.nephroai.com
- **Support Email**: support@nephroai.com
- **Emergency Contact**: emergency@nephroai.com
- **GitHub Issues**: https://github.com/nephroai/enterprise/issues

### Additional Resources

- [API Documentation](https://api.nephroai.com/docs)
- [User Guide](https://docs.nephroai.com/user-guide)
- [Developer Guide](https://docs.nephroai.com/developer-guide)
- [Security Best Practices](https://docs.nephroai.com/security)
- [Performance Tuning](https://docs.nephroai.com/performance)

---

**Note**: This deployment guide is for the Enterprise version of the Nephrology AI Agent. For community edition deployment, please refer to the standard README.md file.

**Security Notice**: Always follow your organization's security policies and compliance requirements when deploying in production environments. Regular security audits and penetration testing are recommended.

**Disclaimer**: This software is for educational and research purposes. Always consult with qualified healthcare professionals for medical decisions.