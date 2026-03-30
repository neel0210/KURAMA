import os
import sys
import subprocess
import asyncio
from telethon import events

# Pulling credentials from .env
GIT_TOKEN = os.getenv("GIT")
REPO_URL = "github.com/neel0210/kurama.git"

# Path to your new stickers
IMG_UPDATE = "image/update_available.png"
IMG_NO_UPDATE = "image/update_not_available.png"

def register(client):
    @client.on(events.NewMessage(pattern=r'\.update(?:[ ]+([\w]+))?', outgoing=True))
    async def update_jutsu(event):
        arg = event.pattern_match.group(1)
        
        # 1. Setup authenticated remote for GitHub
        if GIT_TOKEN:
            auth_url = f"https://{GIT_TOKEN}@{REPO_URL}"
            subprocess.run(["git", "remote", "set-url", "origin", auth_url], check=True)

        await event.edit("`🌀 Sensing for new Chakra on GitHub...` 📜")
        
        try:
            # 2. Fetch changes to see what's new
            subprocess.run(["git", "fetch"], check=True)
            
            # Count commits between local and remote
            status = subprocess.check_output(
                ["git", "rev-list", "HEAD..origin/main", "--count"]
            ).decode("utf-8").strip()

            # --- CASE: NO UPDATES FOUND ---
            if status == "0":
                if os.path.exists(IMG_NO_UPDATE):
                    await client.send_file(event.chat_id, IMG_NO_UPDATE, reply_to=event.id)
                return await event.edit("🏮 **【 SYSTEM: PEAK CHAKRA 】**\n`No new jutsu detected. Your vault is current.`")

            # --- CASE: UPDATE FOUND (Check Mode) ---
            if not arg or arg != "install":
                if os.path.exists(IMG_UPDATE):
                    await client.send_file(event.chat_id, IMG_UPDATE, reply_to=event.id)
                return await event.edit(
                    f"🏮 **【 SYSTEM: NEW JUTSU DETECTED 】**\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"📜 **Status:** `{status} new scrolls available.`\n\n"
                    f"💡 **To Install:** Type `.update install`"
                )

            # --- CASE: UPDATE INSTALL ---
            if arg == "install":
                await event.edit("`🌀 Reincarnating Kurama with new scrolls...` 🦊")
                
                # Pull the changes from GitHub
                pull_output = subprocess.check_output(["git", "pull"]).decode("utf-8")
                
                await event.edit(f"✅ **Update Successful!**\n`{pull_output[:50]}...` \n\n`Restarting now...`")
                await asyncio.sleep(2)
                
                # RESTART JUTSU: Replacing process inside .venv
                os.execl(sys.executable, sys.executable, *sys.argv)

        except Exception as e:
            await event.edit(f"❌ `Sense Jutsu failed: {str(e)[:50]}`")