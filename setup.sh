#!/bin/bash

# --- COLOR SCHEME ---
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}             🦊 KURAMA USERBOT: ETERNAL GUARDIAN${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# --- OS & ENVIRONMENT DETECTION ---
OS_TYPE="unknown"
VENV_DIR=".venv"

if [[ "$OSTYPE" == "linux-android"* ]]; then
    OS_TYPE="termux"
    PY_CMD="python"
    
    # --- TERMUX VENV LOGIC ---
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${YELLOW}🌀 No Venv detected. Forging a new Chakra Pool...${NC}"
        python -m venv $VENV_DIR
    fi
    echo -e "${CYAN}🧪 Activating Termux Virtual Environment...${NC}"
    source $VENV_DIR/bin/activate
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS_TYPE="windows"
    PY_CMD="python"
else
    OS_TYPE="linux/macos"
    PY_CMD="python3"
fi

echo -e "${YELLOW}📡 OS Detected:${NC} ${OS_TYPE^^}"
echo -e "${YELLOW}🐍 Python Chakra:${NC} $(which $PY_CMD)"

# --- THE REINCARNATION LOOP ---
while true
do
    echo -e "${GREEN}⚡ Kurama is awakening... Launching main.py${NC}"
    
    if [[ "$OS_TYPE" == "windows" ]]; then
        # Windows requires winpty for interactive terminal sessions
        winpty $PY_CMD requirements.py
        winpty $PY_CMD main.py
    else
        # Termux/Linux runs directly
        $PY_CMD requirements.py
        $PY_CMD main.py
    fi

    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${CYAN}🏮 Manual Reincarnation detected (.update install).${NC}"
    else
        echo -e "${RED}⚠️  Kurama took damage (Crash Exit Code: $EXIT_CODE).${NC}"
    fi

    echo -e "${YELLOW}⏳ Restoring Chakra in 3 seconds...${NC}"
    sleep 3
done
