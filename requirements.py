import subprocess
import sys
import os
import urllib.request

def install_requirements():
    packages = [
        "python-dotenv", "psutil", "telethon", "python-barcode", 
        "pillow", "googletrans==4.0.0-rc1", "legacy-cgi", "yt-dlp", "rembg[pillow]", "onnxruntime"
    ]
    
    print("🦊 Kurama is gathering dependencies...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed: {package}")
        except Exception as e:
            print(f"❌ Failed to install {package}: {e}")

    # --- DOWNLOAD FONT FOR STICKERS ---
    font_url = "https://github.com/matomo-org/travis-scripts/raw/master/fonts/Arial.ttf"
    font_path = "kurama_font.ttf"
    
    if not os.path.exists(font_path):
        print("📜 Forging the Ink Brush (Downloading Font)...")
        try:
            urllib.request.urlretrieve(font_url, font_path)
            print("✅ Font 'kurama_font.ttf' is ready.")
        except Exception as e:
            print(f"⚠️ Could not download font: {e}. Defaulting to basic ink.")

    print("\n🔥 All systems ready. Ensure 'ffmpeg' and 'nodejs' are installed on your OS path.")

if __name__ == "__main__":
    install_requirements()