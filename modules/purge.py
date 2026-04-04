import asyncio
from telethon import events

# --- FIX: Removed the '.' from the import ---
# This assumes logging.py is in the same 'modules' folder
try:
    from logging import report_error 
except ImportError:
    # Fallback if logging isn't available or named differently
    async def report_error(client, name): pass

def register(client):
    """
    Tail Sweep Jutsu: Mass deletion of messages.
    Usage: .purge <number>
    """
    @client.on(events.NewMessage(pattern=r'\.purge (\d+)', outgoing=True))
    async def tail_sweep(event):
        try:
            # Parse the count from the command
            count = int(event.pattern_match.group(1))
            
            # Gather message IDs to delete (count + the .purge command itself)
            messages = []
            async for msg in client.iter_messages(event.chat_id, limit=count + 1):
                messages.append(msg.id)
            
            # Bulk delete for better performance and less API rate-limiting
            await client.delete_messages(event.chat_id, messages)
            
            # Send a temporary confirmation
            status = await client.send_message(event.chat_id, f"🦊 `{count} messages incinerated.`")
            await asyncio.sleep(2)
            await status.delete()

        except Exception:
            await report_error(client, "Purge Jutsu")
            await event.edit("`Tch. Purge failed. Check the logs.`")

    """
    Single Erase: Deletes the replied-to message.
    Usage: Reply to a message with .del
    """
    @client.on(events.NewMessage(pattern=r'\.del', outgoing=True))
    async def delete_one(event):
        if not event.is_reply:
            return await event.edit("`Reply to a message to erase it.`")
        
        try:
            reply = await event.get_reply_message()
            await reply.delete()
            await event.delete()
        except Exception:
            await report_error(client, "Single Delete")