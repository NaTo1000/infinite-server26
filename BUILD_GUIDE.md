# 🔨 INFINITE SERVER26 - Complete Build Guide

**Version 26.1 - FORTRESS Edition**

This guide walks you through building all components of Infinite Server26 from source.

---

## 📋 Prerequisites

### Required Tools

```bash
# Check versions
docker --version          # Docker 20.10+
docker-compose --version  # Docker Compose 2.0+
python3 --version         # Python 3.9+
node --version            # Node.js 18+
npm --version             # npm 9+
```

### Optional (for native apps)

```bash
# macOS development
xcodebuild -version       # Xcode 14.0+
swift --version           # Swift 5.0+

# Android development
java -version             # Java 17+
gradle --version          # Gradle 8.0+
```

### System Requirements

- **RAM**: Minimum 8GB (16GB recommended)
- **Disk**: 50GB free space
- **CPU**: 4 cores (8 cores recommended)
- **OS**: Linux, macOS, or Windows with WSL2

---

## 🚀 Quick Build (All Components)

### Using run.sh (Recommended)

```bash
# Clone repository
git clone https://github.com/NaTo1000/infinite-server26.git
cd infinite-server26

# Make run.sh executable
chmod +x run.sh

# Build everything
./run.sh all
```

This will:
1. ✅ Check dependencies
2. ✅ Build Docker images
3. ✅ Build Web UI
4. ✅ Build SwiftUI app (macOS only)
5. ✅ Build Android app
6. ✅ Run tests
7. ✅ Generate build report

Build logs are saved in `logs/` directory.

---

## 🐳 Building Docker Images

### Main Fortress Image

```bash
# Build latest
docker build -t nato1000/infinite-server26:latest .

# Build with specific version
docker build -t nato1000/infinite-server26:26.1 .

# Build with no cache
docker build --no-cache -t nato1000/infinite-server26:latest .

# Multi-platform build (requires buildx)
docker buildx build --platform linux/amd64,linux/arm64 \
  -t nato1000/infinite-server26:latest .
```

### Verify Image

```bash
# Check image size
docker images nato1000/infinite-server26

# Test image
docker run --rm nato1000/infinite-server26:latest python3 --version

# Run health check
docker run -d --name test-fortress nato1000/infinite-server26:latest
sleep 10
docker exec test-fortress curl -f http://localhost:8000/health
docker rm -f test-fortress
```

### Push to Registry

```bash
# Login to Docker Hub
docker login

# Push image
docker push nato1000/infinite-server26:latest
docker push nato1000/infinite-server26:26.1
```

---

## 🌐 Building Web UI

### Development Build

```bash
cd frontend/web-ui

# Install dependencies
npm install

# Start development server (with hot reload)
npm start
```

Access at: http://localhost:3000

### Production Build

```bash
cd frontend/web-ui

# Build for production
npm run build

# Output in build/ directory
ls -lh build/

# Test production build locally
npx serve -s build -p 3000
```

### Docker Build

```bash
cd frontend/web-ui

# Build Docker image
docker build -t infinite-web-ui:latest .

# Run container
docker run -d -p 3000:80 \
  -e REACT_APP_API_URL=http://localhost:8000 \
  infinite-web-ui:latest

# Test
curl http://localhost:3000
```

### Optimization Tips

```bash
# Analyze bundle size
npm run build -- --stats
npx webpack-bundle-analyzer build/bundle-stats.json

# Clean install
rm -rf node_modules package-lock.json
npm ci

# Update dependencies
npm update
npm audit fix
```

---

## 🖥️ Building SwiftUI Desktop App

**Platform**: macOS only

### Prerequisites

```bash
# Install Xcode from App Store
xcode-select --install

# Verify installation
xcodebuild -version
swift --version
```

### Command Line Build

```bash
cd frontend/desktop-swiftui

# Clean build
xcodebuild clean -project InfiniteServer26.xcodeproj

# Build debug
xcodebuild -project InfiniteServer26.xcodeproj \
  -scheme InfiniteServer26 \
  -configuration Debug \
  build

# Build release
xcodebuild -project InfiniteServer26.xcodeproj \
  -scheme InfiniteServer26 \
  -configuration Release \
  build

# Output location
ls -lh build/Release/
```

### Xcode GUI Build

```bash
# Open project
open InfiniteServer26.xcodeproj

# Then in Xcode:
# 1. Select scheme: InfiniteServer26
# 2. Select destination: My Mac
# 3. Product → Build (⌘B)
# 4. Product → Archive (for distribution)
```

### Create DMG Installer

```bash
# Create disk image
hdiutil create -volname "Infinite Server26" \
  -srcfolder build/Release/InfiniteServer26.app \
  -ov -format UDZO \
  InfiniteServer26.dmg
```

### Code Signing (for distribution)

```bash
# Sign app
codesign --force --deep --sign "Developer ID Application: YourName" \
  build/Release/InfiniteServer26.app

# Verify signature
codesign --verify --deep --strict --verbose=2 \
  build/Release/InfiniteServer26.app

# Notarize with Apple (required for distribution)
xcrun notarytool submit InfiniteServer26.dmg \
  --apple-id your@email.com \
  --password app-specific-password \
  --team-id TEAMID
```

---

## 📱 Building Android Application

### Prerequisites

```bash
# Install Android Studio
# Download from: https://developer.android.com/studio

# Install SDK via Android Studio SDK Manager
# Required: SDK 26+, Build Tools 34+
```

### Command Line Build

```bash
cd frontend/android-app

# Make gradlew executable
chmod +x gradlew

# Clean build
./gradlew clean

# Build debug APK
./gradlew assembleDebug

# Build release APK
./gradlew assembleRelease

# Output locations
ls -lh app/build/outputs/apk/debug/
ls -lh app/build/outputs/apk/release/
```

### Android Studio Build

```bash
# Open project
studio frontend/android-app

# Then in Android Studio:
# 1. Build → Make Project
# 2. Build → Generate Signed Bundle/APK
# 3. Follow wizard for signing
```

### Signing Release APK

Create keystore:

```bash
keytool -genkey -v -keystore infinite-server26.keystore \
  -alias infinite-server26 \
  -keyalg RSA -keysize 2048 -validity 10000
```

Sign APK:

```bash
# Using apksigner
apksigner sign --ks infinite-server26.keystore \
  --out app-release-signed.apk \
  app/build/outputs/apk/release/app-release-unsigned.apk

# Verify signature
apksigner verify app-release-signed.apk
```

### Install on Device

```bash
# Enable USB debugging on device
# Connect device via USB

# List devices
adb devices

# Install APK
adb install app/build/outputs/apk/release/app-release.apk

# Launch app
adb shell am start -n com.nato1000.infiniteserver26/.MainActivity

# View logs
adb logcat | grep InfiniteServer26
```

---

## 🧪 Running Tests

### Python Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_ai_systems.py

# Run with verbose output
pytest -v -s
```

### Web UI Tests

```bash
cd frontend/web-ui

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- Dashboard.test.js

# Update snapshots
npm test -- -u
```

### Linting

```bash
# Python
flake8 .
black --check .
mypy .

# JavaScript
cd frontend/web-ui
npm run lint
npm run format

# Kotlin (Android)
cd frontend/android-app
./gradlew ktlintCheck
```

---

## 📦 Complete Build Pipeline

### Automated Build (CI/CD)

The project includes GitHub Actions workflow for automated builds:

**.github/workflows/ui-workflow-ci.yml**

Triggers:
- Push to main/master/develop
- Pull requests
- Manual dispatch

Jobs:
1. Backend tests (Python)
2. Web UI build & tests
3. SwiftUI build (macOS)
4. Android build
5. Docker integration
6. Security scanning
7. K8s validation
8. Performance tests

### Manual Full Build

```bash
# 1. Clean everything
./run.sh clean
docker system prune -a

# 2. Install dependencies
pip install -r requirements.txt
cd frontend/web-ui && npm install && cd ../..

# 3. Build all components
./run.sh all

# 4. Run tests
./run.sh test

# 5. Start services
./run.sh start

# 6. Verify health
./run.sh health

# 7. View build report
cat logs/build-report-*.txt
```

---

## 🚀 Deployment Builds

### Production Docker Build

```bash
# Build production images
docker-compose build --no-cache

# Tag for production
docker tag nato1000/infinite-server26:latest nato1000/infinite-server26:production
docker tag nato1000/infinite-server26:latest nato1000/infinite-server26:26.1

# Push to registry
docker push nato1000/infinite-server26:production
docker push nato1000/infinite-server26:26.1
```

### Kubernetes Deployment

```bash
# Build images
./run.sh docker

# Push to registry
docker push nato1000/infinite-server26:latest

# Deploy to K8s
kubectl apply -f k8s/

# Verify deployment
kubectl get all -n infinite-server26
kubectl rollout status deployment/infinite-server26 -n infinite-server26
```

---

## 🔍 Troubleshooting

### Docker Build Issues

```bash
# Clear Docker cache
docker system prune -a

# Build with verbose output
docker build --progress=plain --no-cache .

# Check disk space
df -h
```

### Node.js Issues

```bash
# Clear npm cache
npm cache clean --force

# Delete and reinstall
rm -rf node_modules package-lock.json
npm install

# Use specific Node version
nvm use 18
```

### SwiftUI Build Issues

```bash
# Clean derived data
rm -rf ~/Library/Developer/Xcode/DerivedData

# Reset package cache
rm -rf ~/Library/Caches/org.swift.swiftpm

# Update command line tools
xcode-select --install
```

### Android Build Issues

```bash
# Clean gradle cache
rm -rf ~/.gradle/caches

# Invalidate caches in Android Studio:
# File → Invalidate Caches / Restart

# Sync gradle
./gradlew --refresh-dependencies
```

---

## 📊 Build Metrics

Typical build times (on 8-core, 16GB RAM machine):

- Docker image: ~15-20 minutes
- Web UI: ~2-3 minutes
- SwiftUI app: ~5-10 minutes
- Android app: ~3-5 minutes
- Full build: ~30-40 minutes

Artifact sizes:

- Docker image: ~3-4 GB
- Web UI build: ~2-5 MB
- SwiftUI app: ~10-20 MB
- Android APK: ~15-25 MB

---

## 📝 Build Checklist

Before release:

- [ ] Update version numbers
- [ ] Run all tests
- [ ] Update CHANGELOG.md
- [ ] Build all components
- [ ] Test each component
- [ ] Sign releases
- [ ] Create release notes
- [ ] Tag release in git
- [ ] Push to registries
- [ ] Update documentation

---

## 🆘 Getting Help

- Review logs in `logs/` directory
- Check GitHub Issues
- Read documentation
- Contact: nato1000@github.com

---

**Built with ❤️ by NaTo1000**  
**Version 26.1 - FORTRESS Edition**
