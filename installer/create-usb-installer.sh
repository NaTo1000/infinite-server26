#!/bin/bash

################################################################################
#                                                                              #
#   INFINITE SERVER26 - ENCRYPTED USB INSTALLER CREATOR                       #
#   Self-Building, Auto-Deploying Installation System                         #
#   Version: 26.1 | Built by: NaTo1000                                        #
#                                                                              #
#   Creates an encrypted USB drive that self-builds and deploys               #
#   Infinite Server26 on any compatible system                                #
#                                                                              #
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
print_banner() {
    clear
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                                                                   ║"
    echo "║   ∞ INFINITE SERVER26 - USB INSTALLER CREATOR                    ║"
    echo "║   Encrypted Self-Building Installation System                    ║"
    echo "║   Version: 26.1 | Built by: NaTo1000                             ║"
    echo "║                                                                   ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}❌ This script must be run as root${NC}"
        echo "Please run: sudo $0"
        exit 1
    fi
}

# List available USB devices
list_usb_devices() {
    echo -e "${CYAN}📀 Available USB Devices:${NC}"
    echo ""
    lsblk -d -o NAME,SIZE,TYPE,TRAN | grep usb || echo "No USB devices found"
    echo ""
}

# Select USB device
select_usb_device() {
    list_usb_devices
    
    echo -e "${YELLOW}⚠️  WARNING: All data on the selected device will be ERASED!${NC}"
    echo ""
    read -p "Enter USB device (e.g., sdb): " USB_DEVICE
    
    if [ ! -b "/dev/${USB_DEVICE}" ]; then
        echo -e "${RED}❌ Device /dev/${USB_DEVICE} not found${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${RED}⚠️  FINAL WARNING: This will ERASE /dev/${USB_DEVICE}${NC}"
    read -p "Type 'YES' to continue: " CONFIRM
    
    if [ "$CONFIRM" != "YES" ]; then
        echo "Cancelled."
        exit 0
    fi
}

# Create encrypted partition
create_encrypted_partition() {
    echo -e "${BLUE}🔐 Creating encrypted partition...${NC}"
    
    # Unmount if mounted
    umount /dev/${USB_DEVICE}* 2>/dev/null || true
    
    # Wipe device
    echo -e "${CYAN}Wiping device...${NC}"
    dd if=/dev/zero of=/dev/${USB_DEVICE} bs=1M count=100 status=progress 2>/dev/null || true
    
    # Create partition table
    echo -e "${CYAN}Creating partition table...${NC}"
    parted -s /dev/${USB_DEVICE} mklabel gpt
    parted -s /dev/${USB_DEVICE} mkpart primary ext4 1MiB 100%
    
    # Setup LUKS encryption
    echo -e "${CYAN}Setting up LUKS encryption...${NC}"
    echo ""
    echo -e "${YELLOW}Enter encryption password for USB drive:${NC}"
    cryptsetup luksFormat /dev/${USB_DEVICE}1
    
    echo ""
    echo -e "${YELLOW}Enter password again to open encrypted partition:${NC}"
    cryptsetup open /dev/${USB_DEVICE}1 infinite_usb
    
    # Create filesystem
    echo -e "${CYAN}Creating filesystem...${NC}"
    mkfs.ext4 -L "INFINITE_SERVER26" /dev/mapper/infinite_usb
    
    echo -e "${GREEN}✅ Encrypted partition created${NC}"
}

# Mount encrypted partition
mount_encrypted_partition() {
    echo -e "${BLUE}📂 Mounting encrypted partition...${NC}"
    
    MOUNT_POINT="/mnt/infinite_usb"
    mkdir -p $MOUNT_POINT
    mount /dev/mapper/infinite_usb $MOUNT_POINT
    
    echo -e "${GREEN}✅ Mounted at $MOUNT_POINT${NC}"
}

# Copy installation files
copy_installation_files() {
    echo -e "${BLUE}📦 Copying installation files...${NC}"
    
    # Create directory structure
    mkdir -p $MOUNT_POINT/{installer,docker,ai-systems,security,blockchain,config,scripts}
    
    # Copy Dockerfile
    echo -e "${CYAN}Copying Dockerfile...${NC}"
    cp /home/ubuntu/infinite-server26/Dockerfile $MOUNT_POINT/docker/
    
    # Copy AI systems
    echo -e "${CYAN}Copying AI systems...${NC}"
    cp -r /home/ubuntu/infinite-server26/ai-systems/* $MOUNT_POINT/ai-systems/
    
    # Copy security systems
    echo -e "${CYAN}Copying security systems...${NC}"
    cp -r /home/ubuntu/infinite-server26/security/* $MOUNT_POINT/security/
    
    # Copy blockchain
    echo -e "${CYAN}Copying blockchain...${NC}"
    cp -r /home/ubuntu/infinite-server26/blockchain/* $MOUNT_POINT/blockchain/
    
    echo -e "${GREEN}✅ Files copied${NC}"
}

# Create auto-installer script
create_auto_installer() {
    echo -e "${BLUE}🤖 Creating auto-installer script...${NC}"
    
    cat > $MOUNT_POINT/installer/auto-install.sh << 'INSTALLER_EOF'
#!/bin/bash

################################################################################
#   INFINITE SERVER26 - AUTO INSTALLER                                        #
#   Self-building installation script                                         #
################################################################################

set -e

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║   ∞ INFINITE SERVER26 - AUTO INSTALLER                           ║"
echo "║   Self-Building Fortress Deployment                               ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
fi

# Build Docker image
echo "🔨 Building Infinite Server26 Docker image..."
cd /mnt/infinite_usb/docker
docker build -t nato1000/infinite-server26:latest .

# Create service files
echo "⚙️  Creating systemd services..."

# NayDoeV1 service
cat > /etc/systemd/system/naydoev1.service << 'EOF'
[Unit]
Description=NayDoeV1 Autonomous Orchestrator
After=docker.service
Requires=docker.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/ai-systems/naydoe_orchestrator.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# JessicAi service
cat > /etc/systemd/system/jessicai.service << 'EOF'
[Unit]
Description=JessicAi Security Huntress
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/ai-systems/jessicai_huntress.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# NAi_gAil service
cat > /etc/systemd/system/nai-gail.service << 'EOF'
[Unit]
Description=NAi_gAil Mesh Shield
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/security/nai_gail_mesh_shield.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# NiA_Vault service
cat > /etc/systemd/system/nia-vault.service << 'EOF'
[Unit]
Description=NiA_Vault Braided Blockchain
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/blockchain/nia_vault_blockchain.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Copy files to system
echo "📁 Installing system files..."
mkdir -p /opt/{ai-systems,security,blockchain}
cp -r /mnt/infinite_usb/ai-systems/* /opt/ai-systems/
cp -r /mnt/infinite_usb/security/* /opt/security/
cp -r /mnt/infinite_usb/blockchain/* /opt/blockchain/

# Make scripts executable
chmod +x /opt/ai-systems/*.py
chmod +x /opt/security/*.py
chmod +x /opt/blockchain/*.py

# Enable and start services
echo "🚀 Starting services..."
systemctl daemon-reload
systemctl enable naydoev1 jessicai nai-gail nia-vault
systemctl start naydoev1 jessicai nai-gail nia-vault

# Start Rancher
echo "🐄 Starting Rancher..."
docker run -d \
    --name rancher \
    --restart=unless-stopped \
    -p 80:80 -p 443:443 \
    --privileged \
    rancher/rancher:latest

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║   ✅ INFINITE SERVER26 INSTALLATION COMPLETE!                    ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🤖 NayDoeV1 - Orchestrator: RUNNING"
echo "⚔️  JessicAi - Huntress: ACTIVE (NO MERCY MODE)"
echo "🛡️  NAi_gAil - Mesh Shield: DEPLOYED"
echo "🔐 NiA_Vault - Blockchain: ENCRYPTED"
echo "🐄 Rancher - Dashboard: https://localhost"
echo ""
echo "⚡ FORTRESS MODE ACTIVATED ⚡"
echo ""
INSTALLER_EOF

    chmod +x $MOUNT_POINT/installer/auto-install.sh
    
    echo -e "${GREEN}✅ Auto-installer created${NC}"
}

# Create README
create_readme() {
    echo -e "${BLUE}📝 Creating README...${NC}"
    
    cat > $MOUNT_POINT/README.md << 'README_EOF'
# ∞ INFINITE SERVER26 - ENCRYPTED USB INSTALLER

**Autonomous AI-Powered Security Fortress**

Version: 26.1 | Built by: NaTo1000

---

## 🚀 Quick Start

### Step 1: Decrypt USB Drive

```bash
sudo cryptsetup open /dev/sdX1 infinite_usb
sudo mount /dev/mapper/infinite_usb /mnt/infinite_usb
```

### Step 2: Run Auto-Installer

```bash
cd /mnt/infinite_usb/installer
sudo ./auto-install.sh
```

### Step 3: Access Systems

- **Rancher Dashboard**: https://localhost
- **NayDoeV1 Logs**: `journalctl -u naydoev1 -f`
- **JessicAi Logs**: `journalctl -u jessicai -f`
- **System Status**: `systemctl status naydoev1 jessicai nai-gail nia-vault`

---

## 🔐 Security

- **Encryption**: LUKS AES-256
- **AI Security**: JessicAi Huntress (No Mercy Mode)
- **Mesh Shield**: NAi_gAil Impenetrable Dome
- **Blockchain**: NiA_Vault Braided Chain

---

## ⚡ FORTRESS MODE ACTIVATED ⚡

**NO MERCY. NO COMPROMISE. TOTAL SECURITY.**

Built with ❤️ by NaTo1000
README_EOF

    echo -e "${GREEN}✅ README created${NC}"
}

# Unmount and close
cleanup() {
    echo -e "${BLUE}🔒 Securing USB drive...${NC}"
    
    sync
    umount $MOUNT_POINT
    cryptsetup close infinite_usb
    rmdir $MOUNT_POINT
    
    echo -e "${GREEN}✅ USB drive secured${NC}"
}

# Main
main() {
    print_banner
    check_root
    select_usb_device
    create_encrypted_partition
    mount_encrypted_partition
    copy_installation_files
    create_auto_installer
    create_readme
    cleanup
    
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   ✅ ENCRYPTED USB INSTALLER CREATED SUCCESSFULLY!               ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}📀 USB Device: /dev/${USB_DEVICE}${NC}"
    echo -e "${CYAN}🔐 Encryption: LUKS AES-256${NC}"
    echo -e "${CYAN}📦 Contents: Infinite Server26 Complete System${NC}"
    echo ""
    echo -e "${YELLOW}To use:${NC}"
    echo "  1. Insert USB on target system"
    echo "  2. Decrypt: sudo cryptsetup open /dev/sdX1 infinite_usb"
    echo "  3. Mount: sudo mount /dev/mapper/infinite_usb /mnt/infinite_usb"
    echo "  4. Install: cd /mnt/infinite_usb/installer && sudo ./auto-install.sh"
    echo ""
    echo -e "${PURPLE}⚡ FORTRESS READY FOR DEPLOYMENT ⚡${NC}"
    echo ""
}

main
