import json
import os
from telethon import events

NOTES_FILE = "kurama_notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)

def register(client):
    # Save a note: .save [keyword] [text]
    @client.on(events.NewMessage(pattern=r'\.save (\w+) (.*)', outgoing=True))
    async def save_jutsu(event):
        keyword = event.pattern_match.group(1)
        text = event.pattern_match.group(2)
        notes = load_notes()
        notes[keyword] = text
        save_notes(notes)
        await event.edit(f"🦊 **Scroll Stored:** `{keyword}` has been sealed.")

    # Get a note: .get [keyword]
    @client.on(events.NewMessage(pattern=r'\.get (\w+)', outgoing=True))
    async def get_jutsu(event):
        keyword = event.pattern_match.group(1)
        notes = load_notes()
        if keyword in notes:
            await event.edit(notes[keyword])
        else:
            await event.edit(f"`Tch. No scroll found for '{keyword}', brat.`")

    # List all notes: .notes
    @client.on(events.NewMessage(pattern=r'\.notes', outgoing=True))
    async def list_notes(event):
        notes = load_notes()
        if not notes:
            return await event.edit("`The archive is empty.`")
        
        msg = "📜 **Kurama's Archived Scrolls:**\n"
        for k in notes.keys():
            msg += f"• `{k}`\n"
        await event.edit(msg)