import subprocess
import os
import webbrowser

def main():
    shell_name="GhostShell"
    print(f"Welcome to {shell_name}!(Type 'help' to see commands, 'exit' to quit)")

    while True:
        user_input=input(f"{shell_name}> ")
        #this cuts sentence into words
        #eg: "open youtube" becomes ["open", "youtube"]
        parts=user_input.split()

        #if u press enter without anything else do nothing
        if not parts:
            continue

        command=parts[0].lower()#first word like "open" or "exit"
        args=" ".join(parts[1:])#rest of the words

        #CUSTOM COMMANDS
        if command=="exit":
            print(f"Exiting {shell_name}...")
            break

        elif command=="clear":
            os.system('cls')#clear the entire screen (for windows)

        elif command=="help":
            print("Available commands:")
            print("  open <url> - Open a URL in the default web browser")
            print("  clear - Clear the screen")
            print("  exit - Exit the shell")
            print("--------------------------------------------")
            print("You can also run any system command directly, like 'dir' or 'calc'.")

        elif command=="open" and args:
            #if u type open youtube it adds .com (try to make it smarter)
            if"." not in args:
                args+=".com"
            if not args.startswith("http"):
                args="http://"+args
            
            webbrowser.open(args)
            print(f"Opening {args} in the default web browser...")

        #WINDOWS PASS THROUGH
        else:
            #if its not custom command let windwos handle it
            try:
                subprocess.run(user_input, shell=True)
            except Exception as e:
                print(f"Error executing command: {e}")

if __name__ == "__main__":
    main()