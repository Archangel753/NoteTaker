import os
import importlib
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMANDS_DIR = os.path.join(BASE_DIR, "commands")

# store lower-case to allow case-insensitive matching via user_input.lower()
SPECIAL_COMMAND_VALENTINE = "its me, president funny valentine"

def load_commands():
    commands = {}
    for filename in os.listdir(COMMANDS_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            full_path = os.path.join(COMMANDS_DIR, filename)

            # Load module dynamically
            spec = importlib.util.spec_from_file_location(f"commands.{module_name}", full_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "run"):
                commands[module_name] = module.run
    return commands

def main(welcome_message=None):
    if welcome_message:
        print(welcome_message)
    print("Welcome to NoteTaker!")
    print("Type 'help' to see available commands. Type 'exit' to quit. Example note, 'hello'\n")

    commands = load_commands()

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            if user_input.lower() == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                if welcome_message:
                    print(welcome_message)
                print("Welcome to NoteTaker!")
                print("Type 'help' to see available commands. Type 'exit' to quit. Example note, 'hello'\n")
                continue
            if user_input.lower() == SPECIAL_COMMAND_VALENTINE:
                print("dirty deeds done dirt cheap")
                continue
            parts = user_input.split()
            cmd = parts[0]
            args = parts[1:]

            # Easter egg: print a special message for the "acdc" command
            if cmd.lower() == "FunnyValentine".lower():
                print("dirty deeds done dirt cheap")
                continue
            if cmd.lower() == "Dio".lower():
                print("WRYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
                continue
            if cmd.lower() == "Jotaro".lower():
                print("Yare yare daze...")
                continue
            if cmd.lower() == "Gyro".lower():
                print("I, Gyro Zeppeli, have come to kick some ass!")
                continue
            if cmd.lower() == "Star-Platinum".lower():
                print("Star Platinum: The World!")
                continue

            if cmd in commands:
                commands[cmd](args)
            elif cmd == "help":
                print("\nAvailable commands:")
                for name in sorted(commands.keys()):
                    print(f" - {name}")
                print(" - clear")
                print(" - help")
                print(" - exit\n")
            else:
                print(f"Unknown command: {cmd}")
        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    welcome_message = """ 

  _   _       _        _______        _     
 | \ | |     | |      |__   __|      | |           
 |  \| | ___ | |_ __     | |   __ _  | |___  __    _____
 | . ` |/ _ \| __/ _ \   | | /  _` | | |___ / _ \ |  ___|
 | |\  | (_) | ||  __/   | | | (_| | | |\ \|. __/ | |
 |_| \_|\___/ \__\____|  |_|  \__,_| |_| \_|\____|| |     """
    
    main(welcome_message=welcome_message)
