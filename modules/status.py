import os
import time
import psutil
import platform
from datetime import datetime
from telethon import events

# Record the start time when the module is loaded
start_time = time.time()

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

def register(client):
    @client.on(events.NewMessage(pattern=r'\.status', outgoing=True))
    async def status_check(event):
        # Calculate Uptime
        uptime = get_readable_time(int(time.time() - start_time))
        
        # System Info
        curr_os = platform.system()
        cpu_usage = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        
        # Formatting the message
        status_msg = (
            "🦊 **Kurama's Sensory Feedback**\n"
            "───\n"
            f"**Status:** `Active (Stable)`\n"
            f"**Uptime:** `{uptime}`\n"
            f"**Host OS:** `{curr_os}`\n"
            f"**CPU Load:** `{cpu_usage}%`\n"
            f"**Chakra (RAM):** `{ram.percent}% used`\n"
            "───\n"
            "`Hmph. Don't push me too hard, brat.`"
        )
        
        await event.edit(status_msg)