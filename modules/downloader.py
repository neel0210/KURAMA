import os
import asyncio
import time
import yt_dlp
from telethon import events
from .logging import report_error

DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def get_chakra_bar(current, total, phase="Processing"):
    """Calculates Kunai trajectory with MB stats"""
    percentage = (current / total) * 100 if total > 0 else 0
    p = max(0, min(100, int(percentage)))
    
    current_mb = round(current / (1024 * 1024), 2)
    total_mb = round(total / (1024 * 1024), 2)
    
    total_width = 15 
    pos = int((p / 100) * total_width)
    trail = "🔥" * pos
    kunai = "🗡️"
    ahead = "☁️" * (total_width - pos)
    
    return (
        f"🦊 **Flying Thunder God: {phase}**\n"
        f"`🏁 {trail}{kunai}{ahead}` `{p}%`\n"
        f"**Chakra Flow:** `{current_mb}MB / {total_mb}MB`"
    )

class KuramaLogger:
    def __init__(self, event, loop, mode):
        self.event = event
        self.loop = loop
        self.mode = mode
        self.last_edit = 0

    def hook(self, d):
        if d['status'] == 'downloading':
            curr = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
            now = time.time()
            # Update every 4 seconds to avoid Telegram FloodWait
            if (now - self.last_edit > 4) or (curr == total):
                self.last_edit = now
                msg = get_chakra_bar(curr, total, phase=f"Extracting {self.mode}")
                asyncio.run_coroutine_threadsafe(self.event.edit(msg), self.loop)

def register(client):
    @client.on(events.NewMessage(pattern=r'\.dl (https?://\S+)', outgoing=True))
    async def video_dl(event): 
        await start_extraction(client, event, "video")

    @client.on(events.NewMessage(pattern=r'\.mp3 (https?://\S+)', outgoing=True))
    async def audio_dl(event): 
        await start_extraction(client, event, "audio")

async def start_extraction(client, event, mode):
    url = event.pattern_match.group(1)
    loop = asyncio.get_running_loop()
    progress = KuramaLogger(event, loop, mode)
    
    await event.edit("`Marking the target...` 🦊")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress.hook],
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    }

    if mode == "audio":
        # High Quality 320kbps MP3
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        })
        quality_tag = "320kbps"
    else:
        # Prioritize 1080p MP4, then 720p, then best available
        ydl_opts.update({
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        })
        quality_tag = "1080p/Best"

    try:
        # --- PHASE 1: DOWNLOAD ---
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))
            filename = ydl.prepare_filename(info)
            if mode == "audio":
                filename = os.path.splitext(filename)[0] + ".mp3"

        if not os.path.exists(filename):
            raise FileNotFoundError("Chakra leak! File not found after download.")

        # --- PHASE 2: UPLOAD ---
        file_size = os.path.getsize(filename)
        last_up = [0]

        async def up_cb(current, total):
            now = time.time()
            if now - last_up[0] > 4 or current == total:
                last_up[0] = now
                # Force the progress bar update for Uploading
                await event.edit(get_chakra_bar(current, total, phase="Teleporting Scroll"))

        # Manual edit to start the upload bar
        await event.edit(get_chakra_bar(0, file_size, phase="Teleporting Scroll"))

        await client.send_file(
            event.chat_id, 
            filename,
            caption=(
                f"🦊 **Extraction Successful**\n"
                f"**Title:** `{info.get('title')}`\n"
                f"**Quality:** `{quality_tag}`"
            ),
            reply_to=event.id,
            progress_callback=up_cb
        )

        # Cleanup: Erase the traces
        if os.path.exists(filename):
            os.remove(filename)
        await event.delete()

    except Exception as e:
        await report_error(client, f"Downloader ({mode})")
        await event.edit(f"`Jutsu failed: {str(e)[:50]}`")
        # Ensure cleanup on failure
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)