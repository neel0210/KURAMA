import os
import io
import textwrap
import asyncio
from PIL import Image, ImageDraw, ImageFont
from telethon import events
from .logging import report_error

FONT_FILE = "kurama_font.ttf"

def get_circle_avatar(avatar_bytes):
    """Crops a profile pic into a clean shinobi circle."""
    img = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
    img = img.resize((100, 100), Image.LANCZOS)
    mask = Image.new("L", (100, 100), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 100, 100), fill=255)
    output = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask=mask)
    return output

def register(client):
    @client.on(events.NewMessage(pattern=r'\.q', outgoing=True))
    async def quote_jutsu(event):
        await event.edit("`Replicating QuotLy Seal...` 🌀")
        target = await event.get_reply_message() if event.is_reply else event
        user = await client.get_entity(target.sender_id)
        
        photo = await client.download_profile_photo(user, file=bytes)
        avatar_img = get_circle_avatar(photo) if photo else None

        def create_quotly_style():
            # 1. Setup Fonts
            try:
                name_f = ImageFont.truetype(FONT_FILE, 26)
                text_f = ImageFont.truetype(FONT_FILE, 24)
            except:
                name_f = text_f = ImageFont.load_default()

            # 2. Process Text & Calculate Bubble Width
            msg = target.text or "[Media/Sticker]"
            lines = textwrap.wrap(msg, width=30)
            
            # Find the longest line to determine bubble width
            max_line_width = 0
            for line in lines:
                bbox = text_f.getbbox(line)
                max_line_width = max(max_line_width, bbox[2] - bbox[0])
            
            bubble_width = max(250, max_line_width + 60)
            bubble_height = (len(lines) * 32) + 90
            
            # 3. Create Canvas
            canvas_w, canvas_h = 600, bubble_height + 100
            canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(canvas)
            
            # 4. Draw Bubble with Tail
            bx, by = 130, 30
            # Rounded Rectangle
            draw.rounded_rectangle(
                [bx, by, bx + bubble_width, by + bubble_height], 
                radius=25, fill=(30, 30, 30, 255)
            )
            # The Tail (triangle)
            draw.polygon([(bx, by+40), (bx-15, by+30), (bx, by+20)], fill=(30, 30, 30, 255))
            
            # 5. Paste Avatar
            if avatar_img:
                canvas.paste(avatar_img, (15, 30), avatar_img)
            
            # 6. Draw Name (Telegram Blue) and Text
            name = (user.first_name or "Shinobi")
            draw.text((bx + 25, by + 15), name, font=name_f, fill=(0, 136, 204, 255))
            
            y_offset = by + 55
            for line in lines:
                draw.text((bx + 25, y_offset), line, font=text_f, fill="white")
                y_offset += 32

            # Final Save as WEBP Sticker
            out = io.BytesIO()
            canvas.save(out, format="WEBP")
            out.seek(0)
            out.name = "quote.webp"
            return out

        try:
            loop = asyncio.get_running_loop()
            sticker = await loop.run_in_executor(None, create_quotly_style)
            await client.send_file(event.chat_id, sticker, reply_to=target.id)
            await event.delete()
        except Exception as e:
            await report_error(client, "QuotLy Clone")
            await event.edit(f"`Seal failed: {str(e)[:40]}`")