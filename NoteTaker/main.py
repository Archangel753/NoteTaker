import os
import sys
import importlib
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMANDS_DIR = os.path.join(BASE_DIR, "commands")

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

def main():
    print("Welcome to NoteTaker!")
    print("Type 'help' to see available commands. Type 'exit' to quit.\n")

    commands = load_commands()

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            parts = user_input.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd in commands:
                commands[cmd](args)
            elif cmd == "help":
                print("\nAvailable commands:")
                for name in sorted(commands.keys()):
                    print(f" - {name}")
                print(" - help")
                print(" - exit\n")
            else:
                print(f"Unknown command: {cmd}")
        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
