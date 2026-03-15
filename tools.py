# tools.py
import yt_dlp
import os
import yt_dlp
from config import DOWNLOAD_DIR

def search_youtube(query, max_results=5):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Search logic
            results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)['entries']
            return True, results
        except Exception as e:
            return False, str(e)

def download_audio(input_str, bitrate="320"):
    """
    Extracts audio from a URL or search query at a specific bitrate.
    """
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # High-quality options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': bitrate,
        }, {
            'key': 'FFmpegMetadata',
        }],
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }

    # If it's not a link, search YouTube for the best match
    if not input_str.startswith(('http://', 'https://')):
        input_str = f"ytsearch1:{input_str}"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(input_str, download=True)
            # Handle list vs single result
            video_info = info['entries'][0] if 'entries' in info else info
            
            filename = ydl.prepare_filename(video_info)
            base, _ = os.path.splitext(filename)
            final_path = f"{base}.mp3"
            
            return True, final_path
    except Exception as e:
        return False, str(e)
