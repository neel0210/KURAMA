#!/bin/bash

# --- KURAMA UNIVERSAL STARTUP SCRIPT ---
echo "🏮 Initializing Kurama S-Rank Interface..."

# 1. Detect Environment
OS_TYPE="$(uname -s)"
case "${OS_TYPE}" in
    Linux*)     ENV="Linux";;
    Darwin*)    ENV="MacOS";;
    *)          ENV="Unknown/Android";;
esac

echo "🌍 Realm Detected: $ENV"

# 2. Create Virtual Environment if it doesn't exist
if [ ! -d "kurama_env" ]; then
    echo "⚙️ Creating a new Virtual Environment..."
    python3 -m venv kurama_env
fi

# 3. Activate the Environment
echo "🔌 Awakening the environment..."
source kurama_env/bin/activate

# 4. Install/Update Requirements
if [ -f "requirements.txt" ]; then
    echo "📦 Gathering components (requirements.txt)..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found! Installing core components manually..."
    pip install python-telegram-bot qrcode[pil] yt-dlp requests psutil
fi

# 5. Start the Bot
echo "🔥 Starting Kurama Professional Grade..."
python3 main.py
