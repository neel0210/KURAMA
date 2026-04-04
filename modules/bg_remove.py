import os
import requests
from telethon import events
from dotenv import load_dotenv

# Absolute pathing for Termux stability
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("REMOVE_BG_API_KEY")

def register(client):
    @client.on(events.NewMessage(pattern=r"\.rbg"))
    async def remove_bg(event):
        if not API_KEY:
            await event.edit("❌ **Error:** `REMOVE_BG_API_KEY` missing in `.env`!")
            return

        if not event.reply_to_msg_id:
            await event.edit("🦊 **Usage:** Reply to a photo with `.rbg`")
            return

        reply_message = await event.get_reply_message()
        if not reply_message.photo and not reply_message.document:
            await event.edit("❌ **Error:** Please reply to an image.")
            return

        await event.edit("🌀 **Extracting Background...**")
        
        # Download the image to a temporary path in Termux
        input_path = await reply_message.download_media()
        output_path = "kurama_no_bg.png"

        try:
            # Offload the heavy AI work to the API
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open(input_path, 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': API_KEY},
            )

            if response.status_code == requests.codes.ok:
                with open(output_path, 'wb') as out:
                    out.write(response.content)
                
                await client.send_file(
                    event.chat_id, 
                    output_path, 
                    caption="✨ **Eraser Style: Jutsu Complete!**",
                    reply_to=reply_message.id
                )
                await event.delete()
            else:
                await event.edit(f"❌ **API Error:** {response.json().get('errors')[0].get('title')}")

        except Exception as e:
            await event.edit(f"❌ **Failed:** {str(e)}")
        
        finally:
            # Clean up files to save storage on the device
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
