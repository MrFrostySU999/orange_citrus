#!/bin/bash

# =====================================================
# ORANGE_CITRUS AUTOMATED DEPLOYMENT & INSTALLATION SCRIPT
# =====================================================

# Color configurations
ORANGE='\033[38;5;208m'
GREEN='\033[92m'
RED='\033[91m'
YELLOW='\033[93m'
RESET='\033[0m'

clear
echo -e "${ORANGE}=============================================${RESET}"
echo -e "${ORANGE}    ORANGE_CITRUS SYSTEM DEPLOYMENT WIZARD   ${RESET}"
echo -e "${ORANGE}=============================================${RESET}"

# 1. Enforce root privileges for apt manipulation
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Error: This framework setup script must be run as root/sudo.${RESET}"
    echo -e "${YELLOW}[*] Please retry using: sudo bash setup.sh${RESET}"
    exit 1
fi

# 2. Update package repositories and install core dependencies
echo -e "\n${ORANGE}[*] Stage 1: Synchronizing system repositories...${RESET}"
apt-get update -y

echo -e "\n${ORANGE}[*] Stage 2: Deploying system dependencies (git, python3, pip)...${RESET}"
apt-get install -y git python3 python3-pip python3-requests

# 3. Handle Python environments
echo -e "\n${ORANGE}[*] Stage 3: Verifying required Python packages...${RESET}"
python3 -m pip install --break-system-packages requests 2>/dev/null || python3 -m pip install requests

# 4. Generate system storage directories used by VulnEngine
echo -e "\n${ORANGE}[*] Stage 4: Preparing workspace environments...${RESET}"
USER_HOME=$(eval echo ~${SUDO_USER})
mkdir -p "$USER_HOME/orange_tools"
mkdir -p "$USER_HOME/orange_v1"

# Adjust file ownership so your regular system user can access the tools
chown -R ${SUDO_USER}:${SUDO_USER} "$USER_HOME/orange_tools"
chown -R ${SUDO_USER}:${SUDO_USER} "$USER_HOME/orange_v1"

# 5. Optional Feature: Automatically check and convert SSH URLs to HTTPS if preferred
if [ -f "config.py" ]; then
    echo -e "\n${ORANGE}[*] Stage 5: Aligning script file architectures...${RESET}"
    read -p "Use HTTPS instead of SSH for GitHub tool downloads? (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        sed -i 's|git@github.com:|https://github.com|g' config.py
        echo -e "${GREEN}[+] config.py successfully converted to public HTTPS cloning URLs.${RESET}"
    fi
fi

# 6. Final verification
echo -e "\n${GREEN}[+] Environment configuration complete!${RESET}"
echo -e "${YELLOW}[*] To launch your framework, run: sudo python3 orange.py${RESET}\n"
