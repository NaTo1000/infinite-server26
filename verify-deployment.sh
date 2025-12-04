#!/bin/bash

# ═══════════════════════════════════════════════════════════════════
# INFINITE SERVER26 - Deployment Verification Script
# ═══════════════════════════════════════════════════════════════════
# 
# Verifies that all components are running correctly
# Usage: ./verify-deployment.sh
#
# Built by: NaTo1000
# Version: 26.1
# ═══════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Counters
PASS=0
FAIL=0
WARN=0

# Banner
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   INFINITE SERVER26 - DEPLOYMENT VERIFICATION                    ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test functions
test_pass() {
    echo -e "${GREEN}[✓]${NC} $1"
    ((PASS++))
}

test_fail() {
    echo -e "${RED}[✗]${NC} $1"
    ((FAIL++))
}

test_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
    ((WARN++))
}

test_info() {
    echo -e "${BLUE}[*]${NC} $1"
}

# Check Docker
test_info "Testing Docker..."
if command -v docker &> /dev/null; then
    test_pass "Docker installed: $(docker --version | cut -d' ' -f3)"
else
    test_fail "Docker not installed"
fi

# Check Docker Compose
test_info "Testing Docker Compose..."
if command -v docker-compose &> /dev/null; then
    test_pass "Docker Compose installed: $(docker-compose --version | cut -d' ' -f3)"
else
    test_fail "Docker Compose not installed"
fi

# Check if containers are running
echo ""
test_info "Testing Container Status..."

# Check fortress container
if docker ps | grep -q "infinite-fortress"; then
    test_pass "Fortress container is running"
    
    # Check if it's healthy
    STATUS=$(docker inspect --format='{{.State.Health.Status}}' infinite-fortress 2>/dev/null || echo "unknown")
    if [ "$STATUS" = "healthy" ]; then
        test_pass "Fortress health check: healthy"
    elif [ "$STATUS" = "starting" ]; then
        test_warn "Fortress health check: starting (wait a moment)"
    else
        test_warn "Fortress health check: $STATUS"
    fi
else
    test_fail "Fortress container is not running"
fi

# Check rancher container
if docker ps | grep -q "rancher-dashboard"; then
    test_pass "Rancher container is running"
else
    test_warn "Rancher container is not running"
fi

# Check network connectivity
echo ""
test_info "Testing Network Connectivity..."

# Test localhost connection
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    test_pass "Fortress API responding on port 8000"
elif curl -sf http://localhost:8000 > /dev/null 2>&1; then
    test_pass "Fortress responding on port 8000"
else
    test_warn "Fortress not responding on port 8000 (may need time to start)"
fi

# Test Rancher
if curl -sf http://localhost:8090 > /dev/null 2>&1; then
    test_pass "Rancher responding on port 8090"
else
    test_warn "Rancher not responding on port 8090 (may need time to start)"
fi

# Check volumes
echo ""
test_info "Testing Docker Volumes..."

VOLUMES=("infinite-server26_fortress-data" "infinite-server26_vault-storage" "infinite-server26_logs" "infinite-server26_rancher-data")
for vol in "${VOLUMES[@]}"; do
    if docker volume ls | grep -q "$vol"; then
        test_pass "Volume exists: $vol"
    else
        test_warn "Volume not found: $vol"
    fi
done

# Check resources
echo ""
test_info "Testing System Resources..."

# CPU
CPU_CORES=$(nproc)
if [ "$CPU_CORES" -ge 4 ]; then
    test_pass "CPU cores: $CPU_CORES (4+ recommended)"
else
    test_warn "CPU cores: $CPU_CORES (4+ recommended)"
fi

# Memory
TOTAL_MEM=$(free -g | awk '/^Mem:/{print $2}')
if [ "$TOTAL_MEM" -ge 8 ]; then
    test_pass "Total memory: ${TOTAL_MEM}GB (8GB+ recommended)"
else
    test_warn "Total memory: ${TOTAL_MEM}GB (8GB+ recommended)"
fi

# Disk space
AVAILABLE_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$AVAILABLE_SPACE" -ge 20 ]; then
    test_pass "Available disk space: ${AVAILABLE_SPACE}GB (20GB+ recommended)"
else
    test_warn "Available disk space: ${AVAILABLE_SPACE}GB (20GB+ recommended)"
fi

# Check Docker logs for errors
echo ""
test_info "Checking Container Logs for Errors..."

FORTRESS_ERRORS=$(docker logs infinite-fortress 2>&1 | grep -i "error" | wc -l)
if [ "$FORTRESS_ERRORS" -eq 0 ]; then
    test_pass "No errors in fortress logs"
else
    test_warn "Found $FORTRESS_ERRORS error messages in fortress logs"
fi

# Check if .env exists
echo ""
test_info "Testing Configuration..."

if [ -f .env ]; then
    test_pass "Configuration file (.env) exists"
else
    test_warn "Configuration file (.env) not found"
fi

# Check if docker-compose.yml exists
if [ -f docker-compose.yml ]; then
    test_pass "Docker Compose configuration exists"
else
    test_fail "docker-compose.yml not found"
fi

# Summary
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   VERIFICATION SUMMARY                                            ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${GREEN}Passed:${NC}  $PASS tests"
echo -e "  ${YELLOW}Warnings:${NC} $WARN tests"
echo -e "  ${RED}Failed:${NC}  $FAIL tests"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}✓ All critical tests passed!${NC}"
    if [ "$WARN" -gt 0 ]; then
        echo -e "${YELLOW}⚠ Some warnings detected. Review them for optimal operation.${NC}"
    fi
    echo ""
    echo -e "${CYAN}🚀 System Status: OPERATIONAL${NC}"
    echo ""
    echo -e "Access your fortress at:"
    echo -e "  ${BLUE}Fortress:${NC} http://localhost:8000"
    echo -e "  ${BLUE}Rancher:${NC}  http://localhost:8090"
    EXIT_CODE=0
else
    echo -e "${RED}✗ Some tests failed. Please review and fix issues.${NC}"
    echo ""
    echo "Troubleshooting commands:"
    echo "  docker-compose logs fortress    # View fortress logs"
    echo "  docker-compose ps              # Check container status"
    echo "  docker-compose restart         # Restart all services"
    EXIT_CODE=1
fi

echo ""
echo -e "${CYAN}For detailed troubleshooting, see DEPLOYMENT.md${NC}"
echo ""

exit $EXIT_CODE
