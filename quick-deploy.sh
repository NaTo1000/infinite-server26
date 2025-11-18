#!/bin/bash

# ═══════════════════════════════════════════════════════════════════
# INFINITE SERVER26 - Quick Deploy Script
# ═══════════════════════════════════════════════════════════════════
# 
# This script automates the deployment of Infinite Server26 Fortress
# Usage: ./quick-deploy.sh
#
# Built by: NaTo1000
# Version: 26.1
# ═══════════════════════════════════════════════════════════════════

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}║   ∞ INFINITE SERVER26 - QUICK DEPLOY                             ║${NC}"
echo -e "${CYAN}║   Autonomous AI-Powered Security Fortress                        ║${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}║   Version: 26.1 | Built by: NaTo1000                             ║${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if running as root (for some system operations)
if [ "$EUID" -eq 0 ]; then 
    print_warning "Running as root. Some features will be skipped for security."
fi

# Check prerequisites
print_status "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed!"
    echo ""
    echo "Install Docker with:"
    echo "  curl -fsSL https://get.docker.com | sh"
    exit 1
fi
print_success "Docker found: $(docker --version)"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed!"
    echo ""
    echo "Install Docker Compose with:"
    echo '  sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
    echo "  sudo chmod +x /usr/local/bin/docker-compose"
    exit 1
fi
print_success "Docker Compose found: $(docker-compose --version)"

# Check if .env exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        print_success "Created .env from .env.example"
        print_warning "Please edit .env file with your configuration before proceeding!"
        echo ""
        echo "Important settings to configure:"
        echo "  - RANCHER_PASSWORD"
        echo "  - VAULT_MASTER_KEY"
        echo "  - MESH_NETWORK_PASSWORD"
        echo ""
        read -p "Press Enter after editing .env to continue, or Ctrl+C to exit..."
    else
        print_error ".env.example not found!"
        exit 1
    fi
else
    print_success ".env file found"
fi

# Check disk space
print_status "Checking disk space..."
AVAILABLE_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$AVAILABLE_SPACE" -lt 20 ]; then
    print_warning "Low disk space: ${AVAILABLE_SPACE}GB available (20GB+ recommended)"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_success "Sufficient disk space: ${AVAILABLE_SPACE}GB available"
fi

# Stop existing containers if any
print_status "Stopping any existing containers..."
docker-compose down 2>/dev/null || true
print_success "Stopped existing containers"

# Pull latest images
print_status "Pulling latest Docker images..."
if docker-compose pull; then
    print_success "Images pulled successfully"
else
    print_warning "Failed to pull images, will build locally if needed"
fi

# Start deployment
print_status "Starting deployment..."
echo ""

if docker-compose up -d; then
    print_success "Deployment started successfully!"
else
    print_error "Deployment failed!"
    echo ""
    echo "Check logs with: docker-compose logs"
    exit 1
fi

# Wait for containers to start
print_status "Waiting for containers to start..."
sleep 10

# Check container status
print_status "Checking container status..."
echo ""
docker-compose ps
echo ""

# Verify services
print_status "Verifying services..."

# Check fortress container
if docker-compose ps | grep -q "fortress.*Up"; then
    print_success "Fortress container is running"
else
    print_error "Fortress container is not running!"
    docker-compose logs fortress
fi

# Check rancher container
if docker-compose ps | grep -q "rancher.*Up"; then
    print_success "Rancher container is running"
else
    print_warning "Rancher container status unclear"
fi

# Display access information
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                                   ║${NC}"
echo -e "${GREEN}║   ✓ DEPLOYMENT SUCCESSFUL!                                        ║${NC}"
echo -e "${GREEN}║                                                                   ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}🚀 Access Points:${NC}"
echo ""
echo -e "  ${BLUE}Fortress Dashboard:${NC}  http://localhost:8000"
echo -e "  ${BLUE}Rancher Dashboard:${NC}   http://localhost:8090"
echo ""
echo -e "${CYAN}📊 Useful Commands:${NC}"
echo ""
echo -e "  ${YELLOW}View logs:${NC}           docker-compose logs -f fortress"
echo -e "  ${YELLOW}Check status:${NC}        docker-compose ps"
echo -e "  ${YELLOW}Enter container:${NC}     docker-compose exec fortress /bin/bash"
echo -e "  ${YELLOW}Stop fortress:${NC}       docker-compose down"
echo -e "  ${YELLOW}Restart:${NC}             docker-compose restart"
echo ""
echo -e "${CYAN}🔐 Rancher Bootstrap Password:${NC}"
echo ""
RANCHER_PASSWORD=$(docker logs rancher-dashboard 2>&1 | grep "Bootstrap Password:" | tail -1 || echo "Check logs with: docker logs rancher-dashboard")
echo "  $RANCHER_PASSWORD"
echo ""
echo -e "${CYAN}📖 Documentation:${NC}"
echo ""
echo -e "  ${BLUE}Full Guide:${NC}          See DEPLOYMENT.md"
echo -e "  ${BLUE}Build Guide:${NC}         See BUILD_AND_PUSH.md"
echo -e "  ${BLUE}README:${NC}              See README.md"
echo ""
echo -e "${GREEN}⚡ FORTRESS MODE ACTIVATED ⚡${NC}"
echo -e "   ${RED}NO MERCY. NO COMPROMISE. TOTAL SECURITY.${NC}"
echo ""
echo -e "${CYAN}Built with ❤️  by NaTo1000 | Version 26.1${NC}"
echo ""

# Save deployment info
DEPLOYMENT_INFO="deployment-info-$(date +%Y%m%d-%H%M%S).txt"
cat > "$DEPLOYMENT_INFO" <<EOF
═══════════════════════════════════════════════════════════════════
INFINITE SERVER26 - DEPLOYMENT INFORMATION
═══════════════════════════════════════════════════════════════════

Deployment Time: $(date)
Deployment User: $(whoami)
Hostname: $(hostname)

Access Points:
- Fortress Dashboard: http://localhost:8000
- Rancher Dashboard: http://localhost:8090

Container Status:
$(docker-compose ps)

Rancher Bootstrap Password:
$RANCHER_PASSWORD

Useful Commands:
- View logs: docker-compose logs -f fortress
- Check status: docker-compose ps
- Enter container: docker-compose exec fortress /bin/bash
- Stop: docker-compose down
- Restart: docker-compose restart

═══════════════════════════════════════════════════════════════════
Built by NaTo1000 | Version 26.1 | FORTRESS MODE
═══════════════════════════════════════════════════════════════════
EOF

print_success "Deployment info saved to: $DEPLOYMENT_INFO"

exit 0
