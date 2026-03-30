import subprocess
import sys
import os
import urllib.request

def is_termux():
    # Detection for Termux environment
    return "com.termux" in sys.executable or "TERMUX_VERSION" in os.environ

def is_venv():
    # Detects if the script is running inside a virtual environment
    return sys.prefix != sys.base_prefix

def install_requirements():
    if not is_venv():
        print("⚠️  Warning: You are NOT in a virtual environment!")
        if is_termux():
            print("💡 Run: 'source .venv/bin/activate' before running this script.")
        else:
            print("💡 Run: 'source .venv/Scripts/activate' (Windows) first.")
        # We continue anyway, but it's best practice to be in venv

    # The base list of Jutsu (packages)
    packages = [
        "python-dotenv", "telethon", "python-barcode", 
        "pillow", "googletrans==4.0.0-rc1", "legacy-cgi", 
        "yt-dlp", "rembg[pillow]", "onnxruntime"
    ]
    
    # --- TERMUX COMPATIBILITY SEAL ---
    if not is_termux():
        packages.append("psutil")
        print("🖥️  PC Detected: Adding psutil to the scroll...")
    else:
        print("📱 Termux Detected: Skipping psutil and using binary-only for heavy scrolls.")

    print(f"🦊 Kurama is gathering dependencies into: {sys.prefix}")
    
    for package in packages:
        try:
            # --- THE VENV FIX ---
            # Using sys.executable ensures we use the Python inside the .venv
            cmd = [sys.executable, "-m", "pip", "install", package, "--no-cache-dir"]
            
            # For Termux, we force binary to prevent hanging during compilation (especially for yt-dlp)
            if is_termux():
                cmd.append("--prefer-binary")
            
            # Keeping the terminal clean
            cmd.append("--quiet")
            
            subprocess.check_call(cmd)
            print(f"✅ Installed: {package}")
        except Exception as e:
            print(f"❌ Failed to install {package}: {e}")

    # --- DOWNLOAD FONT FOR STICKERS ---
    font_url = "https://github.com/matomo-org/travis-scripts/raw/master/fonts/Arial.ttf"
    font_path = "kurama_font.ttf"
    
    if not os.path.exists(font_path):
        print("📜 Forging the Ink Brush (Downloading Font)...")
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(font_url, font_path)
            print("✅ Font 'kurama_font.ttf' is ready.")
        except Exception as e:
            print(f"⚠️ Could not download font: {e}. Defaulting to basic ink.")

    print("\n🔥 All systems ready.")
    if is_termux():
        print("💡 Termux Tip: Ensure you ran 'pkg install ffmpeg nodejs' in the main terminal.")

if __name__ == "__main__":
    try:
        install_requirements()
    except KeyboardInterrupt:
        print("\n🦊 Installation interrupted.")
