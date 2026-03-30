from googletrans import Translator
from telethon import events
from .logging import report_error

translator = Translator()

def register(client):
    @client.on(events.NewMessage(pattern=r'\.tr (.*)', outgoing=True))
    async def translate_jutsu(event):
        if not event.is_reply:
            return await event.edit("`Reply to a scroll (message) to translate it.`")
        
        dest_lang = event.pattern_match.group(1).strip()
        reply_msg = await event.get_reply_message()
        
        try:
            result = translator.translate(reply_msg.text, dest=dest_lang)
            
            output = (
                "🦊 **Translation Seal**\n"
                f"**From:** `{result.src.upper()}`\n"
                f"**To:** `{dest_lang.upper()}`\n"
                "───\n"
                f"{result.text}"
            )
            await event.edit(output)
        except Exception:
            await report_error(client, "Translation Jutsu")
            await event.edit("`I couldn't decipher those markings...` 🦊")