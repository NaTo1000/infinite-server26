# 🚀 DEPLOYMENT GUIDE - INFINITE SERVER26

Complete deployment guide for getting Infinite Server26 Fortress up and running in production.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Deploy (Recommended)](#quick-deploy-recommended)
3. [Docker Compose Deployment](#docker-compose-deployment)
4. [Manual Docker Deployment](#manual-docker-deployment)
5. [Production Deployment](#production-deployment)
6. [GitHub Actions CI/CD](#github-actions-cicd)
7. [Configuration](#configuration)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB
- OS: Linux (Ubuntu 20.04+, Debian 11+, or Kali Linux)

**Recommended:**
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 100GB+ SSD
- OS: Ubuntu 22.04 LTS or Kali Linux Rolling

### Software Requirements

```bash
# Docker
Docker Engine 20.10+
Docker Compose 2.0+

# System packages
git
curl
wget
```

### Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

---

## Quick Deploy (Recommended)

The fastest way to get started:

```bash
# Clone repository
git clone https://github.com/NaTo1000/infinite-server26.git
cd infinite-server26

# Copy and configure environment
cp .env.example .env
nano .env  # Edit with your settings

# Deploy with docker-compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f fortress
```

**Access Points:**
- Fortress Dashboard: http://localhost:8000
- Rancher Dashboard: http://localhost:8090

---

## Docker Compose Deployment

### Step 1: Clone and Configure

```bash
git clone https://github.com/NaTo1000/infinite-server26.git
cd infinite-server26
```

### Step 2: Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Important variables to set:**
```bash
RANCHER_PASSWORD=YourSecurePassword123
VAULT_MASTER_KEY=your_32_char_encryption_key_here
MESH_NETWORK_PASSWORD=SecureWiFiPassword
```

### Step 3: Deploy

```bash
# Pull latest images
docker-compose pull

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 4: Verify

```bash
# Check running containers
docker-compose ps

# Check fortress health
docker-compose exec fortress curl http://localhost:8000/health

# Access Rancher
# Open browser: http://localhost:8090
```

---

## Manual Docker Deployment

### Build from Source

```bash
# Clone repository
git clone https://github.com/NaTo1000/infinite-server26.git
cd infinite-server26

# Build image
docker build -t nato1000/infinite-server26:latest .
```

### Run Container

```bash
# Run with all features
docker run -d \
  --name infinite-fortress \
  --privileged \
  --network=host \
  --restart=unless-stopped \
  -v fortress-data:/root/fortress \
  -v vault-storage:/opt/nia-vault/storage \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e NAYDOE_MODE=autonomous \
  -e JESSICAI_MODE=huntress \
  -e SECURITY_LEVEL=maximum \
  nato1000/infinite-server26:latest
```

### Deploy Rancher Separately

```bash
docker run -d \
  --name rancher-dashboard \
  --privileged \
  --restart=unless-stopped \
  -p 8090:80 -p 8444:443 \
  -v rancher-data:/var/lib/rancher \
  rancher/rancher:latest
```

---

## Production Deployment

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
  git curl wget \
  ufw fail2ban \
  htop tmux

# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8000/tcp  # Fortress API
sudo ufw allow 8090/tcp  # Rancher
sudo ufw --force enable
```

### 2. SSL/TLS Certificates

```bash
# Install certbot
sudo apt install -y certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com
```

### 3. Systemd Service

Create `/etc/systemd/system/infinite-fortress.service`:

```ini
[Unit]
Description=Infinite Server26 Fortress
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/infinite-server26
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable infinite-fortress
sudo systemctl start infinite-fortress
sudo systemctl status infinite-fortress
```

### 4. Reverse Proxy (Nginx)

```bash
# Install Nginx
sudo apt install -y nginx

# Create config
sudo nano /etc/nginx/sites-available/fortress
```

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name rancher.your-domain.com;
    
    location / {
        proxy_pass http://localhost:8090;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/fortress /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## GitHub Actions CI/CD

### Setup GitHub Secrets

1. Go to: `Settings` → `Secrets and variables` → `Actions`
2. Add these secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token

### Workflow

The workflow automatically:
- ✅ Builds Docker image on push to main branch
- ✅ Pushes to Docker Hub with multiple tags
- ✅ Uses build cache for faster builds
- ✅ Supports manual triggers

**Trigger manually:**
1. Go to: `Actions` → `Build and Push Docker Image`
2. Click `Run workflow`

---

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

**Key configurations:**

| Variable | Description | Default |
|----------|-------------|---------|
| `RANCHER_PASSWORD` | Rancher admin password | `admin` |
| `VAULT_MASTER_KEY` | Encryption master key | - |
| `NAYDOE_MODE` | AI orchestrator mode | `autonomous` |
| `JESSICAI_MODE` | Security mode | `huntress` |
| `SECURITY_LEVEL` | Security level | `maximum` |
| `NAI_GAIL_ENABLED` | Mesh shield status | `true` |
| `SHIELD_RADIUS` | Mesh shield radius (m) | `100` |

### AI Systems

Edit AI system configurations in:
- `/opt/ai-systems/naydoe_orchestrator.py`
- `/opt/ai-systems/jessicai_huntress.py`
- `/opt/security/nai_gail_mesh_shield.py`
- `/opt/blockchain/nia_vault_blockchain.py`

---

## Verification

### 1. Check Container Status

```bash
# Using docker-compose
docker-compose ps

# Using docker
docker ps | grep fortress
```

### 2. Check Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fortress
docker-compose logs -f rancher
```

### 3. Health Checks

```bash
# Fortress health
curl http://localhost:8000/health

# Check AI systems
docker-compose exec fortress systemctl status naydoev1
docker-compose exec fortress systemctl status jessicai
```

### 4. Access Dashboards

**Fortress Dashboard:**
```bash
http://localhost:8000
```

**Rancher Dashboard:**
```bash
http://localhost:8090
# Get bootstrap password:
docker logs rancher-dashboard 2>&1 | grep "Bootstrap Password:"
```

### 5. Verify Services

```bash
# Enter fortress container
docker-compose exec fortress /bin/bash

# Check services
systemctl status naydoev1 jessicai nai-gail nia-vault

# Check logs
tail -f /var/log/naydoev1.log
tail -f /var/log/jessicai.log
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs fortress

# Check Docker status
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker
```

### Port Conflicts

```bash
# Check what's using ports
sudo netstat -tuln | grep -E ':(80|443|8000|8090)'

# Kill conflicting process
sudo kill -9 $(sudo lsof -t -i:8000)

# Or change ports in docker-compose.yml
```

### Permission Issues

```bash
# Fix volume permissions
sudo chown -R 1000:1000 fortress-data vault-storage logs

# Run with sudo (not recommended)
sudo docker-compose up -d
```

### Build Fails

```bash
# Clean Docker system
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check disk space
df -h
```

### Can't Access Rancher

```bash
# Check Rancher logs
docker logs rancher-dashboard

# Restart Rancher
docker restart rancher-dashboard

# Get bootstrap password
docker logs rancher-dashboard 2>&1 | grep "Bootstrap Password:"
```

### AI Systems Not Starting

```bash
# Enter container
docker-compose exec fortress /bin/bash

# Check service status
systemctl status naydoev1 jessicai nai-gail nia-vault

# Restart services
systemctl restart naydoev1 jessicai nai-gail nia-vault

# View error logs
journalctl -u naydoev1 -n 50
```

---

## Maintenance

### Update to Latest Version

```bash
# Pull latest image
docker-compose pull

# Restart with new image
docker-compose up -d

# Clean old images
docker image prune -a
```

### Backup

```bash
# Backup volumes
docker run --rm \
  -v fortress-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/fortress-backup-$(date +%Y%m%d).tar.gz /data

# Backup configuration
tar czf config-backup-$(date +%Y%m%d).tar.gz .env docker-compose.yml
```

### Restore

```bash
# Restore volume
docker run --rm \
  -v fortress-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd / && tar xzf /backup/fortress-backup-20240101.tar.gz"
```

---

## Support

- **Documentation**: Check `/docs` folder
- **GitHub Issues**: https://github.com/NaTo1000/infinite-server26/issues
- **Build Guide**: See [BUILD_AND_PUSH.md](BUILD_AND_PUSH.md)

---

## ⚡ Quick Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Logs
docker-compose logs -f fortress

# Update
docker-compose pull && docker-compose up -d

# Status
docker-compose ps

# Enter container
docker-compose exec fortress /bin/bash

# Cleanup
docker system prune -a
```

---

**Built by NaTo1000 | Version 26.1 | FORTRESS MODE**

*"Deploy once, defend forever."*
