import subprocess
import sys
import os
import urllib.request

def run_cmd(cmd):
    """Utility to run shell commands and catch errors."""
    try:
        subprocess.check_call(cmd, shell=isinstance(cmd, str))
        return True
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return False

def is_termux():
    return "com.termux" in sys.executable or "TERMUX_VERSION" in os.environ

def setup_termux_environment():
    """Installs the necessary system binaries for ARM64 Python wheels."""
    print("🛠️ Preparing Termux environment for C++ compilation...")
    # These are required to build psutil and Pillow from source on Android
    termux_pkgs = [
        "pkg", "upgrade", "-y", "&&", "pkg", "install", 
        "python", "binutils", "build-essential", "clang", 
        "libjpeg-turbo", "libpng", "libwebp", "libffi", "openssl", "-y"
    ]
    run_cmd(" ".join(termux_pkgs))

def install_requirements():
    print(f"🦊 Environment: {'📱 Termux' if is_termux() else '🖥️ PC'}")
    
    if is_termux():
        setup_termux_environment()

    # Core requirements list
    packages = [
        "python-dotenv", "telethon", "python-barcode", 
        "pillow", "googletrans==4.0.0-rc1", "legacy-cgi", 
        "yt-dlp", "rembg", "onnxruntime", "psutil"
    ]

    print(f"🌀 Gathering dependencies into: {sys.prefix}")
    
    for package in packages:
        # --prefer-binary saves time; --no-build-isolation helps with termux env vars
        pip_cmd = [sys.executable, "-m", "pip", "install", package, "--prefer-binary"]
        if is_termux():
            pip_cmd.append("--no-cache-dir")
        
        print(f"📦 Installing {package}...")
        run_cmd(pip_cmd)

    # --- FONT DOWNLOAD ---
    font_path = os.path.join(os.path.dirname(__file__), "kurama_font.ttf")
    if not os.path.exists(font_path):
        print("📜 Downloading Ink (Font)...")
        try:
            url = "https://github.com/matomo-org/travis-scripts/raw/master/fonts/Arial.ttf"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(font_path, 'wb') as out_file:
                out_file.write(response.read())
            print("✅ Font ready.")
        except Exception as e:
            print(f"⚠️ Font error: {e}")

    print("\n🔥 All systems unsealed and ready.")

if __name__ == "__main__":
    try:
        install_requirements()
    except KeyboardInterrupt:
        print("\n🦊 Installation stopped.")
