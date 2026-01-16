# Docker Quick Reference

Quick reference for common Docker operations with Infinite Server26.

## Build Commands

```bash
# Standard build
docker build -t nato1000/infinite-server26:latest .

# No-cache build
docker build --no-cache -t nato1000/infinite-server26:latest .

# Build with arguments
docker build \
  --build-arg VERSION=26.1 \
  --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  -t nato1000/infinite-server26:26.1 .

# Build specific stage
docker build --target production -t fortress:prod .
docker build --target test -t fortress:test .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t nato1000/infinite-server26:latest .
```

## Docker Compose Commands

```bash
# Start services
docker compose up -d

# Start with build
docker compose up -d --build

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Restart service
docker compose restart fortress

# View logs
docker compose logs -f
docker compose logs -f fortress
docker compose logs --tail=100 rancher

# Check status
docker compose ps

# Scale service
docker compose up -d --scale fortress=3

# Execute command
docker compose exec fortress bash
docker compose exec fortress python3 --version

# View resource usage
docker compose stats

# Validate configuration
docker compose config
```

## Container Management

```bash
# List containers
docker ps
docker ps -a

# Start/stop container
docker start fortress
docker stop fortress
docker restart fortress

# Remove container
docker rm fortress
docker rm -f fortress  # Force remove

# View logs
docker logs fortress
docker logs -f fortress
docker logs --tail=50 fortress

# Execute command
docker exec -it fortress bash
docker exec fortress python3 --version

# Inspect container
docker inspect fortress
docker inspect fortress | jq '.[0].State'
docker inspect fortress | grep -A 10 Health

# Copy files
docker cp fortress:/path/to/file ./local/path
docker cp ./local/file fortress:/path/to/dest
```

## Image Management

```bash
# List images
docker images
docker images nato1000/infinite-server26

# Remove image
docker rmi nato1000/infinite-server26:latest

# Tag image
docker tag nato1000/infinite-server26:latest nato1000/infinite-server26:26.1

# Push image
docker push nato1000/infinite-server26:latest

# Pull image
docker pull nato1000/infinite-server26:latest

# Inspect image
docker inspect nato1000/infinite-server26:latest

# View history
docker history nato1000/infinite-server26:latest

# Check image size
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## Volume Management

```bash
# List volumes
docker volume ls

# Create volume
docker volume create fortress-data

# Inspect volume
docker volume inspect infinite-fortress-data

# Remove volume
docker volume rm fortress-data

# Prune unused volumes
docker volume prune

# Backup volume
docker run --rm \
  -v infinite-fortress-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/fortress-backup.tar.gz /data

# Restore volume
docker run --rm \
  -v infinite-fortress-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/fortress-backup.tar.gz --strip 1"
```

## Network Management

```bash
# List networks
docker network ls

# Create network
docker network create fortress-network

# Inspect network
docker network inspect infinite-fortress-network

# Connect container
docker network connect fortress-network my-container

# Disconnect container
docker network disconnect fortress-network my-container

# Remove network
docker network rm fortress-network

# Prune unused networks
docker network prune
```

## Health Checks

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' fortress

# View health logs
docker inspect fortress | jq '.[0].State.Health.Log'

# Test health endpoint
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/live

# Manual health check
docker exec fortress curl -f http://localhost:8000/health
```

## Testing & Validation

```bash
# Run test script
./scripts/docker-test.sh

# Build test stage
docker build --target test -t fortress:test .

# Run tests in container
docker compose exec fortress python3 -m pytest

# Validate compose file
docker compose config --quiet

# Check syntax
docker compose config
```

## Monitoring & Stats

```bash
# View resource usage
docker stats
docker stats fortress
docker compose stats

# View processes
docker top fortress

# View events
docker events
docker events --filter 'container=fortress'

# View port mappings
docker port fortress
```

## Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything unused
docker system prune

# Remove everything including volumes
docker system prune -a --volumes
```

## Security

```bash
# Scan image
docker scan nato1000/infinite-server26:latest

# View image vulnerabilities
trivy image nato1000/infinite-server26:latest

# Run with security options
docker run -d \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  --cap-add NET_ADMIN \
  --read-only \
  --tmpfs /tmp \
  nato1000/infinite-server26:latest

# Check for updates
docker pull kalilinux/kali-rolling:latest
docker compose pull
```

## Troubleshooting

```bash
# View detailed logs
docker logs fortress 2>&1 | less

# Enter container for debugging
docker exec -it fortress bash

# Check disk usage
docker system df

# View container processes
docker exec fortress ps aux

# Check network connectivity
docker exec fortress ping -c 3 rancher
docker exec fortress curl -v http://localhost:8000/health

# Restart with clean state
docker compose down -v
docker compose up -d --force-recreate

# Check permissions
ls -la data/
docker exec fortress ls -la /opt/fortress

# View environment variables
docker exec fortress env
```

## Production Deployment

```bash
# Deploy stack (Swarm mode)
docker stack deploy -c docker-compose.yml fortress

# List services
docker service ls

# View service logs
docker service logs fortress_fortress

# Scale service
docker service scale fortress_fortress=3

# Update service
docker service update --image nato1000/infinite-server26:latest fortress_fortress

# Remove stack
docker stack rm fortress
```

## Useful Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
# Docker aliases
alias d='docker'
alias dc='docker compose'
alias dps='docker ps'
alias di='docker images'
alias dlog='docker logs -f'
alias dexec='docker exec -it'

# Fortress specific
alias fortress-up='docker compose up -d'
alias fortress-down='docker compose down'
alias fortress-logs='docker compose logs -f fortress'
alias fortress-bash='docker compose exec fortress bash'
alias fortress-health='curl http://localhost:8000/health'
alias fortress-restart='docker compose restart fortress'

# Cleanup
alias docker-clean='docker system prune -a --volumes'
alias docker-clean-containers='docker container prune -f'
alias docker-clean-images='docker image prune -a -f'
```

## Environment Setup

```bash
# Create directories
mkdir -p secrets data/{fortress,vault,rancher} logs/fortress

# Setup secrets
openssl rand -base64 32 > secrets/vault_master_key.txt
openssl rand -base64 24 > secrets/rancher_password.txt
chmod 600 secrets/*.txt

# Configure environment
cp .env.example .env
nano .env

# Set permissions
chmod 755 data/
chown -R 1000:1000 data/
```

## Debugging

```bash
# Enable debug logging
LOG_LEVEL=DEBUG docker compose up

# View container config
docker inspect fortress --format='{{json .Config}}' | jq

# Check mounts
docker inspect fortress --format='{{json .Mounts}}' | jq

# View network settings
docker inspect fortress --format='{{json .NetworkSettings}}' | jq

# Check resource limits
docker inspect fortress --format='{{json .HostConfig.Resources}}' | jq

# Test from inside container
docker exec -it fortress bash
curl http://localhost:8000/health
python3 /usr/local/bin/health-check.py 8000
```

## Performance Optimization

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Use cache
docker build --cache-from nato1000/infinite-server26:latest .

# Parallel builds
docker compose build --parallel

# Limit resources during build
docker build --memory=4g --cpu-shares=1024 .
```

---

**For complete documentation, see [DOCKER.md](DOCKER.md)**
