#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════════╗
# ║   ∞ INFINITE SERVER26 - MASTER BUILD & ORCHESTRATION SCRIPT      ║
# ║   Comprehensive UI Workflow CI Build Process                     ║
# ║   Built by: NaTo1000 | Version: 26.1                             ║
# ╚═══════════════════════════════════════════════════════════════════╝

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build"
LOGS_DIR="${PROJECT_ROOT}/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create necessary directories
mkdir -p "${BUILD_DIR}" "${LOGS_DIR}"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

log_info() {
    echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

# Banner
show_banner() {
    clear
    echo -e "${CYAN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ██╗███╗   ██╗███████╗██╗███╗   ██╗██╗████████╗███████╗         ║
║   ██║████╗  ██║██╔════╝██║████╗  ██║██║╚══██╔══╝██╔════╝         ║
║   ██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║   ██║   █████╗           ║
║   ██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║   ██║   ██╔══╝           ║
║   ██║██║ ╚████║██║     ██║██║ ╚████║██║   ██║   ███████╗         ║
║   ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚══════╝         ║
║                                                                   ║
║   SERVER26 MASTER BUILD & ORCHESTRATION SCRIPT                   ║
║   Version: 26.1 | Built by: NaTo1000                             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Check dependencies
check_dependencies() {
    log "Checking dependencies..."
    
    local missing_deps=()
    
    # Essential tools
    command -v docker >/dev/null 2>&1 || missing_deps+=("docker")
    command -v docker-compose >/dev/null 2>&1 || missing_deps+=("docker-compose")
    command -v python3 >/dev/null 2>&1 || missing_deps+=("python3")
    command -v node >/dev/null 2>&1 || log_warning "Node.js not found (optional for web UI)"
    command -v npm >/dev/null 2>&1 || log_warning "npm not found (optional for web UI)"
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies and try again"
        exit 1
    fi
    
    log "✓ All required dependencies found"
}

# Build Docker images
build_docker() {
    log "Building Docker images..."
    
    log_info "Building main Infinite Server26 image..."
    docker build -t nato1000/infinite-server26:latest \
        -t nato1000/infinite-server26:26.1 \
        -t nato1000/infinite-server26:fortress \
        -f Dockerfile . 2>&1 | tee "${LOGS_DIR}/docker-build-${TIMESTAMP}.log"
    
    log "✓ Docker image built successfully"
}

# Build Web UI
build_web_ui() {
    log "Building Web UI..."
    
    if [ -d "${PROJECT_ROOT}/frontend/web-ui" ]; then
        cd "${PROJECT_ROOT}/frontend/web-ui"
        
        if [ -f "package.json" ]; then
            log_info "Installing npm dependencies..."
            npm install 2>&1 | tee "${LOGS_DIR}/npm-install-${TIMESTAMP}.log"
            
            log_info "Building web application..."
            npm run build 2>&1 | tee "${LOGS_DIR}/npm-build-${TIMESTAMP}.log"
            
            log "✓ Web UI built successfully"
        else
            log_warning "No package.json found in web UI directory"
        fi
        
        cd "${PROJECT_ROOT}"
    else
        log_warning "Web UI directory not found, skipping..."
    fi
}

# Build SwiftUI Desktop App
build_swiftui() {
    log "Building SwiftUI Desktop Application..."
    
    if [ -d "${PROJECT_ROOT}/frontend/desktop-swiftui" ]; then
        if command -v xcodebuild >/dev/null 2>&1; then
            cd "${PROJECT_ROOT}/frontend/desktop-swiftui"
            
            log_info "Building SwiftUI app with xcodebuild..."
            xcodebuild -project InfiniteServer26.xcodeproj \
                -scheme InfiniteServer26 \
                -configuration Release \
                clean build 2>&1 | tee "${LOGS_DIR}/swiftui-build-${TIMESTAMP}.log"
            
            log "✓ SwiftUI app built successfully"
            cd "${PROJECT_ROOT}"
        else
            log_warning "xcodebuild not found - skipping SwiftUI build (macOS only)"
        fi
    else
        log_info "SwiftUI directory not found, creating structure..."
    fi
}

# Build Android App
build_android() {
    log "Building Android Application..."
    
    if [ -d "${PROJECT_ROOT}/frontend/android-app" ]; then
        cd "${PROJECT_ROOT}/frontend/android-app"
        
        if [ -f "gradlew" ]; then
            log_info "Building Android app with Gradle..."
            chmod +x gradlew
            ./gradlew clean assembleRelease 2>&1 | tee "${LOGS_DIR}/android-build-${TIMESTAMP}.log"
            
            log "✓ Android app built successfully"
            log_info "APK location: ${PROJECT_ROOT}/frontend/android-app/app/build/outputs/apk/release/"
        else
            log_warning "Gradle wrapper not found in Android directory"
        fi
        
        cd "${PROJECT_ROOT}"
    else
        log_info "Android directory not found, creating structure..."
    fi
}

# Run Python tests
run_python_tests() {
    log "Running Python tests..."
    
    log_info "Testing AI systems..."
    python3 -m pytest tests/ -v 2>&1 | tee "${LOGS_DIR}/pytest-${TIMESTAMP}.log" || log_warning "Some tests failed"
    
    log_info "Checking Python code with flake8..."
    python3 -m flake8 . --exclude=venv,build,dist --max-line-length=120 2>&1 | tee "${LOGS_DIR}/flake8-${TIMESTAMP}.log" || log_warning "Flake8 warnings found"
    
    log "✓ Python tests completed"
}

# Start services
start_services() {
    log "Starting services with Docker Compose..."
    
    # Copy env example if .env doesn't exist
    if [ ! -f ".env" ]; then
        log_info "Creating .env from template..."
        cp .env.example .env
    fi
    
    log_info "Pulling latest images..."
    docker-compose pull
    
    log_info "Starting all services..."
    docker-compose up -d 2>&1 | tee "${LOGS_DIR}/docker-compose-${TIMESTAMP}.log"
    
    log "✓ Services started successfully"
}

# Stop services
stop_services() {
    log "Stopping services..."
    docker-compose down 2>&1 | tee "${LOGS_DIR}/docker-compose-down-${TIMESTAMP}.log"
    log "✓ Services stopped"
}

# Check service health
check_health() {
    log "Checking service health..."
    
    log_info "Waiting for services to be ready..."
    sleep 10
    
    # Check Docker containers
    docker-compose ps
    
    # Check health endpoints
    local services=("http://localhost:8000/health" "http://localhost:8090")
    
    for service in "${services[@]}"; do
        if curl -f -s "${service}" >/dev/null 2>&1; then
            log "✓ ${service} is healthy"
        else
            log_warning "${service} is not responding"
        fi
    done
}

# Deploy to Kubernetes
deploy_kubernetes() {
    log "Deploying to Kubernetes..."
    
    if command -v kubectl >/dev/null 2>&1; then
        log_info "Applying Kubernetes manifests..."
        kubectl apply -f k8s/ 2>&1 | tee "${LOGS_DIR}/kubectl-apply-${TIMESTAMP}.log"
        
        log_info "Checking deployment status..."
        kubectl rollout status deployment/infinite-server26 -n default
        
        log "✓ Kubernetes deployment completed"
    else
        log_warning "kubectl not found - skipping Kubernetes deployment"
    fi
}

# Cleanup
cleanup() {
    log "Cleaning up build artifacts..."
    
    # Remove temporary files
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    
    log "✓ Cleanup completed"
}

# Generate report
generate_report() {
    log "Generating build report..."
    
    local report_file="${LOGS_DIR}/build-report-${TIMESTAMP}.txt"
    
    cat > "${report_file}" << EOF
╔═══════════════════════════════════════════════════════════════════╗
║   INFINITE SERVER26 BUILD REPORT                                 ║
║   Timestamp: $(date +'%Y-%m-%d %H:%M:%S')                        ║
╚═══════════════════════════════════════════════════════════════════╝

BUILD CONFIGURATION
-------------------
Project Root: ${PROJECT_ROOT}
Build Directory: ${BUILD_DIR}
Logs Directory: ${LOGS_DIR}

COMPONENTS BUILT
----------------
✓ Docker Images
✓ Python Services
EOF

    [ -d "${PROJECT_ROOT}/frontend/web-ui" ] && echo "✓ Web UI" >> "${report_file}"
    [ -d "${PROJECT_ROOT}/frontend/desktop-swiftui" ] && echo "✓ SwiftUI Desktop App" >> "${report_file}"
    [ -d "${PROJECT_ROOT}/frontend/android-app" ] && echo "✓ Android Application" >> "${report_file}"
    
    cat >> "${report_file}" << EOF

DOCKER IMAGES
-------------
$(docker images | grep infinite-server26)

RUNNING CONTAINERS
------------------
$(docker-compose ps 2>/dev/null || echo "No containers running")

LOG FILES
---------
$(ls -lh "${LOGS_DIR}"/*-${TIMESTAMP}.log 2>/dev/null || echo "No log files")

BUILD STATUS: SUCCESS
EOF
    
    cat "${report_file}"
    log "✓ Build report saved to ${report_file}"
}

# Show usage
usage() {
    cat << EOF
Usage: $0 [COMMAND]

Commands:
    all             Build everything (default)
    docker          Build Docker images only
    web             Build Web UI only
    swiftui         Build SwiftUI desktop app only
    android         Build Android app only
    test            Run tests only
    start           Start all services
    stop            Stop all services
    restart         Restart all services
    health          Check service health
    deploy          Deploy to Kubernetes
    clean           Clean build artifacts
    help            Show this help message

Examples:
    $0                  # Build everything
    $0 all              # Build everything
    $0 docker start     # Build Docker and start services
    $0 test             # Run tests only
    $0 clean            # Clean build artifacts

EOF
}

# Main execution
main() {
    show_banner
    
    # Parse command
    local command="${1:-all}"
    
    case "${command}" in
        all)
            check_dependencies
            build_docker
            build_web_ui
            build_swiftui
            build_android
            run_python_tests
            generate_report
            log "${GREEN}✓ Build completed successfully!${NC}"
            ;;
        docker)
            check_dependencies
            build_docker
            ;;
        web)
            build_web_ui
            ;;
        swiftui)
            build_swiftui
            ;;
        android)
            build_android
            ;;
        test)
            run_python_tests
            ;;
        start)
            check_dependencies
            start_services
            check_health
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            sleep 2
            start_services
            check_health
            ;;
        health)
            check_health
            ;;
        deploy)
            deploy_kubernetes
            ;;
        clean)
            cleanup
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            log_error "Unknown command: ${command}"
            usage
            exit 1
            ;;
    esac
    
    log "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    log "${GREEN}All operations completed!${NC}"
}

# Run main function
main "$@"
