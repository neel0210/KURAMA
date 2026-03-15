# database.py
import json
import os

DB_FILE = "user_stats.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_user_stats(user_id, username, download=False):
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {"username": username, "downloads": 0, "messages": 0}
    
    db[uid]["messages"] += 1
    if download:
        db[uid]["downloads"] += 1
    
    save_db(db)
    return db[uid]
