import os
import json
from commands.add import DATA_PATH

def load_notes():
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Warning: notes.json is corrupted or empty. Resetting...")
        return []
    
def read(args):
    if not args:
        print("Usage: read <note_title>")
        return

    title = " ".join(args).lower()
    notes = load_notes()

    for note in notes:
        if note.get("title", "").lower() == title:
            print(f"Title: {note.get('title', '')}")
            print(f"Content:\n{note.get('content', '')}")
            return
   
    print(f"No note found with title '{title}'.")
    
    
def run(args):
    read(args)

