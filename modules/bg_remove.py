import io
import asyncio
from PIL import Image
from rembg import remove
from telethon import events
from .logging import report_error

def register(client):
    @client.on(events.NewMessage(pattern=r'\.rbg', outgoing=True))
    async def remove_bg_jutsu(event):
        if not event.is_reply:
            return await event.edit("`Reply to an image to erase its background, brat!`")
        
        reply = await event.get_reply_message()
        if not reply.media:
            return await event.edit("`No visual chakra detected.`")

        await event.edit("`Erase Style: Dust Release Jutsu...` 💨")
        
        try:
            # 1. Download image
            photo_bytes = await reply.download_media(file=bytes)
            
            # 2. Process in a separate thread (it's heavy)
            def process():
                input_img = Image.open(io.BytesIO(photo_bytes))
                output_img = remove(input_img)
                out = io.BytesIO()
                output_img.save(out, format="PNG")
                out.seek(0)
                out.name = "kurama_no_bg.png"
                return out

            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, process)
            
            # 3. Send back
            await client.send_file(
                event.chat_id,
                result,
                force_document=True, # Sends as file to keep transparency
                reply_to=reply.id
            )
            await event.delete()

        except Exception as e:
            await report_error(client, "BG Remove")
            await event.edit(f"`The Eraser Seal failed: {str(e)[:40]}`")