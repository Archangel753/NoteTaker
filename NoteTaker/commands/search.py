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
    
def search(args):
    if not args:
        print("Usage: search <query>")
        return

    query = " ".join(args).lower()
    notes = load_notes()
    
    results = [note for note in notes if query in note.get("title", "").lower() or query in note.get("content", "").lower()]
    
    if results:
        print(f"Found {len(results)} result(s) for '{query}':")
        for note in results:
            print(f"- {note.get('title', '')}")
    else:
        print(f"No results found for '{query}'.")

def run(args):
    search(args)
# This function is called when the command is executed
# It takes the command line arguments as input
# and performs the search operation