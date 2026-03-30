import os
import io
import textwrap
import asyncio
from PIL import Image, ImageDraw, ImageFont
from telethon import events
from .logging import report_error

DOWNLOAD_DIR = "downloads"
FONT_FILE = "kurama_font.ttf"

async def resize_to_sticker(photo_bytes):
    """Ensures media fits the 512px sticker requirement."""
    img = Image.open(io.BytesIO(photo_bytes))
    if img.mode != "RGBA": img = img.convert("RGBA")
    
    width, height = img.size
    aspect = width / height
    if width > height:
        new_w, new_h = 512, int(512 / aspect)
    else:
        new_h, new_w = 512, int(512 * aspect)
        
    img = img.resize((new_w, new_h), Image.LANCZOS)
    out = io.BytesIO()
    img.save(out, "PNG")
    out.seek(0)
    return out

def register(client):
    @client.on(events.NewMessage(pattern=r'\.kang(?:[ ]+([\w]+))?(?:[ ]+([\w]+))?', outgoing=True))
    async def kang_jutsu(event):
        if not event.is_reply: return await event.edit("`Reply to a target, brat!`")
        reply = await event.get_reply_message()
        if not reply.media: return await event.edit("`No chakra detected.`")

        emoji = event.pattern_match.group(1) or "🤔"
        pack_name = event.pattern_match.group(2) or "main"
        await event.edit(f"`Sealing into {pack_name}...` 🦊")

        try:
            me = await client.get_me()
            pack_short = f"Kurama_{pack_name}_{me.id}"
            photo = await reply.download_media(file=bytes)
            sticker_f = await resize_to_sticker(photo)
            sticker_f.name = "sticker.png"

            async with client.conversation("@Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                await conv.send_message(pack_short)
                res = await conv.get_response()

                if "Choose the sticker" in res.text:
                    await conv.send_file(sticker_f, force_document=True)
                    await conv.get_response()
                    await conv.send_message(emoji)
                    await conv.get_response()
                    await conv.send_message("/done")
                    await conv.get_response()
                else:
                    await event.edit("`Creating Vault...` 📜")
                    await conv.send_message("/newpack")
                    await conv.get_response()
                    await conv.send_message(f"Kurama Vault: {pack_name}")
                    await conv.get_response()
                    await conv.send_file(sticker_f, force_document=True)
                    await conv.get_response()
                    await conv.send_message(emoji)
                    await conv.get_response()
                    await conv.send_message("/publish")
                    await conv.get_response()
                    await conv.send_message("/skip")
                    await conv.get_response()
                    await conv.send_message(pack_short)
                    await conv.get_response()

            await event.edit(f"🦊 **Sealed!**\n[Vault Link](https://t.me/add_stickers/{pack_short})")
        except Exception:
            await report_error(client, "Kang")

    @client.on(events.NewMessage(pattern=r'\.stext (.*)', outgoing=True))
    async def stext_jutsu(event):
        text = event.pattern_match.group(1)
        await event.edit("`Inking...` ✍️")
        
        def create_text_sticker():
            img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            try: font = ImageFont.truetype(FONT_FILE, 45)
            except: font = ImageFont.load_default()
            
            lines = textwrap.wrap(text, width=15)
            y = (512 - (len(lines) * 55)) // 2
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                draw.text(((512 - (bbox[2]-bbox[0])) // 2, y), line, font=font, fill="white", stroke_width=2, stroke_fill="black")
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