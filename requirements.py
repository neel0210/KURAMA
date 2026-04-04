import os
import requests
import asyncio
from telethon import events
from dotenv import load_dotenv

# --- PATH CONFIGURATION ---
# Using absolute paths ensures compatibility with Termux environments
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("REMOVE_BG_API_KEY")

def register(client):
    @client.on(events.NewMessage(pattern=r"\.rbg"))
    async def remove_background(event):
        """
        Eraser Style Jutsu: Removes image backgrounds via API to save Termux RAM.
        """
        if not API_KEY:
            await event.edit("❌ **Error:** `REMOVE_BG_API_KEY` is missing from your `.env` file!")
            return

        if not event.reply_to_msg_id:
            await event.edit("🦊 **Usage:** Reply to a photo with `.rbg` to unseal it.")
            return

        reply_message = await event.get_reply_message()
        
        # Validate that the replied message contains a photo or an image document
        if not (reply_message.photo or (reply_message.document and "image" in reply_message.document.mime_type)):
            await event.edit("❌ **Error:** This Jutsu only works on image scrolls!")
            return

        await event.edit("🌀 **Eraser Style: Gathering Chakra...**")
        
        # Download media to the local Termux storage
        input_path = await reply_message.download_media()
        output_path = "kurama_no_bg.png"

        try:
            await event.edit("✨ **Eraser Style: Removing Background...**")
            
            # Use the API to offload heavy AI processing from the mobile CPU
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open(input_path, 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': API_KEY},
            )

            if response.status_code == requests.codes.ok:
                with open(output_path, 'wb') as out:
                    out.write(response.content)
                
                # Send the processed image back to the chat
                await client.send_file(
                    event.chat_id, 
                    output_path, 
                    caption="🔥 **Jutsu Complete: Background Erased!**",
                    reply_to=reply_message.id
                )
                await event.delete()
            else:
                error_msg = response.json().get('errors', [{}])[0].get('title', 'Unknown Error')
                await event.edit(f"❌ **Sealing Error:** {error_msg}")

        except Exception as e:
            await event.edit(f"❌ **System Failure:** {str(e)}")
        
        finally:
            # Clean up files immediately to keep the device storage clean
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
