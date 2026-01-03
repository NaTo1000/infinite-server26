#!/bin/bash

# Infinite Server26 - Build Script for Multiple Editions
# Version: 26.2

set -e

EDITION="${1:-standard}"
VERSION="26.2"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  INFINITE SERVER26 - BUILD SCRIPT                                    ║"
echo "║  Version: ${VERSION}                                                    ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Validate edition
if [[ ! "$EDITION" =~ ^(lite|standard|enterprise)$ ]]; then
    echo "❌ Invalid edition: $EDITION"
    echo "Valid editions: lite, standard, enterprise"
    exit 1
fi

echo "🏗️  Building Infinite Server26 - ${EDITION^^} Edition"
echo ""

# Create build directory
BUILD_DIR="build/${EDITION}"
mkdir -p "$BUILD_DIR"

echo "📦 Copying core files..."
cp -r common core "$BUILD_DIR/"
cp server.py "$BUILD_DIR/"
cp LICENSE "$BUILD_DIR/"

# Copy edition-specific files
if [ "$EDITION" = "lite" ]; then
    echo "📦 Copying Lite edition files..."
    cp requirements-lite.txt "$BUILD_DIR/requirements.txt"
    cp config-lite.yaml "$BUILD_DIR/config.yaml"
elif [ "$EDITION" = "enterprise" ]; then
    echo "📦 Copying Enterprise edition files..."
    cp requirements-enterprise.txt "$BUILD_DIR/requirements.txt"
    cp config-enterprise.yaml "$BUILD_DIR/config.yaml"
    # Copy additional enterprise components
    if [ -d "plugins" ]; then
        cp -r plugins "$BUILD_DIR/"
    fi
else
    echo "📦 Copying Standard edition files..."
    cp requirements.txt "$BUILD_DIR/"
    cp config.yaml "$BUILD_DIR/"
fi

# Copy documentation
echo "📚 Copying documentation..."
cp README_V2.md "$BUILD_DIR/README.md"
cp VERSION.md "$BUILD_DIR/"
cp CHANGELOG.md "$BUILD_DIR/"

# Copy tests
echo "🧪 Copying tests..."
cp -r tests "$BUILD_DIR/"
cp run_tests.sh "$BUILD_DIR/"

# Create version file
echo "📝 Creating version file..."
cat > "$BUILD_DIR/version.txt" << EOF
Infinite Server26
Edition: ${EDITION^^}
Version: ${VERSION}-${EDITION}
Build Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Git Commit: $(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
EOF

# Create startup script
echo "📝 Creating startup script..."
cat > "$BUILD_DIR/start.sh" << EOF
#!/bin/bash
# Infinite Server26 ${EDITION^^} Edition Startup Script

echo "Starting Infinite Server26 ${EDITION^^} Edition..."
python3 server.py --edition=${EDITION}
EOF
chmod +x "$BUILD_DIR/start.sh"

# Create archive
echo "📦 Creating distribution archive..."
ARCHIVE_NAME="infinite-server26-${VERSION}-${EDITION}.tar.gz"
cd build
tar -czf "$ARCHIVE_NAME" "$EDITION"
cd ..

echo ""
echo "✅ Build complete!"
echo ""
echo "📦 Build output:"
echo "   - Directory: build/${EDITION}/"
echo "   - Archive:   build/${ARCHIVE_NAME}"
echo ""
echo "🚀 To run:"
echo "   cd build/${EDITION}"
echo "   pip install -r requirements.txt"
echo "   ./start.sh"
echo ""
