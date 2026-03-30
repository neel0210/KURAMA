#!/bin/bash

# --- COLOR SCHEME ---
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}                🦊 KURAMA USERBOT: GLOBAL EDITION${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# --- OS DETECTION JUTSU ---
OS_TYPE="unknown"
if [[ "$OSTYPE" == "linux-android"* ]]; then
    OS_TYPE="termux"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS_TYPE="windows"
fi

echo -e "${YELLOW}📡 Detecting Chakra Signature: ${NC}${OS_TYPE^^}"

# --- SYSTEM DEPENDENCIES ---
case $OS_TYPE in
    "termux")
        echo -e "${YELLOW}📦 Updating Termux Packages...${NC}"
        pkg update -y && pkg upgrade -y
        pkg install -y python git libjpeg-turbo libpng binutils rust
        ;;
    "linux")
        echo -e "${YELLOW}📦 Ensuring Python and PIP are installed...${NC}"
        sudo apt update
        sudo apt install -y python3 python3-pip git libjpeg-dev zlib1g-dev
        ;;
    "macos")
        brew install python git
        ;;
esac

# --- GIT CONFIGURATION ---
git config --global pull.rebase false

# --- .ENV VALIDATION JUTSU ---
if [ ! -f .env ]; then touch .env; fi

check_env_var() {
    local var_name=$1
    local prompt_msg=$2
    if ! grep -q "^$var_name=" .env; then
        echo -e "${RED}⚠️  Missing $var_name in .env!${NC}"
        echo -e "${CYAN}$prompt_msg${NC}"
        read -r user_input
        echo "$var_name=$user_input" >> .env
    fi
}

check_env_var "API_ID" "Enter your Telegram API_ID:"
check_env_var "API_HASH" "Enter your Telegram API_HASH:"
check_env_var "CHAT_ID" "Enter the Target Group ID (e.g., -100...):"
check_env_var "GIT" "Enter your GitHub Personal Access Token:"

# --- REQUIREMENTS.TXT ---
if [ ! -f requirements.txt ]; then
    cat <<EOT >> requirements.txt
telethon
python-dotenv
pillow
rembg[pillow]
onnxruntime
requests
aiohttp
hachoir
python-barcode
google-trans-new
EOT
fi

# --- INSTALL PYTHON DEPS ---
echo -e "${YELLOW}🐍 Installing Python Modules globally...${NC}"
# Use --break-system-packages if on modern Linux/Debian to bypass venv enforcement
if [[ "$OS_TYPE" == "linux" ]]; then
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt --break-system-packages
else
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
fi

# --- FINAL EXECUTION ---
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🔥 SYSTEM SEALED. KURAMA IS READY!${NC}"
echo -e "${YELLOW}🦊 Launching the Userbot...${NC}"

python3 main.py