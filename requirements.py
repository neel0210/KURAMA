import subprocess
import sys
import os
import urllib.request

def is_termux():
    return "com.termux" in sys.executable or "TERMUX_VERSION" in os.environ

def is_venv():
    # True if running inside a virtual environment
    return sys.prefix != sys.base_prefix

def install_requirements():
    if not is_venv():
        print("⚠️  Warning: You are NOT in a virtual environment!")
        if is_termux():
            print("💡 Run: 'source .venv/bin/activate' first.")
        else:
            print("💡 Run: '.venv\\Scripts\\activate' (Windows) first.")

    # --- THE REMBG FIX ---
    # We use 'rembg' instead of 'rembg[pillow]' to avoid the dependency hang.
    packages = [
        "python-dotenv", "telethon", "python-barcode", 
        "pillow", "googletrans==4.0.0-rc1", "legacy-cgi", 
        "yt-dlp", "rembg", "onnxruntime"
    ]
    
    # psutil is a headache for Termux compilation
    if not is_termux():
        packages.append("psutil")
        print("🖥️  PC Detected: Adding psutil to the scroll...")
    else:
        print("📱 Termux Detected: Skipping psutil and forcing binary installs.")

    print(f"🦊 Kurama is gathering dependencies into: {sys.prefix}")
    
    for package in packages:
        try:
            # sys.executable ensures we use the pip belonging to the active .venv
            cmd = [sys.executable, "-m", "pip", "install", package]
            
            if is_termux():
                # --prefer-binary: Fixes the 'yt-dlp' and 'rembg' stuck issue
                # --no-cache-dir: Prevents corrupted downloads from previous hangs
                cmd.extend(["--prefer-binary", "--no-cache-dir", "--quiet"])
            else:
                cmd.append("--quiet")
            
            print(f"🌀 Installing {package}...")
            subprocess.check_call(cmd)
            print(f"✅ Installed: {package}")
        except Exception as e:
            print(f"❌ Failed to install {package}: {e}")

    # --- FONT DOWNLOAD ---
    font_url = "https://github.com/matomo-org/travis-scripts/raw/master/fonts/Arial.ttf"
    font_path = "kurama_font.ttf"
    
    if not os.path.exists(font_path):
        print("📜 Downloading Ink (Font)...")
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(font_url, font_path)
            print("✅ Font ready.")
        except Exception as e:
            print(f"⚠️ Font error: {e}")

    print("\n🔥 All systems ready.")

if __name__ == "__main__":
    try:
        install_requirements()
    except KeyboardInterrupt:
        print("\n🦊 Installation stopped by the Master.")
