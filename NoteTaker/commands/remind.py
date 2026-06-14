import os
import json 
from datetime import datetime, timedelta


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "reminders.json")


def load_reminders():
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Warning: reminders.json is corrupted or empty. Resetting...")
        return []
    

def save_reminders(reminders):
    with open(DATA_PATH, "w") as f:
        json.dump(reminders, f, indent=4)


def add_reminder(title, content, due_date):
    reminders = load_reminders()
    reminders.append({
        "title": title,
        "content": content,
        "due_date": due_date.isoformat()
    })
    save_reminders(reminders)
    print(f"✅ Reminder '{title}' added for {due_date.strftime('%Y-%m-%d %H:%M:%S')}.")


def list_reminders():
    reminders = load_reminders()
    if not reminders:
        print("No reminders found.")
        return
    print("Reminders:")
    for reminder in reminders:
        due_date = datetime.fromisoformat(reminder["due_date"])
        print(f"- {reminder['title']} (Due: {due_date.strftime('%Y-%m-%d %H:%M:%S')})")


def run(args):
    if not args:
        print("Usage: remind <add/list> [options]")
        return

    command = args[0].lower()
    
    if command == "add":
        if len(args) < 3:
            print("Usage: remind add <title> <content> [due_date (YYYY-MM-DD HH:MM:SS)]")
            return
        title = args[1]
        if len(args) > 3:
            due_date_str = " ".join(args[-2:])
            content = " ".join(args[2:-2])
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD HH:MM:SS.")
                return
        else:
            content = args[2]
            due_date = datetime.now() + timedelta(days=1)  # Default to 1 day from now

        add_reminder(title, content, due_date)
    
    elif command == "list":
        list_reminders()
    
    else:
        print(f"Unknown command: {command}")
