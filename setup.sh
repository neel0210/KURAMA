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

# --- OS & PYTHON DETECTION ---
OS_TYPE="unknown"
if [[ "$OSTYPE" == "linux-android"* ]]; then
    OS_TYPE="termux"
    PY_CMD="python"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS_TYPE="windows"
    PY_CMD="python"
else
    OS_TYPE="linux/macos"
    PY_CMD="python3"
fi

echo -e "${YELLOW}📡 OS Detected:${NC} ${OS_TYPE^^}"
echo -e "${YELLOW}🐍 Python Chakra:${NC} $PY_CMD"

# --- THE REINCARNATION LOOP ---
while true
do
    echo -e "${GREEN}⚡ Kurama is awakening... Launching main.py${NC}"
    
    # Check if we are on Windows/Git Bash to use winpty for interactive input
    if [[ "$OS_TYPE" == "windows" ]]; then
        winpty $PY_CMD requirements.py
		winpty $PY_CMD main.py
    else
		$PY_CMD requirements.py
        $PY_CMD main.py
    fi

    # The code only reaches here if the bot crashes or .update install triggers os._exit(0)
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${CYAN}🏮 Manual Reincarnation detected (.update install).${NC}"
    else
        echo -e "${RED}⚠️  Kurama took damage (Crash Exit Code: $EXIT_CODE).${NC}"
    fi

    echo -e "${YELLOW}⏳ Restoring Chakra in 3 seconds...${NC}"
    sleep 3
done
