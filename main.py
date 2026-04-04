import sys
import os
import glob
import importlib
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

# --- ABSOLUTE PATHING ---
# Ensures the bot finds its scrolls even if launched via symlink or Tasker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_PATH = os.path.join(BASE_DIR, "modules")

# --- TERMUX WAKE-LOCK ---
def ensure_wakelock():
    if "com.termux" in sys.executable:
        print("📱 Termux detected. Requesting Chakra stability (Wake Lock)...")
        os.system("termux-wake-lock")

# --- PYTHON 3.14 COMPATIBILITY PATCH ---
try:
    import cgi
except ImportError:
    try:
        import legacy_cgi as cgi
        sys.modules['cgi'] = cgi
    except ImportError:
        pass

# --- LOAD ENVIRONMENT ---
load_dotenv(os.path.join(BASE_DIR, ".env"))
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

if not API_ID or not API_HASH:
    print("❌ Error: API_ID or API_HASH missing from .env!")
    sys.exit(1)

# Persistent session file in the base directory
SESSION_PATH = os.path.join(BASE_DIR, 'kurama_session')
client = TelegramClient(SESSION_PATH, int(API_ID), API_HASH)

def load_modules():
    """
    Dynamically loads all Jutsu from the modules folder using absolute paths.
    """
    search_path = os.path.join(MODULES_PATH, "*.py")
    files = glob.glob(search_path)
    
    for name in files:
        module_name = os.path.basename(name).replace(".py", "")
        if module_name.startswith("__"):
            continue
            
        try:
            # Create a spec and load it directly to avoid sys.path issues
            spec = importlib.util.spec_from_file_location(module_name, name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "register"):
                module.register(client)
                print(f"✅ Loaded Jutsu: {module_name}")
        except Exception as e:
            print(f"❌ Failed to load {module_name}: {e}")

async def main():
    print("🦊 Kurama's chakra is gathering...")
    ensure_wakelock()
    
    await client.start()
    load_modules()
    
    me = await client.get_me()
    print(f"🔥 Kurama is fully awake as: {me.first_name}")
    print("✨ Bot is active. Termux is locked to prevent sleep.")
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🦊 Kurama is returning to the seal...")
