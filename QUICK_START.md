# ∞ INFINITE SERVER26 - Quick Start Guide

**Version 26.1 - FORTRESS Edition**

---

## 🚀 5-Minute Quick Start

### Step 1: Clone Repository
```bash
git clone https://github.com/NaTo1000/infinite-server26.git
cd infinite-server26
```

### Step 2: Build Everything
```bash
./run.sh all
```

### Step 3: Start Services
```bash
./run.sh start
```

### Step 4: Access Applications

- 🌐 **Web UI**: http://localhost:3000
- 🔧 **API**: http://localhost:8000
- 🐳 **Rancher**: http://localhost:8090

---

## 📱 Frontend Applications

### Web Dashboard (Browser)
```bash
cd frontend/web-ui
npm install
npm start
# Opens at http://localhost:3000
```

### macOS Desktop App
```bash
cd frontend/desktop-swiftui
open InfiniteServer26.xcodeproj
# Build and run in Xcode
```

### Android Mobile App
```bash
cd frontend/android-app
./gradlew assembleRelease
# APK: app/build/outputs/apk/release/app-release.apk
```

---

## 🔨 Build Commands

| Command | Description |
|---------|-------------|
| `./run.sh all` | Build everything |
| `./run.sh docker` | Build Docker images |
| `./run.sh web` | Build Web UI |
| `./run.sh swiftui` | Build macOS app |
| `./run.sh android` | Build Android app |
| `./run.sh test` | Run all tests |

---

## 🐳 Docker Commands

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose build --no-cache
```

---

## ☸️ Kubernetes Commands

```bash
# Deploy
kubectl apply -f k8s/

# Check status
kubectl get all -n infinite-server26

# View logs
kubectl logs -n infinite-server26 -l app=infinite-server26 -f

# Port forward
kubectl port-forward -n infinite-server26 svc/infinite-server26-service 8000:8000
```

---

## 🧪 Testing

```bash
# Run all tests
./run.sh test

# Python tests
pytest

# Web UI tests
cd frontend/web-ui && npm test

# Android tests
cd frontend/android-app && ./gradlew test
```

---

## 📊 Monitoring

```bash
# Check health
./run.sh health

# View system status
curl http://localhost:8000/health

# Docker stats
docker stats

# Kubernetes metrics
kubectl top pods -n infinite-server26
```

---

## 🔧 Troubleshooting

### Services not starting?
```bash
# Check Docker
docker ps

# Check logs
docker logs infinite-fortress

# Restart services
./run.sh restart
```

### Build failing?
```bash
# Clean and rebuild
./run.sh clean
./run.sh all
```

### Port already in use?
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Main documentation |
| [UI_WORKFLOW_DOCUMENTATION.md](UI_WORKFLOW_DOCUMENTATION.md) | Complete UI guide |
| [BUILD_GUIDE.md](BUILD_GUIDE.md) | Build instructions |
| [k8s/README.md](k8s/README.md) | Kubernetes guide |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Implementation details |

---

## 🎯 Common Tasks

### Update Code
```bash
git pull origin main
./run.sh all
./run.sh restart
```

### Deploy to Production
```bash
./run.sh all
docker push nato1000/infinite-server26:latest
kubectl apply -f k8s/
```

### Add New Feature
```bash
# Create branch
git checkout -b feature/new-feature

# Make changes
# ... edit files ...

# Test
./run.sh test

# Build
./run.sh all

# Commit
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

---

## 💡 Tips

- Use `./run.sh help` to see all commands
- Check logs in `logs/` directory
- Use Docker Compose for development
- Use Kubernetes for production
- Enable hot reload in Web UI: `npm start`
- Read documentation for details

---

## 🆘 Need Help?

1. Check documentation
2. Review logs
3. Search GitHub Issues
4. Create new issue with details

---

## 📞 Support

- **GitHub**: https://github.com/NaTo1000/infinite-server26
- **Issues**: Report bugs and request features

---

**Built with ❤️ by NaTo1000**  
**Version 26.1 - FORTRESS Edition**
