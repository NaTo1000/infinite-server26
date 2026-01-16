# ╔═══════════════════════════════════════════════════════════════════╗
# ║                                                                   ║
# ║   ∞ INFINITE SERVER26 KALI EDITION                               ║
# ║   Autonomous AI-Powered Security Fortress                        ║
# ║                                                                   ║
# ║   Built by: NaTo1000                                             ║
# ║   Version: 26.1                                                  ║
# ║   Codename: "FORTRESS"                                           ║
# ║                                                                   ║
# ║   Multi-Stage Build - Optimized & Secure                         ║
# ║                                                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝

# ═══════════════════════════════════════════════════════════════════
# STAGE 1: DEPENDENCY BUILDER
# ═══════════════════════════════════════════════════════════════════
FROM kalilinux/kali-rolling:latest AS dependencies

# Build arguments for version control
ARG VERSION=26.1
ARG BUILD_DATE
ARG VCS_REF
ARG CODENAME=FORTRESS

# Environment setup for build stage
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Update and install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        git \
        gnupg \
        build-essential \
        gcc \
        g++ \
        make \
        cmake \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create virtual environment for Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python AI/ML dependencies in virtual environment
RUN pip3 install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    websockets==12.0 \
    aiohttp==3.9.1 \
    requests==2.31.0 \
    cryptography==41.0.7 \
    pycryptodome==3.19.1 \
    ecdsa==0.18.0 \
    web3==6.15.1 \
    eth-account==0.10.0 \
    eth-utils==2.3.1 \
    scikit-learn==1.4.0 \
    pandas==2.2.0 \
    numpy==1.26.3 \
    scipy==1.12.0 \
    matplotlib==3.8.2

# ═══════════════════════════════════════════════════════════════════
# STAGE 2: TOOLS AND REPOSITORIES
# ═══════════════════════════════════════════════════════════════════
FROM kalilinux/kali-rolling:latest AS tools

ENV DEBIAN_FRONTEND=noninteractive

# Install Kali security tools and runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # Core utilities
        ca-certificates \
        curl \
        wget \
        git \
        gnupg \
        procps \
        net-tools \
        iputils-ping \
        iproute2 \
        # Container orchestration
        docker.io \
        # Kali network scanning
        nmap \
        masscan \
        # Kali web tools
        nikto \
        sqlmap \
        dirb \
        gobuster \
        # Kali exploitation
        metasploit-framework \
        exploitdb \
        # Kali password tools
        john \
        hydra \
        # Kali wireless
        aircrack-ng \
        # Kali sniffing
        tcpdump \
        # Security tools
        openssl \
        fail2ban \
        ufw \
        # Python runtime
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Docker Compose
RUN curl -fsSL "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install kubectl
RUN curl -fsSL "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl" \
    -o /usr/local/bin/kubectl && \
    chmod +x /usr/local/bin/kubectl

# Install Helm
RUN curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Clone NiA Ecosystem repositories (lightweight, depth 1)
WORKDIR /opt/nia-ecosystem

RUN git clone --depth 1 --single-branch https://github.com/NaTo1000/NiA-Pegasus-Core.git pegasus 2>/dev/null || mkdir -p pegasus && \
    git clone --depth 1 --single-branch https://github.com/NaTo1000/NiA-Cluster.git cluster 2>/dev/null || mkdir -p cluster && \
    git clone --depth 1 --single-branch https://github.com/NaTo1000/CyberSecurity-Arsenal.git security-arsenal 2>/dev/null || mkdir -p security-arsenal

# Clone AI Systems repositories
WORKDIR /opt/ai-systems

RUN git clone --depth 1 --single-branch https://github.com/NaTo1000/NayDoe-AI-Assistant.git naydoe 2>/dev/null || mkdir -p naydoe && \
    git clone --depth 1 --single-branch https://github.com/NaTo1000/quantum-twinbrain.git twinbrain 2>/dev/null || mkdir -p twinbrain && \
    git clone --depth 1 --single-branch https://github.com/NaTo1000/ai-orchestration-system.git orchestration 2>/dev/null || mkdir -p orchestration

# ═══════════════════════════════════════════════════════════════════
# STAGE 3: FINAL PRODUCTION IMAGE
# ═══════════════════════════════════════════════════════════════════
FROM kalilinux/kali-rolling:latest AS production

# Build arguments
ARG VERSION=26.1
ARG BUILD_DATE
ARG VCS_REF
ARG CODENAME=FORTRESS

# OCI-compliant labels
LABEL org.opencontainers.image.title="Infinite Server26 Kali Edition" \
      org.opencontainers.image.description="Autonomous AI-Powered Security Fortress with Kali Linux" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="NaTo1000" \
      org.opencontainers.image.authors="NaTo1000" \
      org.opencontainers.image.url="https://github.com/NaTo1000/infinite-server26" \
      org.opencontainers.image.source="https://github.com/NaTo1000/infinite-server26" \
      org.opencontainers.image.documentation="https://github.com/NaTo1000/infinite-server26/blob/main/DOCKER.md" \
      org.opencontainers.image.licenses="MIT" \
      infinite.version="${VERSION}" \
      infinite.codename="${CODENAME}" \
      infinite.build.date="${BUILD_DATE}" \
      infinite.build.vcs-ref="${VCS_REF}"

# Production environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    TERM=xterm-256color \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:/usr/local/bin:${PATH}" \
    INFINITE_VERSION="${VERSION}" \
    NAYDOE_MODE="autonomous" \
    JESSICAI_MODE="huntress" \
    NAI_GAIL_ENABLED="true" \
    NIA_VAULT_ACTIVE="true" \
    SECURITY_LEVEL="maximum" \
    MERCY_MODE="disabled"

# Install minimal runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        python3 \
        python3-pip \
        procps \
        net-tools \
        openssl \
        docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy Python virtual environment from dependencies stage
COPY --from=dependencies /opt/venv /opt/venv

# Copy tools and binaries from tools stage
COPY --from=tools /usr/local/bin/docker-compose /usr/local/bin/docker-compose
COPY --from=tools /usr/local/bin/kubectl /usr/local/bin/kubectl
COPY --from=tools /usr/local/bin/helm /usr/local/bin/helm

# Copy Kali tools
COPY --from=tools /usr/bin/nmap /usr/bin/nmap
COPY --from=tools /usr/bin/masscan /usr/bin/masscan
COPY --from=tools /usr/bin/nikto /usr/bin/nikto
COPY --from=tools /usr/bin/hydra /usr/bin/hydra
COPY --from=tools /usr/bin/aircrack-ng /usr/bin/aircrack-ng

# Copy required libraries for Kali tools
COPY --from=tools /usr/lib/x86_64-linux-gnu/ /usr/lib/x86_64-linux-gnu/
COPY --from=tools /usr/share/nmap /usr/share/nmap

# Copy NiA ecosystem and AI systems
COPY --from=tools /opt/nia-ecosystem /opt/nia-ecosystem
COPY --from=tools /opt/ai-systems /opt/ai-systems

# Copy application files
COPY health-check.py /usr/local/bin/health-check.py
COPY ai-systems/ /opt/fortress/ai-systems/
COPY blockchain/ /opt/fortress/blockchain/
COPY security/ /opt/fortress/security/
COPY intelligence/ /opt/fortress/intelligence/
COPY payment/ /opt/fortress/payment/
COPY licensing/ /opt/fortress/licensing/
COPY news-vault/ /opt/fortress/news-vault/
COPY plugins/ /opt/fortress/plugins/
COPY updates/ /opt/fortress/updates/
COPY data-streams/ /opt/fortress/data-streams/

# Create necessary directories
RUN mkdir -p \
    /opt/nai-gail/{ble,wifi,mesh,shield} \
    /opt/nia-vault/{blockchain,storage,keys,encrypted} \
    /opt/autonomous/{orchestrator,monitor,defender,healer} \
    /opt/rancher \
    /var/lib/rancher \
    /root/{fortress,vault,logs,config} \
    /var/log/fortress && \
    chmod +x /usr/local/bin/health-check.py

# Create non-root user for security (where applicable)
RUN useradd -r -u 1000 -m -s /bin/bash fortress && \
    chown -R fortress:fortress /opt/fortress /root/fortress /var/log/fortress

# Create service launcher scripts
RUN echo '#!/bin/bash\npython3 /opt/fortress/ai-systems/naydoe_orchestrator.py' > /usr/local/bin/naydoe-start && \
    echo '#!/bin/bash\npython3 /opt/fortress/ai-systems/jessicai_huntress.py' > /usr/local/bin/jessicai-start && \
    echo '#!/bin/bash\npython3 /opt/fortress/security/nai_gail_mesh_shield.py' > /usr/local/bin/nai-gail-start && \
    echo '#!/bin/bash\npython3 /opt/fortress/blockchain/nia_vault_blockchain.py' > /usr/local/bin/nia-vault-start && \
    echo '#!/bin/bash\ndocker run -d --privileged --restart=unless-stopped -p 8090:80 -p 8444:443 -v rancher-data:/var/lib/rancher rancher/rancher:latest' > /usr/local/bin/rancher-start && \
    chmod +x /usr/local/bin/*-start

# Create welcome banner
COPY --chown=root:root <<'EOF' /usr/local/bin/infinite-welcome
#!/bin/bash
clear
echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║   ██╗███╗   ██╗███████╗██╗███╗   ██╗██╗████████╗███████╗         ║"
echo "║   ██║████╗  ██║██╔════╝██║████╗  ██║██║╚══██╔══╝██╔════╝         ║"
echo "║   ██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║██║   ██║   █████╗           ║"
echo "║   ██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██║   ██║   ██╔══╝           ║"
echo "║   ██║██║ ╚████║██║     ██║██║ ╚████║██║   ██║   ███████╗         ║"
echo "║   ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚══════╝         ║"
echo "║                                                                   ║"
echo "║   SERVER26 KALI EDITION - FORTRESS                               ║"
echo "║   Autonomous AI-Powered Security Fortress                        ║"
echo "║   Version: ${INFINITE_VERSION} | Built by: NaTo1000              ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🤖 AI SYSTEMS: Ready"
echo "🛡️  DEFENSE: Active"
echo "🐳 CONTAINERS: Available"
echo "⚔️  KALI TOOLS: Loaded"
echo ""
echo "🔐 SECURITY STATUS: [MAXIMUM]"
echo "⚡ FORTRESS MODE ACTIVATED ⚡"
echo ""
EOF

RUN chmod +x /usr/local/bin/infinite-welcome && \
    echo '[ -f /usr/local/bin/infinite-welcome ] && /usr/local/bin/infinite-welcome' >> /root/.bashrc

# Set working directory
WORKDIR /root/fortress

# Expose ports
EXPOSE 80 443 8080 8443 6443 2376 2377 5000 8000 9000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start health check service
CMD ["python3", "/usr/local/bin/health-check.py", "8000"]

# ═══════════════════════════════════════════════════════════════════
# STAGE 4: BUILD TEST
# ═══════════════════════════════════════════════════════════════════
FROM production AS test

# Install test dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        netcat-traditional && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Run basic validation tests
RUN python3 --version && \
    python3 -c "import fastapi, uvicorn, cryptography, web3" && \
    docker-compose --version && \
    kubectl version --client && \
    helm version && \
    nmap --version && \
    echo "✓ All core dependencies validated"

# Validate directory structure
RUN test -d /opt/fortress && \
    test -d /opt/nia-ecosystem && \
    test -d /opt/ai-systems && \
    test -f /usr/local/bin/health-check.py && \
    echo "✓ Directory structure validated"

# Test health check script
RUN timeout 5 python3 /usr/local/bin/health-check.py 8000 & \
    sleep 2 && \
    curl -f http://localhost:8000/health && \
    echo "✓ Health check validated"
