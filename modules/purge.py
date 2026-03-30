import asyncio
from telethon import events
from .logging import report_error  # Import our new logger

def register(client):
    @client.on(events.NewMessage(pattern=r'\.purge (\d+)', outgoing=True))
    async def tail_sweep(event):
        try:
            count = int(event.pattern_match.group(1))
            chat = await event.get_input_chat()
            
            # Collect messages
            messages = []
            async for msg in client.iter_messages(event.chat_id, limit=count + 1):
                messages.append(msg.id)
            
            # Delete in bulk
            await client.delete_messages(chat, messages)
            
            status = await client.send_message(event.chat_id, f"🦊 `{count} messages incinerated.`")
            await asyncio.sleep(2)
            await status.delete()

        except Exception:
            await report_error(client, "Purge Jutsu")
            await event.edit("`Tch. Purge failed. Check the logs.`")

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