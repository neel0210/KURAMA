import os
from telethon import events
from datetime import datetime

# Path to the image you saved
INFO_IMAGE = "kurama_seal.jpg"
# Your GitHub repository link
REPO_LINK = "https://github.com/neel0210/kurama.git"

def register(client):
    @client.on(events.NewMessage(pattern=r'\.info', outgoing=True))
    async def info_jutsu(event):
        # Brief update to show the command is working
        await event.edit("`Unrolling the Forbidden Scroll...` 📜")
        
        me = await client.get_me()
        
        # --- SHINOBI DATA-BOOK: MINIMALIST STYLE ---
        info_caption = (
            f"🏮 **【 KURAMA S-RANK DATA-BOOK 】** 🏮\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🥷 **SHINOBI:** [{me.first_name}](tg://user?id={me.id})\n"
            f"⚔️ **RANK:** `S-Class Rogue / Userbot`\n"
            f"🧧 **VILLAGE:** `Hidden in the Cloud` (Digital)\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            
            f"💡 **DO** `.help` **TO KNOW MORE**\n\n"
            
            f"📜 **FORBIDDEN SOURCE SCROLL**\n"
            f"• [Access Source Code]({REPO_LINK})\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🦊 *“True strength is found in the code that is hidden.”*"
        )
        
        try:
            if os.path.exists(INFO_IMAGE):
                # Send the image with the caption
                await client.send_file(
                    event.chat_id, 
                    INFO_IMAGE, 
                    caption=info_caption,
                    reply_to=event.id
                )
                # Remove the .info command text
                await event.delete()
            else:
                # Fallback to text if the image file is missing
                await event.edit(info_caption)
                
        except Exception as e:
            # Fallback if there's an error sending the file
            await event.edit(f"❌ `Seal Error: {str(e)[:40]}`\n\n{info_caption}")