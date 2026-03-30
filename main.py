import sys
import os
import glob
import importlib
import asyncio

# --- PYTHON 3.14 COMPATIBILITY PATCH ---
# Modern Python (3.13+) removed the 'cgi' module. 
# This shim ensures older libraries like googletrans still work.
try:
    import cgi
except ImportError:
    try:
        import legacy_cgi as cgi
        sys.modules['cgi'] = cgi
    except ImportError:
        # If legacy-cgi isn't installed, run: pip install legacy-cgi
        pass

from telethon import TelegramClient
from dotenv import load_dotenv

# --- LOAD ENVIRONMENT ---
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Safety check for credentials
if not API_ID or not API_HASH:
    print("❌ Error: API_ID or API_HASH not found in .env file!")
    sys.exit(1)

# Ensure API_ID is a clean integer
try:
    API_ID = int(API_ID.strip())
except ValueError:
    print("❌ Error: API_ID must be a number!")
    sys.exit(1)

client = TelegramClient('kurama_session', API_ID, API_HASH)

def load_modules():
    """
    Dynamically loads all Python files in the /modules folder.
    """
    # Look for .py files inside the 'modules' directory
    path = os.path.join("modules", "*.py")
    files = glob.glob(path)
    
    for name in files:
        # Cross-platform way to get module name (modules.filename)
        # Removes the .py extension and converts path separators to dots
        module_path = name.replace(".py", "").replace(os.sep, ".")
        
        # Skip __init__ files
        if "__init__" in module_path:
            continue
            
        try:
            # Import the module
            module = importlib.import_module(module_path)
            
            # Check for the 'register' function defined in our Jutsu modules
            if hasattr(module, "register"):
                module.register(client)
                # Success message using just the filename (e.g., 'status')
                print(f"✅ Loaded Jutsu: {module_path.split('.')[-1]}")
        except Exception as e:
            print(f"❌ Failed to load {module_path}: {e}")

async def main():
    print("🦊 Kurama's chakra is gathering...")
    
    # Start the client (Will ask for phone/code if kurama_session.session is missing)
    await client.start()
    
    # Load all the modules from the folder
    load_modules()
    
    # Get bot info to confirm login
    me = await client.get_me()
    print(f"🔥 Kurama is fully awake as: {me.first_name}")
    print("✨ Bot is active. Type .status in any chat to test.")
    
    # Keep the bot running
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        # Modern Python 3.11+ way to run the loop
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🦊 Kurama is returning to the seal... (Stopped)")