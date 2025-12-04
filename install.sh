#!/bin/bash

# ═══════════════════════════════════════════════════════════════════
# INFINITE SERVER26 - One-Line Installer
# ═══════════════════════════════════════════════════════════════════
# 
# This script installs all prerequisites and deploys Infinite Server26
# Usage: curl -fsSL https://raw.githubusercontent.com/NaTo1000/infinite-server26/main/install.sh | bash
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

# Banner
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}║   ∞ INFINITE SERVER26 - ONE-LINE INSTALLER                       ║${NC}"
echo -e "${CYAN}║   Autonomous AI-Powered Security Fortress                        ║${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}║   Version: 26.1 | Built by: NaTo1000                             ║${NC}"
echo -e "${CYAN}║                                                                   ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

print_status() { echo -e "${BLUE}[*]${NC} $1"; }
print_success() { echo -e "${GREEN}[✓]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "This installer must be run as root (use sudo)"
    exit 1
fi

# Detect OS
print_status "Detecting operating system..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION=$VERSION_ID
    print_success "Detected: $PRETTY_NAME"
else
    print_error "Cannot detect OS. This script supports Ubuntu, Debian, and Kali Linux."
    exit 1
fi

# Update system
print_status "Updating system packages..."
apt-get update -qq
print_success "System updated"

# Install prerequisites
print_status "Installing prerequisites..."
apt-get install -y -qq curl wget git ca-certificates gnupg lsb-release >/dev/null 2>&1
print_success "Prerequisites installed"

# Install Docker
print_status "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    print_status "Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com | sh >/dev/null 2>&1
    systemctl enable docker
    systemctl start docker
    print_success "Docker installed and started"
else
    print_success "Docker already installed: $(docker --version)"
fi

# Install Docker Compose
print_status "Checking Docker Compose installation..."
if ! command -v docker-compose &> /dev/null; then
    print_status "Docker Compose not found. Installing..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose 2>/dev/null
    chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed"
else
    print_success "Docker Compose already installed: $(docker-compose --version)"
fi

# Clone repository
INSTALL_DIR="/opt/infinite-server26"
print_status "Cloning Infinite Server26 repository..."

if [ -d "$INSTALL_DIR" ]; then
    print_warning "Directory $INSTALL_DIR already exists. Updating..."
    cd "$INSTALL_DIR"
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true
else
    git clone https://github.com/NaTo1000/infinite-server26.git "$INSTALL_DIR" 2>/dev/null
    print_success "Repository cloned to $INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# Create environment file
if [ ! -f .env ]; then
    print_status "Creating environment configuration..."
    if [ -f .env.example ]; then
        cp .env.example .env
        
        # Generate random passwords
        RANCHER_PASS=$(openssl rand -base64 16)
        VAULT_KEY=$(openssl rand -base64 32 | cut -c1-32)
        MESH_PASS=$(openssl rand -base64 16)
        
        # Update .env with generated passwords
        sed -i "s/YourSecurePasswordHere/$RANCHER_PASS/" .env
        sed -i "s/your_secure_vault_master_key_here/$VAULT_KEY/" .env
        sed -i "s/your_mesh_password_here/$MESH_PASS/" .env
        
        print_success "Environment configured with random passwords"
    else
        print_warning ".env.example not found, skipping environment setup"
    fi
else
    print_success "Environment file already exists"
fi

# Pull Docker images
print_status "Pulling Docker images (this may take several minutes)..."
docker-compose pull 2>/dev/null || print_warning "Could not pull images, will build locally if needed"

# Start services
print_status "Starting Infinite Server26 Fortress..."
docker-compose up -d

# Wait for startup
print_status "Waiting for services to initialize..."
sleep 15

# Check status
print_status "Verifying deployment..."
if docker-compose ps | grep -q "Up"; then
    print_success "Services are running!"
else
    print_warning "Some services may still be starting..."
fi

# Display information
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                                   ║${NC}"
echo -e "${GREEN}║   ✓ INSTALLATION COMPLETE!                                        ║${NC}"
echo -e "${GREEN}║                                                                   ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📍 Installation Directory:${NC} $INSTALL_DIR"
echo ""
echo -e "${CYAN}🚀 Access Points:${NC}"
echo -e "  ${BLUE}Fortress Dashboard:${NC}  http://localhost:8000"
echo -e "  ${BLUE}Rancher Dashboard:${NC}   http://localhost:8090"
echo ""
echo -e "${CYAN}🔐 Generated Credentials:${NC}"
if [ -f .env ]; then
    echo -e "  ${YELLOW}Rancher Password:${NC}     $(grep RANCHER_PASSWORD .env | cut -d'=' -f2)"
    echo -e "  ${YELLOW}Vault Master Key:${NC}     $(grep VAULT_MASTER_KEY .env | cut -d'=' -f2)"
fi
echo ""
echo -e "${CYAN}📊 Useful Commands:${NC}"
echo -e "  ${YELLOW}View status:${NC}          cd $INSTALL_DIR && docker-compose ps"
echo -e "  ${YELLOW}View logs:${NC}            cd $INSTALL_DIR && docker-compose logs -f"
echo -e "  ${YELLOW}Stop fortress:${NC}        cd $INSTALL_DIR && docker-compose down"
echo -e "  ${YELLOW}Restart:${NC}              cd $INSTALL_DIR && docker-compose restart"
echo -e "  ${YELLOW}Verify deployment:${NC}    cd $INSTALL_DIR && ./verify-deployment.sh"
echo ""
echo -e "${CYAN}📖 Documentation:${NC}"
echo -e "  ${BLUE}Full Guide:${NC}          $INSTALL_DIR/DEPLOYMENT.md"
echo -e "  ${BLUE}Build Guide:${NC}         $INSTALL_DIR/BUILD_AND_PUSH.md"
echo -e "  ${BLUE}Contributing:${NC}        $INSTALL_DIR/CONTRIBUTING.md"
echo ""
echo -e "${GREEN}⚡ FORTRESS MODE ACTIVATED ⚡${NC}"
echo -e "   ${RED}NO MERCY. NO COMPROMISE. TOTAL SECURITY.${NC}"
echo ""
echo -e "${CYAN}Built with ❤️  by NaTo1000 | Version 26.1${NC}"
echo ""

# Save installation info
cat > "$INSTALL_DIR/installation-info.txt" <<EOF
═══════════════════════════════════════════════════════════════════
INFINITE SERVER26 - INSTALLATION INFORMATION
═══════════════════════════════════════════════════════════════════

Installation Time: $(date)
Installation Path: $INSTALL_DIR
Operating System: $PRETTY_NAME

Access Points:
- Fortress Dashboard: http://localhost:8000
- Rancher Dashboard: http://localhost:8090

Credentials (saved in .env file):
$(grep -E 'RANCHER_PASSWORD|VAULT_MASTER_KEY|MESH_NETWORK_PASSWORD' .env 2>/dev/null || echo "See .env file")

Useful Commands:
- cd $INSTALL_DIR
- docker-compose ps              # Check status
- docker-compose logs -f         # View logs
- docker-compose restart         # Restart services
- ./verify-deployment.sh         # Verify deployment

═══════════════════════════════════════════════════════════════════
Built by NaTo1000 | Version 26.1 | FORTRESS MODE
═══════════════════════════════════════════════════════════════════
EOF

print_success "Installation information saved to: $INSTALL_DIR/installation-info.txt"

exit 0
