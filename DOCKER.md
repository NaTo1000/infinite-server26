# ∞ INFINITE SERVER26 - Docker Documentation

**Complete Docker Guide for Building, Deploying, and Managing Infinite Server26**

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Build Options](#build-options)
5. [Docker Compose](#docker-compose)
6. [Environment Variables](#environment-variables)
7. [Secrets Management](#secrets-management)
8. [Networking](#networking)
9. [Storage & Volumes](#storage--volumes)
10. [Production Deployment](#production-deployment)
11. [Scaling](#scaling)
12. [Backup & Restore](#backup--restore)
13. [Troubleshooting](#troubleshooting)
14. [Security Best Practices](#security-best-practices)

---

## Overview

Infinite Server26 is a containerized autonomous AI-powered security fortress built on Kali Linux. The Docker configuration uses a multi-stage build process to create optimized, secure images suitable for production deployment.

### Key Features

- **Multi-stage build** - Optimized for minimal image size
- **Security hardening** - Non-root user support, minimal attack surface
- **Health checks** - Built-in health monitoring endpoints
- **OCI-compliant** - Standard container labels and metadata
- **Multi-platform** - Supports linux/amd64 and linux/arm64
- **Production-ready** - Resource limits, logging, secrets management

---

## Architecture

### Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  INFINITE SERVER26 FORTRESS                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │  NayDoeV1   │  │  JessicAi   │  │  NAi_gAil   │       │
│  │ Orchestrator│  │   Huntress  │  │ Mesh Shield │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │  NiA_Vault  │  │ Kali Tools  │  │   Health    │       │
│  │ Blockchain  │  │   Arsenal   │  │   Monitor   │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
           │                           │
           ▼                           ▼
    ┌─────────────┐           ┌─────────────┐
    │   Volumes   │           │   Network   │
    │   Storage   │           │   Bridge    │
    └─────────────┘           └─────────────┘
```

### Multi-Stage Build Process

1. **Dependencies Stage** - Builds Python virtual environment with AI/ML libraries
2. **Tools Stage** - Installs Kali tools, container orchestration tools, and NiA ecosystem
3. **Production Stage** - Creates minimal runtime image with only necessary components
4. **Test Stage** - Validates build with automated tests

---

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum (16GB recommended)
- 50GB free disk space

### Basic Build

```bash
# Clone repository
git clone https://github.com/NaTo1000/infinite-server26.git
cd infinite-server26

# Build the image
docker build -t nato1000/infinite-server26:latest .

# Run container
docker run -d \
  --name fortress \
  -p 8000:8000 \
  -p 8080:8080 \
  nato1000/infinite-server26:latest
```

### Using Docker Compose (Recommended)

```bash
# Create secrets
cp secrets/vault_master_key.txt.example secrets/vault_master_key.txt
cp secrets/rancher_password.txt.example secrets/rancher_password.txt

# Edit secrets with secure values
nano secrets/vault_master_key.txt
nano secrets/rancher_password.txt

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f fortress
```

### Verify Deployment

```bash
# Check health
curl http://localhost:8000/health

# Access Rancher dashboard
open http://localhost:8090
```

---

## Build Options

### Build Arguments

The Dockerfile supports several build arguments for customization:

| Argument | Description | Default |
|----------|-------------|---------|
| `VERSION` | Version number | 26.1 |
| `BUILD_DATE` | Build timestamp | Current time |
| `VCS_REF` | Git commit SHA | Current commit |
| `CODENAME` | Release codename | FORTRESS |

### Custom Build Example

```bash
docker build \
  --build-arg VERSION=26.2 \
  --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  --build-arg CODENAME=GUARDIAN \
  -t nato1000/infinite-server26:26.2 \
  .
```

### Build Targets

Build specific stages for different purposes:

```bash
# Production build (default)
docker build --target production -t fortress:prod .

# Test build (includes validation tests)
docker build --target test -t fortress:test .

# Dependencies only (for development)
docker build --target dependencies -t fortress:deps .

# Tools stage (includes all Kali tools)
docker build --target tools -t fortress:tools .
```

### Multi-Platform Build

```bash
# Build for multiple architectures
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg VERSION=26.1 \
  -t nato1000/infinite-server26:latest \
  --push \
  .
```

### Build Performance

```bash
# Use cache from previous builds
docker build --cache-from nato1000/infinite-server26:latest .

# Disable cache for clean build
docker build --no-cache -t fortress:clean .

# Use BuildKit for improved performance
DOCKER_BUILDKIT=1 docker build -t fortress:latest .
```

---

## Docker Compose

### Service Configuration

The docker-compose.yml defines two main services:

#### Fortress Service

Main application container with:
- Resource limits (4 CPU, 8GB RAM)
- Health checks every 30s
- Persistent volumes for data/logs
- Secrets management
- Custom network

#### Rancher Service

Container orchestration dashboard with:
- Resource limits (2 CPU, 4GB RAM)
- Persistent data volume
- Dedicated ports (8090:80, 8444:443)
- Health monitoring

### Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart specific service
docker-compose restart fortress

# View logs
docker-compose logs -f fortress
docker-compose logs --tail=100 rancher

# Scale services (if supported)
docker-compose up -d --scale fortress=2

# Execute commands in container
docker-compose exec fortress bash
docker-compose exec fortress python3 --version

# Check resource usage
docker-compose stats

# Validate configuration
docker-compose config

# Pull latest images
docker-compose pull
```

### Development vs Production

```bash
# Development with live reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production with optimizations
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Environment Variables

### Core Configuration

```bash
# Application Version
INFINITE_VERSION=26.1
CODENAME=FORTRESS

# AI Systems
NAYDOE_MODE=autonomous          # autonomous | manual | test
JESSICAI_MODE=huntress          # huntress | passive | training
NAI_GAIL_ENABLED=true           # true | false
NIA_VAULT_ACTIVE=true           # true | false

# Security Settings
SECURITY_LEVEL=maximum          # maximum | high | medium | low
MERCY_MODE=disabled             # disabled | enabled
AUTO_DEFENSE_ENABLED=true       # true | false
THREAT_RESPONSE=immediate       # immediate | delayed | manual
```

### Network Configuration

```bash
# Fortress Service
FORTRESS_IP=0.0.0.0
FORTRESS_PORT=8000
FORTRESS_API_PORT=8080
FORTRESS_HTTPS_PORT=8443

# Rancher Service
RANCHER_HTTP_PORT=8090
RANCHER_HTTPS_PORT=8444
RANCHER_PASSWORD=<secure-password>
```

### Storage Paths

```bash
# Volume mount points
FORTRESS_DATA_PATH=./data/fortress
VAULT_STORAGE_PATH=./data/vault
FORTRESS_LOGS_PATH=./logs/fortress
RANCHER_DATA_PATH=./data/rancher
```

### Secrets

```bash
# Secret file paths
VAULT_MASTER_KEY_FILE=./secrets/vault_master_key.txt
RANCHER_PASSWORD_FILE=./secrets/rancher_password.txt
```

### Optional Configuration

```bash
# Mesh Shield
SHIELD_RADIUS=100               # meters
MESH_NETWORK_SSID=NAi_gAil_Shield
MESH_NETWORK_PASSWORD=<secure-password>

# Blockchain
BLOCKCHAIN_CHAINS=3             # number of parallel chains
MINING_DIFFICULTY=4             # 1-10 scale
SYNC_INTERVAL=300               # seconds

# API Keys (if using external services)
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>

# Logging
LOG_LEVEL=INFO                  # DEBUG | INFO | WARNING | ERROR
LOG_RETENTION_DAYS=30

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
```

---

## Secrets Management

### Creating Secrets

```bash
# Create secrets directory
mkdir -p secrets

# Generate secure random passwords
openssl rand -base64 32 > secrets/vault_master_key.txt
openssl rand -base64 24 > secrets/rancher_password.txt

# Set restrictive permissions
chmod 600 secrets/*.txt
```

### Docker Secrets (Swarm Mode)

```bash
# Create Docker secrets
echo "your_vault_key" | docker secret create vault_master_key -
echo "your_rancher_pass" | docker secret create rancher_password -

# Deploy with secrets
docker stack deploy -c docker-compose.yml fortress
```

### Environment File Secrets

```bash
# Use .env file for non-sensitive configuration
cp .env.example .env

# Edit with your values
nano .env

# Ensure .env is in .gitignore
echo ".env" >> .gitignore
```

---

## Networking

### Bridge Network

The default configuration creates a custom bridge network:

```yaml
networks:
  fortress-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.26.0.0/16
          gateway: 172.26.0.1
```

### Network Commands

```bash
# Inspect network
docker network inspect infinite-fortress-network

# Connect additional container
docker network connect fortress-network my-container

# View network traffic
docker network ls
```

### Port Mapping

| Service | Internal Port | External Port | Purpose |
|---------|--------------|---------------|---------|
| Fortress | 8000 | 8000 | Health check / API |
| Fortress | 8080 | 8080 | Application API |
| Fortress | 8443 | 8443 | HTTPS API |
| Rancher | 80 | 8090 | HTTP Dashboard |
| Rancher | 443 | 8444 | HTTPS Dashboard |

### Firewall Configuration

```bash
# Allow required ports
ufw allow 8000/tcp comment "Fortress Health"
ufw allow 8080/tcp comment "Fortress API"
ufw allow 8090/tcp comment "Rancher HTTP"
ufw allow 8444/tcp comment "Rancher HTTPS"

# Or use docker-compose port mapping and firewall rules
iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

---

## Storage & Volumes

### Volume Types

1. **Fortress Data** - Application data and configuration
2. **Vault Storage** - Encrypted blockchain storage
3. **Fortress Logs** - Application logs
4. **Rancher Data** - Rancher management data

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect infinite-fortress-data

# Backup volume
docker run --rm \
  -v infinite-fortress-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/fortress-data-backup.tar.gz /data

# Restore volume
docker run --rm \
  -v infinite-fortress-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/fortress-data-backup.tar.gz --strip 1"

# Remove unused volumes
docker volume prune
```

### Bind Mounts vs Named Volumes

The docker-compose.yml uses bind mounts for easier backup:

```yaml
volumes:
  fortress-data:
    driver_opts:
      type: none
      o: bind
      device: ./data/fortress
```

To use named volumes instead:

```yaml
volumes:
  fortress-data:
    driver: local
```

---

## Production Deployment

### Pre-deployment Checklist

- [ ] Review and secure all environment variables
- [ ] Generate strong secrets for vault and Rancher
- [ ] Configure resource limits based on server capacity
- [ ] Set up log rotation and retention
- [ ] Enable firewall rules for exposed ports
- [ ] Configure backup schedule
- [ ] Test health checks and monitoring
- [ ] Review security scan results
- [ ] Document recovery procedures

### Production Configuration

```bash
# Set production environment
export COMPOSE_FILE=docker-compose.yml
export COMPOSE_PROJECT_NAME=infinite-production

# Use production env file
cp .env.production .env

# Deploy with resource limits
docker-compose up -d

# Verify deployment
./scripts/docker-test.sh
```

### Resource Limits

Adjust based on your server:

```yaml
services:
  fortress:
    deploy:
      resources:
        limits:
          cpus: '8.0'      # Adjust for your CPU
          memory: 16G      # Adjust for your RAM
        reservations:
          cpus: '4.0'
          memory: 8G
```

### High Availability Setup

For production HA deployment:

```bash
# Initialize Docker Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml fortress

# Scale services
docker service scale fortress_fortress=3

# Update service (rolling update)
docker service update --image nato1000/infinite-server26:latest fortress_fortress
```

### Load Balancing

```nginx
# Nginx load balancer configuration
upstream fortress_backend {
    least_conn;
    server 172.26.0.10:8000;
    server 172.26.0.11:8000;
    server 172.26.0.12:8000;
}

server {
    listen 80;
    server_name fortress.example.com;
    
    location / {
        proxy_pass http://fortress_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Scaling

### Horizontal Scaling

```bash
# Scale fortress service
docker-compose up -d --scale fortress=3

# Verify scaling
docker-compose ps

# Monitor load distribution
docker stats
```

### Vertical Scaling

```bash
# Update resource limits in docker-compose.yml
nano docker-compose.yml

# Restart with new limits
docker-compose up -d --force-recreate
```

### Auto-scaling with Kubernetes

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fortress-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fortress
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Backup & Restore

### Automated Backup Script

```bash
#!/bin/bash
# backup-fortress.sh

BACKUP_DIR="/var/backups/fortress"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup volumes
docker run --rm \
  -v infinite-fortress-data:/data \
  -v infinite-vault-storage:/vault \
  -v "$BACKUP_DIR":/backup \
  alpine tar czf "/backup/fortress-$TIMESTAMP.tar.gz" /data /vault

# Backup configurations
tar czf "$BACKUP_DIR/config-$TIMESTAMP.tar.gz" \
  docker-compose.yml \
  .env \
  secrets/

# Keep only last 7 backups
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/fortress-$TIMESTAMP.tar.gz"
```

### Restore Procedure

```bash
#!/bin/bash
# restore-fortress.sh

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup-file>"
    exit 1
fi

# Stop services
docker-compose down

# Restore volumes
docker run --rm \
  -v infinite-fortress-data:/data \
  -v infinite-vault-storage:/vault \
  -v $(dirname "$BACKUP_FILE"):/backup \
  alpine sh -c "cd / && tar xzf /backup/$(basename "$BACKUP_FILE")"

# Restore configurations
tar xzf "config-*.tar.gz"

# Start services
docker-compose up -d

echo "Restore completed from: $BACKUP_FILE"
```

### Schedule Backups

```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /opt/infinite-server26/backup-fortress.sh
```

---

## Troubleshooting

### Common Issues

#### Container Won't Start

```bash
# Check logs
docker-compose logs fortress

# Check resource usage
docker stats

# Verify configuration
docker-compose config

# Try recreating
docker-compose down
docker-compose up -d --force-recreate
```

#### Health Check Failing

```bash
# Test health endpoint manually
curl -v http://localhost:8000/health

# Check container health status
docker inspect fortress | grep -A 10 Health

# View health check logs
docker inspect fortress | jq '.[0].State.Health.Log'

# Exec into container
docker exec -it fortress bash
python3 /usr/local/bin/health-check.py 8000
```

#### Permission Issues

```bash
# Fix volume permissions
sudo chown -R 1000:1000 data/
sudo chmod -R 755 data/

# Check SELinux context (if applicable)
ls -Z data/
sudo chcon -R -t container_file_t data/
```

#### Network Issues

```bash
# Check network connectivity
docker exec fortress ping -c 3 rancher

# Inspect network
docker network inspect infinite-fortress-network

# Recreate network
docker-compose down
docker network prune
docker-compose up -d
```

#### Out of Memory

```bash
# Check memory usage
docker stats fortress

# Increase limits in docker-compose.yml
# Or reduce Python memory usage
docker exec fortress python3 -c "import sys; print(sys.getsizeof([]))"
```

### Debug Mode

```bash
# Run with debug logging
docker-compose down
LOG_LEVEL=DEBUG docker-compose up

# Or exec into running container
docker exec -it fortress bash
export LOG_LEVEL=DEBUG
python3 /opt/fortress/ai-systems/naydoe_orchestrator.py
```

### Performance Profiling

```bash
# Monitor resource usage
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Check disk I/O
docker exec fortress iostat -x 1

# Network traffic
docker exec fortress netstat -tunap
```

---

## Security Best Practices

### Image Security

1. **Use official base images** - kalilinux/kali-rolling:latest
2. **Multi-stage builds** - Reduce attack surface
3. **Run as non-root** - Where possible, use unprivileged user
4. **Regular updates** - Rebuild images with latest packages
5. **Security scanning** - Use Trivy in CI/CD pipeline

### Container Security

```bash
# Run with security options
docker run -d \
  --name fortress \
  --read-only \
  --tmpfs /tmp \
  --cap-drop ALL \
  --cap-add NET_ADMIN \
  --security-opt no-new-privileges \
  nato1000/infinite-server26:latest
```

### Network Security

```bash
# Disable inter-container communication
docker network create --internal fortress-internal

# Use custom networks
docker-compose --compatibility up -d
```

### Secrets Security

```bash
# Never commit secrets to git
echo "secrets/" >> .gitignore

# Use Docker secrets in production
docker secret create my_secret ./secret.txt

# Rotate secrets regularly
./rotate-secrets.sh
```

### Monitoring & Auditing

```bash
# Enable audit logging
docker run -d \
  --log-driver=syslog \
  --log-opt syslog-address=tcp://log-server:514 \
  fortress:latest

# Monitor security events
docker events --filter 'type=container'

# Review security scan results
docker scan nato1000/infinite-server26:latest
```

### Compliance

- **CIS Docker Benchmark** - Follow CIS recommendations
- **NIST Guidelines** - Align with NIST container security
- **Regular audits** - Perform security audits quarterly
- **Vulnerability management** - Track and remediate CVEs

---

## Additional Resources

### Documentation

- [README.md](README.md) - General overview and quick start
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment procedures
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

### Tools & Scripts

- `scripts/docker-test.sh` - Comprehensive build testing
- `.github/workflows/docker-build.yml` - CI/CD pipeline

### Support

- **GitHub Issues**: https://github.com/NaTo1000/infinite-server26/issues
- **GitHub Discussions**: https://github.com/NaTo1000/infinite-server26/discussions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 26.1 | 2025-01 | Initial Docker optimization release |

---

**Built with ❤️ by NaTo1000**  
**For the Security Community**  
**Version 26.1 | 2025**

---

*"Containerized security fortress - Deploy anywhere, defend everywhere."*
