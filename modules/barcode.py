import os
from telethon import events
import barcode
from barcode.writer import ImageWriter

def register(client):
    @client.on(events.NewMessage(pattern=r'\.barcode (.*)', outgoing=True))
    async def make_barcode(event):
        text = event.pattern_match.group(1)
        await event.edit("`Hmph. Fine, I'll seal this data for you...` ✨")
        
        try:
            code_class = barcode.get_barcode_class('code128')
            my_barcode = code_class(text, writer=ImageWriter())
            filename = "kurama_seal"
            my_barcode.save(filename)
            
            await client.send_file(
                event.chat_id, 
                'kurama_seal.png', 
                caption=f"**The seal is complete.**\nData: `{text}`",
                reply_to=event.id
            )
            
            if os.path.exists('kurama_seal.png'):
                os.remove('kurama_seal.png')
            await event.delete() 

        except Exception as e:
            await event.edit(f"**Tch. Error:** `{e}`")