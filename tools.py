# tools.py
import os
import platform
import subprocess
import yt_dlp
from pathlib import Path

# --- DYNAMIC ENVIRONMENT DETECTION ---
IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")
BASE_DIR = Path(__file__).resolve().parent

def get_ffmpeg_path():
    """Locates the correct ffmpeg binary based on the realm."""
    if IS_TERMUX:
        # In Termux, ffmpeg is usually in the standard path provided by the prefix
        return "ffmpeg" 
    if platform.system() == "Windows":
        # If you have ffmpeg.exe in your bot folder, use that
        local_ffmpeg = BASE_DIR / "ffmpeg.exe"
        return str(local_ffmpeg) if local_ffmpeg.exists() else "ffmpeg"
    return "ffmpeg"

def download_audio(url, bitrate="320"):
    """Extracts high-fidelity audio from YouTube."""
    # Ensure a 'downloads' folder exists to keep the scroll clean
    download_path = BASE_DIR / "downloads"
    download_path.mkdir(exist_ok=True)
    
    output_template = str(download_path / "%(title)s.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'ffmpeg_location': get_ffmpeg_path(),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': bitrate,
        }],
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            return True, file_path
    except Exception as e:
        return False, str(e)

def search_youtube(query, limit=5):
    """Scouts YouTube for the top targets."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
            results = []
            for entry in search_results.get('entries', []):
                results.append({
                    'id': entry.get('id'),
                    'title': entry.get('title'),
                    'url': f"https://www.youtube.com/watch?v={entry.get('id')}"
                })
            return True, results
    except Exception as e:
        return False, str(e)
