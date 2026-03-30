import os
import shutil
import glob
from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'\.clean', outgoing=True))
    async def clear_workspace(event):
        await event.edit("`Hmph. Cleaning the battlefield...` 🧹")
        
        folders_to_clean = ['downloads']
        files_to_clean = ['*.png', '*.jpg', '*.mp3', '*.mp4', 'kurama_session.log']
        
        count = 0
        
        # Clean folders
        for folder in folders_to_clean:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                            count += 1
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                            count += 1
                    except Exception as e:
                        print(f'Failed to delete {file_path}. Reason: {e}')

        # Clean stray files in root
        for pattern in files_to_clean:
            for f in glob.glob(pattern):
                try:
                    os.remove(f)
                    count += 1
                except:
                    pass

        await event.edit(f"🦊 **Battlefield Cleaned.**\n`{count} traces of chakra erased.`")
        import asyncio
        await asyncio.sleep(3)
        await event.delete()