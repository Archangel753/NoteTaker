import argparse
import json
import os
import sys

#!/usr/bin/env python3
"""
commands/delete.py

Delete notes stored in a JSON file. This mirrors a simple add.py-style
notes layout: notes are a list of objects in notes.json in the project root.

Usage:
    delete.py --title "My note title"
    delete.py --all [--yes]
"""


# notes.json is expected to live in the project root (one level above this commands folder)
NOTES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notes.json")


def load_notes(path):
        if not os.path.exists(path):
                return []
        with open(path, "r", encoding="utf-8") as f:
                try:
                        return json.load(f)
                except (json.JSONDecodeError, ValueError):
                        return []


def save_notes(path, notes):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
                json.dump(notes, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)


def delete_by_title(notes, title):
        title_lower = title.strip().lower()
        remaining = [n for n in notes if n.get("title", "").strip().lower() != title_lower]
        removed_count = len(notes) - len(remaining)
        return remaining, removed_count


def confirm(prompt):
        try:
                return input(f"{prompt} [y/N]: ").strip().lower() in ("y", "yes")
        except (KeyboardInterrupt, EOFError):
                return False


def main():
        p = argparse.ArgumentParser(description="Delete notes")
        group = p.add_mutually_exclusive_group(required=True)
        group.add_argument("--title", "-t", help="Title of the note to delete (exact match, case-insensitive)")
        group.add_argument("--all", action="store_true", help="Delete all notes")
        p.add_argument("--yes", "-y", action="store_true", help="Assume yes to confirmation prompts")
        args = p.parse_args()

        notes = load_notes(NOTES_FILE)

        if args.all:
                if not notes:
                        print("No notes to delete.")
                        return
                if not args.yes and not confirm(f"Are you sure you want to delete ALL ({len(notes)}) notes?"):
                        print("Aborted.")
                        return
                save_notes(NOTES_FILE, [])
                print(f"Deleted all notes ({len(notes)}).")
                return

        # delete by title
        remaining, removed = delete_by_title(notes, args.title)
        if removed == 0:
                print(f"No note found with title: {args.title!s}")
                sys.exit(1)
        if not args.yes and not confirm(f"Delete note titled '{args.title}'?"):
                print("Aborted.")
                return
        save_notes(NOTES_FILE, remaining)
        print(f"Deleted {removed} note(s) with title: {args.title!s}")


if __name__ == "__main__":
        main()