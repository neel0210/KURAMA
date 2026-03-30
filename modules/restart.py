import os
import asyncio
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'\.restart', outgoing=True))
    async def restart_jutsu(event):
        # 1. Visual Feedback
        await event.edit("`🌀 Gathering Chakra for Reincarnation...` 🦊")
        await asyncio.sleep(2)
        
        # 2. Final Message
        await event.edit("✅ **Kurama is returning to the seal.**\n`Rebooting now...` 🏮")
        await asyncio.sleep(1)
        
        # 3. Clean Disconnect
        # This ensures the .session file is saved correctly before closing
        await client.disconnect()
        
        # 4. The Kill Switch
        # os._exit(0) triggers the 'while true' loop in your run.sh
        os._exit(0)
