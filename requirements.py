import subprocess
import sys
import os
import urllib.request

def is_termux():
    # Detection for Termux environment
    return "com.termux" in sys.executable or "TERMUX_VERSION" in os.environ

def install_requirements():
    # The base list of Jutsu (packages)
    packages = [
        "python-dotenv", "telethon", "python-barcode", 
        "pillow", "googletrans==4.0.0-rc1", "legacy-cgi", 
        "yt-dlp", "rembg[pillow]", "onnxruntime"
    ]
    
    # --- TERMUX COMPATIBILITY SEAL ---
    # We only add psutil if we are NOT on Termux
    if not is_termux():
        packages.append("psutil")
        print("🖥️  PC Detected: Adding psutil to the scroll...")
    else:
        print("📱 Termux Detected: Skipping psutil to avoid compilation errors.")

    print("🦊 Kurama is gathering dependencies...")
    
    for package in packages:
        try:
            # Using -q to keep the terminal clean
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            print(f"✅ Installed: {package}")
        except Exception as e:
            print(f"❌ Failed to install {package}: {e}")

    # --- DOWNLOAD FONT FOR STICKERS ---
    font_url = "https://github.com/matomo-org/travis-scripts/raw/master/fonts/Arial.ttf"
    font_path = "kurama_font.ttf"
    
    if not os.path.exists(font_path):
        print("📜 Forging the Ink Brush (Downloading Font)...")
        try:
            # Adding a User-Agent to prevent 403 Forbidden errors
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            
            urllib.request.urlretrieve(font_url, font_path)
            print("✅ Font 'kurama_font.ttf' is ready.")
        except Exception as e:
            print(f"⚠️ Could not download font: {e}. Defaulting to basic ink.")

    print("\n🔥 All systems ready.")
    if is_termux():
        print("💡 Termux Tip: Run 'pkg install ffmpeg nodejs' if you haven't already.")
    else:
        print("💡 Ensure 'ffmpeg' and 'nodejs' are installed on your OS path.")

if __name__ == "__main__":
    install_requirements()
