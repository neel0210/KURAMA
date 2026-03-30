import os
import sys
import subprocess
import asyncio
from pathlib import Path
from telethon import events

# Pulling credentials from .env
GIT_TOKEN = os.getenv("GIT")
REPO_URL = "github.com/neel0210/kurama.git"

# --- THE PLURAL FIX: LOOKING FOR 'images' FOLDER ---
BASE_DIR = Path(__file__).parent.parent
IMG_UPDATE = BASE_DIR / "images" / "update_available.png"
IMG_NO_UPDATE = BASE_DIR / "images" / "update_not_available.png"

def register(client):
    @client.on(events.NewMessage(pattern=r'\.update(?:[ ]+([\w]+))?', outgoing=True))
    async def update_jutsu(event):
        arg = event.pattern_match.group(1)
        
        # 1. Setup authenticated remote
        if GIT_TOKEN:
            auth_url = f"https://{GIT_TOKEN}@{REPO_URL}"
            subprocess.run(["git", "remote", "set-url", "origin", auth_url], check=True, capture_output=True)

        status_msg = await event.edit("`🌀 Sensing for new Chakra on GitHub...` 📜")
        
        try:
            subprocess.run(["git", "fetch"], check=True, capture_output=True)
            status = subprocess.check_output(
                ["git", "rev-list", "HEAD..origin/main", "--count"]
            ).decode("utf-8").strip()

            # --- CASE: NO UPDATES FOUND ---
            if status == "0":
                if IMG_NO_UPDATE.exists():
                    caption_no = "🏮 **【 SYSTEM: PEAK CHAKRA 】**\n`No new jutsu detected. Your vault is current.`"
                    await client.send_file(event.chat_id, str(IMG_NO_UPDATE), caption=caption_no)
                    return await status_msg.delete()
                
                # Terminal Debug: If image still fails, check path in terminal
                print(f"DEBUG: No update image NOT found at: {IMG_NO_UPDATE}")
                return await event.edit("🏮 `No updates found. (Image missing in images/ folder)`")

            # --- CASE: UPDATE FOUND ---
            if not arg or arg != "install":
                if IMG_UPDATE.exists():
                    caption_up = (
                        f"🏮 **【 SYSTEM: NEW JUTSU DETECTED 】**\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"📜 **Status:** `{status} new scrolls available.`\n\n"
                        f"💡 **To Install:** Type `.update install`"
                    )
                    await client.send_file(event.chat_id, str(IMG_UPDATE), caption=caption_up)
                    return await status_msg.delete()
                
                print(f"DEBUG: Update available image NOT found at: {IMG_UPDATE}")
                return await event.edit(f"🏮 **Update Found!** `{status} scrolls available.`\n`Type .update install to upgrade.`")

            # --- CASE: UPDATE INSTALL ---
            if arg == "install":
                await event.edit("`🌀 Reincarnating Kurama with new scrolls...` 🦊")
                subprocess.check_output(["git", "pull"])
                await event.edit("✅ **Update Successful!**\n`Restarting now...` 🏮")
                await asyncio.sleep(2)
                await client.disconnect()
                os._exit(0)

        except Exception as e:
            print(f"Update Error: {e}")
            await event.edit(f"❌ `Sense Jutsu failed: {str(e)[:100]}`")
