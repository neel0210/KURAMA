import os
import traceback
import logging
import sys
from telethon import events

# Initialize basic terminal logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("KuramaLogger")

# Load Log Chat ID from .env
LOG_CHAT = os.getenv("CHAT_ID")
if LOG_CHAT:
    try:
        LOG_CHAT = int(str(LOG_CHAT).strip())
    except ValueError:
        print("❌ Error: CHAT_ID in .env must be a number!")
        LOG_CHAT = None

async def report_error(client, context):
    """
    The Inner Eye: Reports errors to both the Terminal and the Log Chat.
    """
    error_trace = traceback.format_exc()
    
    # Print to terminal with high visibility
    print("\n" + "="*40)
    print(f"❌ KURAMA ERROR IN: {context}")
    print(error_trace)
    print("="*40 + "\n")
    sys.stdout.flush()
    
    if not LOG_CHAT:
        return

    # Telegram message construction
    # We trim the traceback to 3500 chars to stay safe under Telegram's 4096 limit
    clean_trace = error_trace[:3500]
    
    error_message = (
        "🦊 **Kurama's Inner Eye: Error Detected**\n"
        f"**Context:** `{context}`\n\n"
        "**Scroll of Error:**\n"
        f"```python\n{clean_trace}```"
    )
    
    try:
        await client.send_message(LOG_CHAT, error_message)
    except Exception as e:
        print(f"Failed to send log to Telegram: {e}")

def register(client):
    """Register the logging test jutsu."""
    @client.on(events.NewMessage(pattern=r'\.test_logs', outgoing=True))
    async def test_log(event):
        await event.edit("`Testing sensory link...` 🦊")
        try:
            # This variable does not exist, triggering a NameError
            return print(trigger_error_now)
        except Exception:
            await report_error(client, "Manual Log Test")
            await event.edit("`Sensory link active. Error reported to Log Chat.`")
            
            # Auto-delete the test message after 5 seconds to keep chat clean
            import asyncio
            await asyncio.sleep(5)
            await event.delete()