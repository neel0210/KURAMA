import os
import time
import platform
from datetime import datetime
from telethon import events

# Attempt to import psutil (will fail on Termux)
try:
    import psutil
except ImportError:
    psutil = None

# Record the start time when the module is loaded
start_time = time.time()

def get_readable_time(seconds: int) -> str:
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]
    while count < 4:
        count += 1
        if count < 3:
            seconds, result = divmod(seconds, 60)
        else:
            seconds, result = divmod(seconds, 24)
        time_list.append(f"{int(result)}{time_suffix_list[count-1]}")
        if seconds == 0: break
    time_list.reverse()
    return ":".join(time_list)

def register(client):
    @client.on(events.NewMessage(pattern=r'\.status', outgoing=True))
    async def status_check(event):
        # Calculate Uptime
        uptime = get_readable_time(int(time.time() - start_time))
        curr_os = platform.system()
        
        # --- SYSTEM SENSORY LOGIC ---
        if psutil:
            # PC/Windows Logic
            cpu_usage = f"{psutil.cpu_percent()}%"
            ram = f"{psutil.virtual_memory().percent}% used"
        else:
            # Termux/Android Logic
            cpu_usage = "Not available on Android"
            ram = "Not available on Android"
        
        # Formatting the message
        status_msg = (
            "🦊 **Kurama's Sensory Feedback**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"**Status:** `Active (Stable)`\n"
            f"**Uptime:** `{uptime}`\n"
            f"**Host OS:** `{curr_os}`\n"
            f"**CPU Load:** `{cpu_usage}`\n"
            f"**Chakra (RAM):** `{ram}`\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "`Hmph. Don't push me too hard, brat.`"
        )
        
        await event.edit(status_msg)
