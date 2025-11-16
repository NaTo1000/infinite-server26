# 🚀 BUILD AND PUSH INSTRUCTIONS

**Infinite Server26 - Docker Build & Push Guide**

This guide shows you how to build the Docker image locally and push it to Docker Hub.

---

## 📋 Prerequisites

- Docker installed and running
- Docker Hub account (nato1000)
- At least 20GB free disk space
- Good internet connection (for base image download)

---

## 🔨 Step 1: Build Docker Image

### Build the image locally:

```bash
cd infinite-server26
docker build -t nato1000/infinite-server26:latest .
```

**Build time:** 10-15 minutes  
**Image size:** ~4.5GB

### Tag with version:

```bash
docker tag nato1000/infinite-server26:latest nato1000/infinite-server26:26.1
docker tag nato1000/infinite-server26:latest nato1000/infinite-server26:fortress
```

---

## 🐳 Step 2: Push to Docker Hub

### Login to Docker Hub:

```bash
docker login -u nato1000
# Enter your Docker Hub password when prompted
```

### Push all tags:

```bash
docker push nato1000/infinite-server26:latest
docker push nato1000/infinite-server26:26.1
docker push nato1000/infinite-server26:fortress
```

**Upload time:** 15-30 minutes (depending on connection)

---

## ✅ Step 3: Verify

### Check Docker Hub:

Visit: https://hub.docker.com/r/nato1000/infinite-server26

### Test pull:

```bash
docker pull nato1000/infinite-server26:latest
```

### Test run:

```bash
docker run -d --name fortress-test \
  --privileged --network=host \
  nato1000/infinite-server26:latest
```

---

## 🎯 Quick Commands Reference

```bash
# Build
docker build -t nato1000/infinite-server26:latest .

# Tag
docker tag nato1000/infinite-server26:latest nato1000/infinite-server26:26.1

# Login
docker login -u nato1000

# Push
docker push nato1000/infinite-server26:latest

# Pull (to test)
docker pull nato1000/infinite-server26:latest

# Run
docker run -d --name fortress --privileged --network=host \
  nato1000/infinite-server26:latest
```

---

## 🔧 Troubleshooting

### Build fails with "out of space"

```bash
# Clean up Docker
docker system prune -a

# Check disk space
df -h
```

### Push fails with "denied"

```bash
# Re-login
docker logout
docker login -u nato1000
```

### Build is too slow

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t nato1000/infinite-server26:latest .
```

---

## 📝 Alternative: GitHub Actions Auto-Build

Create `.github/workflows/docker-build.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            nato1000/infinite-server26:latest
            nato1000/infinite-server26:26.1
            nato1000/infinite-server26:fortress
```

**Setup:**
1. Go to GitHub repo settings
2. Add secrets: `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`
3. Push to main branch
4. GitHub Actions will auto-build and push!

---

## ⚡ READY TO BUILD!

Follow the steps above to build and push your fortress to Docker Hub!

**Built by NaTo1000 | Version 26.1**
