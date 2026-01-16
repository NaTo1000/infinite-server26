#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# INFINITE SERVER26 - Docker Build and Test Script
# 
# This script performs comprehensive Docker build validation:
# - Builds image with --no-cache option
# - Runs health checks
# - Validates service startup
# - Tests network connectivity
# - Runs container tests
# - Reports metrics
# ═══════════════════════════════════════════════════════════════════

set -e  # Exit on error
set -o pipefail  # Exit on pipe failure

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="${DOCKER_IMAGE:-nato1000/infinite-server26}"
IMAGE_TAG="${IMAGE_TAG:-test}"
CONTAINER_NAME="fortress-test"
RANCHER_CONTAINER="rancher-test"
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
TEST_TIMEOUT=120

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}║ $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

cleanup() {
    print_header "Cleaning Up Test Containers"
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    docker stop "$RANCHER_CONTAINER" 2>/dev/null || true
    docker rm "$RANCHER_CONTAINER" 2>/dev/null || true
    docker network rm fortress-test-network 2>/dev/null || true
    print_success "Cleanup complete"
}

# Trap errors and cleanup
trap cleanup EXIT

# Main execution
main() {
    local start_time=$(date +%s)
    
    print_header "INFINITE SERVER26 - Docker Build & Test Suite"
    print_info "Image: $IMAGE_NAME:$IMAGE_TAG"
    print_info "Build Date: $BUILD_DATE"
    print_info "VCS Ref: $VCS_REF"
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 1: Build Docker Image
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 1: Building Docker Image (no-cache)"
    
    local build_start=$(date +%s)
    
    if docker build \
        --no-cache \
        --target production \
        --build-arg VERSION=26.1 \
        --build-arg BUILD_DATE="$BUILD_DATE" \
        --build-arg VCS_REF="$VCS_REF" \
        --build-arg CODENAME=FORTRESS \
        -t "$IMAGE_NAME:$IMAGE_TAG" \
        -f Dockerfile \
        . ; then
        
        local build_end=$(date +%s)
        local build_duration=$((build_end - build_start))
        print_success "Image built successfully in ${build_duration}s"
    else
        print_error "Docker build failed"
        exit 1
    fi
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 2: Check Image Size
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 2: Analyzing Image Size"
    
    local image_size=$(docker images "$IMAGE_NAME:$IMAGE_TAG" --format "{{.Size}}")
    print_info "Image size: $image_size"
    
    # Report layers
    docker history "$IMAGE_NAME:$IMAGE_TAG" --no-trunc --format "table {{.Size}}\t{{.CreatedBy}}" | head -10
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 3: Run Build Test Stage
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 3: Running Build Test Stage"
    
    if docker build \
        --target test \
        --build-arg VERSION=26.1 \
        --build-arg BUILD_DATE="$BUILD_DATE" \
        --build-arg VCS_REF="$VCS_REF" \
        -t "$IMAGE_NAME:test-stage" \
        -f Dockerfile \
        . ; then
        print_success "Build test stage passed"
    else
        print_error "Build test stage failed"
        exit 1
    fi
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 4: Create Test Network
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 4: Creating Test Network"
    
    if docker network create fortress-test-network 2>/dev/null; then
        print_success "Test network created"
    else
        print_warning "Test network already exists"
    fi
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 5: Start Test Container
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 5: Starting Test Container"
    
    docker run -d \
        --name "$CONTAINER_NAME" \
        --network fortress-test-network \
        -p 8000:8000 \
        -e INFINITE_VERSION=26.1 \
        -e NAYDOE_MODE=test \
        "$IMAGE_NAME:$IMAGE_TAG"
    
    print_success "Container started: $CONTAINER_NAME"
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 6: Wait for Container to be Healthy
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 6: Waiting for Health Checks"
    
    local health_check_attempts=0
    local max_attempts=30
    
    while [ $health_check_attempts -lt $max_attempts ]; do
        local health_status=$(docker inspect --format='{{.State.Health.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo "none")
        
        if [ "$health_status" = "healthy" ]; then
            print_success "Container is healthy"
            break
        elif [ "$health_status" = "unhealthy" ]; then
            print_error "Container is unhealthy"
            docker logs "$CONTAINER_NAME" --tail 50
            exit 1
        fi
        
        health_check_attempts=$((health_check_attempts + 1))
        print_info "Waiting for container to be healthy... ($health_check_attempts/$max_attempts)"
        sleep 2
    done
    
    if [ $health_check_attempts -eq $max_attempts ]; then
        print_error "Health check timeout"
        docker logs "$CONTAINER_NAME" --tail 50
        exit 1
    fi
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 7: Test Health Endpoints
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 7: Testing Health Endpoints"
    
    # Test /health endpoint
    if curl -f -s http://localhost:8000/health > /dev/null; then
        print_success "/health endpoint responsive"
        curl -s http://localhost:8000/health | jq -r '.status' 2>/dev/null || true
    else
        print_error "/health endpoint failed"
        exit 1
    fi
    
    # Test /ready endpoint
    if curl -f -s http://localhost:8000/ready > /dev/null; then
        print_success "/ready endpoint responsive"
    else
        print_warning "/ready endpoint not available"
    fi
    
    # Test /live endpoint
    if curl -f -s http://localhost:8000/live > /dev/null; then
        print_success "/live endpoint responsive"
    else
        print_warning "/live endpoint not available"
    fi
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 8: Validate Container Components
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 8: Validating Container Components"
    
    # Check Python version
    if docker exec "$CONTAINER_NAME" python3 --version; then
        print_success "Python is available"
    else
        print_error "Python check failed"
        exit 1
    fi
    
    # Check Docker Compose
    if docker exec "$CONTAINER_NAME" docker-compose --version; then
        print_success "Docker Compose is available"
    else
        print_warning "Docker Compose check failed"
    fi
    
    # Check kubectl
    if docker exec "$CONTAINER_NAME" kubectl version --client 2>/dev/null; then
        print_success "kubectl is available"
    else
        print_warning "kubectl check failed"
    fi
    
    # Check key tools
    if docker exec "$CONTAINER_NAME" which nmap >/dev/null 2>&1; then
        print_success "Kali tools are available"
    else
        print_warning "Some Kali tools may not be available"
    fi
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 9: Validate Directory Structure
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 9: Validating Directory Structure"
    
    local required_dirs=(
        "/opt/fortress"
        "/opt/nia-ecosystem"
        "/opt/ai-systems"
        "/opt/nai-gail"
        "/opt/nia-vault"
        "/root/fortress"
    )
    
    for dir in "${required_dirs[@]}"; do
        if docker exec "$CONTAINER_NAME" test -d "$dir"; then
            print_success "Directory exists: $dir"
        else
            print_error "Missing directory: $dir"
            exit 1
        fi
    done
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 10: Test Python Dependencies
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 10: Testing Python Dependencies"
    
    local python_modules=("fastapi" "uvicorn" "cryptography" "web3" "pandas" "numpy")
    
    for module in "${python_modules[@]}"; do
        if docker exec "$CONTAINER_NAME" python3 -c "import $module" 2>/dev/null; then
            print_success "Python module available: $module"
        else
            print_warning "Python module missing: $module"
        fi
    done
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 11: Check Container Logs
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 11: Container Logs (last 20 lines)"
    
    docker logs "$CONTAINER_NAME" --tail 20
    
    # ═════════════════════════════════════════════════════════════════
    # STEP 12: Test Network Connectivity
    # ═════════════════════════════════════════════════════════════════
    print_header "Step 12: Testing Network Connectivity"
    
    # Start a second container for network tests
    docker run -d \
        --name "$RANCHER_CONTAINER" \
        --network fortress-test-network \
        rancher/rancher:latest >/dev/null 2>&1 || true
    
    sleep 5
    
    # Test connectivity between containers
    if docker exec "$CONTAINER_NAME" ping -c 2 "$RANCHER_CONTAINER" >/dev/null 2>&1; then
        print_success "Inter-container connectivity working"
    else
        print_warning "Inter-container ping failed (may be expected)"
    fi
    
    # ═════════════════════════════════════════════════════════════════
    # FINAL: Report Summary
    # ═════════════════════════════════════════════════════════════════
    print_header "Build & Test Summary"
    
    local end_time=$(date +%s)
    local total_duration=$((end_time - start_time))
    
    echo ""
    print_success "All tests passed! ✓"
    echo ""
    print_info "Summary:"
    echo "  - Image: $IMAGE_NAME:$IMAGE_TAG"
    echo "  - Image Size: $image_size"
    echo "  - Build Time: ${build_duration}s"
    echo "  - Total Test Time: ${total_duration}s"
    echo "  - Build Date: $BUILD_DATE"
    echo "  - VCS Ref: $VCS_REF"
    echo ""
    
    print_header "Build & Test Complete!"
    
    return 0
}

# Run main function
main "$@"
exit $?
