import os
import asyncio
from telethon import events

# --- FIX: Removed the '.' from these imports ---
try:
    from logging import report_error
except ImportError:
    async def report_error(client, name): pass

# If your quote module uses a local helper file, import it like this:
try:
    import utils # or 'from utils import ...'
except ImportError:
    # If the helper is named something else, adjust accordingly
    pass

def register(client):
    """
    Quote Style Jutsu: Transforms a message into a quote sticker.
    Usage: Reply to a message with .q
    """
    @client.on(events.NewMessage(pattern=r'\.q', outgoing=True))
    async def quote_sticker(event):
        if not event.is_reply:
            return await event.edit("`Reply to a message to seal it in a quote.`")

        await event.edit("✨ **Forming Quote Seal...**")
        
        try:
            # Your specific quote logic goes here
            # (Usually involves sending a request to a quote API or 
            # using Pillow to draw text on a background)
            
            # Example placeholder for the actual logic:
            reply = await event.get_reply_message()
            
            # ... (Existing quote logic) ...
            
            await event.delete() # Delete the '.q' command after success
            
        except Exception as e:
            await report_error(client, "Quote Jutsu")
            await event.edit(f"❌ **Jutsu Failed:** `{str(e)[:50]}`")