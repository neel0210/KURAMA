from googletrans import Translator
from telethon import events

# --- FIX: Removed the '.' from the import ---
try:
    from logging import report_error
except ImportError:
    async def report_error(client, name): pass

# Initialize translator
translator = Translator()

def register(client):
    """
    Translation Jutsu: Deciphers scrolls into different languages.
    Usage: Reply to a message with .tr <language_code> (e.g., .tr hi, .tr ja)
    """
    @client.on(events.NewMessage(pattern=r'\.tr (.*)', outgoing=True))
    async def translate_jutsu(event):
        if not event.is_reply:
            return await event.edit("`Reply to a scroll (message) to translate it.`")
        
        # Target language (e.g., 'en', 'hi', 'ja')
        dest_lang = event.pattern_match.group(1).strip()
        if not dest_lang:
            dest_lang = "en" # Default to English if no lang code provided
            
        reply_msg = await event.get_reply_message()
        if not reply_msg or not reply_msg.text:
            return await event.edit("`The scroll is blank (no text found).`")
        
        await event.edit("`Deciphering markings...` 🦊")
        
        try:
            # googletrans 3.1.0a0 is sync-based, but we run it in executor for safety
            import asyncio
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: translator.translate(reply_msg.text, dest=dest_lang))
            
            output = (
                "🦊 **Translation Seal**\n"
                f"**From:** `{result.src.upper()}`\n"
                f"**To:** `{dest_lang.upper()}`\n"
                "───\n"
                f"{result.text}"
            )
            await event.edit(output)
            
        except Exception as e:
            await report_error(client, "Translation Jutsu")
            await event.edit(f"`I couldn't decipher those markings: {str(e)[:50]}` 🦊")