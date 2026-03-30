import os
import io
import textwrap
import asyncio
import logging
from PIL import Image, ImageDraw, ImageFont
from telethon import events, functions, types

# Using your existing logging
logger = logging.getLogger("KURAMA_KANG")

FONT_FILE = "kurama_font.ttf"

async def resize_to_sticker(photo_bytes):
    """Ensures media fits the 512px sticker requirement."""
    img = Image.open(io.BytesIO(photo_bytes))
    if img.mode != "RGBA": 
        img = img.convert("RGBA")
    
    width, height = img.size
    # Telegram requirement: one side must be 512px, the other 512px or less
    if width > height:
        new_w, new_h = 512, int(512 * height / width)
    else:
        new_h, new_w = 512, int(512 * width / height)
        
    img = img.resize((new_w, new_h), Image.LANCZOS)
    out = io.BytesIO()
    img.save(out, "PNG")
    out.seek(0)
    out.name = "sticker.png"
    return out

def register(client):
    @client.on(events.NewMessage(pattern=r'\.kang(?:[ ]+([^ ]+))?(?:[ ]+([\w]+))?', outgoing=True))
    async def kang_jutsu(event):
        if not event.is_reply: 
            return await event.edit("`Reply to a target, brat!` 🦊")
        
        reply = await event.get_reply_message()
        if not reply.media: 
            return await event.edit("`No chakra detected in that message.`")

        # pattern_match.group(1) is emoji, (2) is pack name
        emoji = event.pattern_match.group(1) or "🤔"
        pack_name = event.pattern_match.group(2) or "main"
        
        await event.edit(f"`Absorbing into {pack_name} vault...` 🌀")

        try:
            me = await client.get_me()
            # UNIQUE SHORT NAME: Uses your ID to prevent 'Name Taken' errors
            pack_short = f"K_{me.id}_{pack_name}" 
            pack_title = f"🦊 Kurama Vault: {pack_name}"

            # Download and Resize
            photo = await reply.download_media(file=bytes)
            sticker_f = await resize_to_sticker(photo)

            async with client.conversation("@Stickers") as conv:
                # Try adding to existing pack
                await conv.send_message("/addsticker")
                await conv.get_response()
                await conv.send_message(pack_short)
                res = await conv.get_response()

                if "Choose the sticker" in res.text:
                    # PACK EXISTS: Proceed with adding
                    await conv.send_file(sticker_f, force_document=True)
                    await conv.get_response()
                    await conv.send_message(emoji)
                    await conv.get_response()
                    await conv.send_message("/done")
                    await conv.get_response()
                else:
                    # PACK DOES NOT EXIST: Create New
                    await event.edit("`Vault not found. Creating new Scroll...` 📜")
                    await conv.send_message("/cancel") # Reset state
                    await conv.get_response()
                    
                    await conv.send_message("/newpack")
                    await conv.get_response()
                    await conv.send_message(pack_title)
                    await conv.get_response()
                    await conv.send_file(sticker_f, force_document=True)
                    await conv.get_response()
                    await conv.send_message(emoji)
                    await conv.get_response()
                    await conv.send_message("/publish")
                    await conv.get_response()
                    await conv.send_message("/skip") # No icon
                    await conv.get_response()
                    
                    # THIS IS THE CRITICAL PART: The Unique Short Name
                    await conv.send_message(pack_short)
                    final_res = await conv.get_response()
                    
                    if "short name is already taken" in final_res.text:
                        # Fallback: add a random microsecond if ID isn't enough
                        from datetime import datetime
                        pack_short += f"_{datetime.now().microsecond}"
                        await conv.send_message(pack_short)
                        await conv.get_response()

            await event.edit(f"🦊 **Sealed!**\n[View Vault](https://t.me/addstickers/{pack_short})")
            
        except Exception as e:
            logger.error(f"Kang failed: {e}")
            await event.edit(f"❌ `Seal Failed: {str(e)[:50]}`")

    @client.on(events.NewMessage(pattern=r'\.stext (.*)', outgoing=True))
    async def stext_jutsu(event):
        text = event.pattern_match.group(1)
        await event.edit("`Inking text into sticker...` ✍️")
        
        def create_text_sticker():
            img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype(FONT_FILE, 45)
            except:
                font = ImageFont.load_default()
            
            lines = textwrap.wrap(text, width=15)
            y = (512 - (len(lines) * 55)) // 2
            for line in lines:
                # Modern PIL text centering
                left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
                w = right - left
                draw.text(((512 - w) // 2, y), line, font=font, fill="white", stroke_width=3, stroke_fill="black")
                y += 55
            
            out = io.BytesIO()
            img.save(out, format="WEBP")
            out.seek(0)
            out.name = "sticker.webp"
            return out

        loop = asyncio.get_running_loop()
        sticker = await loop.run_in_executor(None, create_text_sticker)
        await client.send_file(event.chat_id, sticker, reply_to=event.id)
        await event.delete()
