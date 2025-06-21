import json
import os

# Variables

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "notes.json"))

# Functions

####################################################################################
# ____________.                                                __
# | __________|                              ______       ____|  |____
# | |_____                    _             /. ____|     |____    ____|
# |  _____|       _     _    | |_____      /. /               |. |
# | |            | |   | |   |  ___  \.   |. |                |  | 
# | |            | |___| |   | |   | |     \. \____           |  |
# |_|             \_____/    |_|   |_|.     \______|          |. |
###################################################################################

def load_notes():
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Warning: notes.json is corrupted or empty. Resetting...")
        return []


def save_notes(notes):
    with open(DATA_PATH, "w") as f:
        json.dump(notes, f, indent=4)

def add_note(title, content, public):
    notes = load_notes()
    notes.append({"title": title, "content": content, "public": public})
    save_notes(notes)
    print(f"✅ Note '{title}' added.")

#############################################
# |\.    /|.
# |. \. / |.          _________.    |\.    |.
# |.  \/  |.              |.        |.\.   |.
# |.      |.   /\.        |.        |. \.  |.
# |.      |.  /. \.       |.        |.  \. |.
# |.      |. /----\.      |.        |.   \.|.
# |.      | /.     \. ____|____.    |.    \|.
#############################################


def run(args):
    if not args:
        print("Usage: add <note_title> [public|private]")
        return

    # Check if last argument is 'public' or 'private'
    if args[-1].lower() in ("public", "private"):
        visibility = args[-1].lower()
        title = " ".join(args[:-1])
    else:
        visibility = None
        title = " ".join(args)

    if not title:
        print("Usage: add <note_title> [public|private]")
        return

    print("Enter your note content (type DONE on a new line to finish):")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)

    content = "\n".join(lines)

    if visibility in ("public", "private"):
        public = visibility == "public"
    else:
        while True:
            visibility = input("Is this note public or private? (public/private): ").strip().lower()
            if visibility in ("public", "private"):
                public = visibility == "public"
                break
            else:
                print("Please enter 'public' or 'private'.")

    add_note(title, content, public)
