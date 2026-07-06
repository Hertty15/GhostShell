import subprocess
import os
import webbrowser
import platform
import socket
import time
import datetime

def main():
    shell_name="GhostShell"
    print(f"Establishing connection to {shell_name}...[SYSTEM ONLINE]")
    print("Type 'help' for a list of commands. Type exit to leave")

    while True:
        #get time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        #show time in prompt
        user_input = input(f"[{current_time}] {shell_name}> ")

        parts=user_input.split()

        if not parts:
            continue

        command=parts[0].lower()
        args=" ".join(parts[1:])

        #CUSTOM COMMANDS
        if command=="exit":
            print("Exiting GhostShell...")
            break

        elif command=="clear":
            os.system('cls')

        elif command=="help":
            print("Available commands:")
            print("exit      - Exit the shell")
            print("clear     - Clear the screen")
            print("sysinfo   - Display system information")
            print("ghost     - Special command for GhostShell")
            print("open[url] - Open a URL in the default web browser")
            print("---------------------------------------------")
            print("Standard Windows commands still work.")

        elif command=="sysinfo":
            print("System Information:")
            print(f"OS         : {platform.system()} {platform.release()}")
            print(f"Device     : {platform.node()}")
            print(f"User       : {os.getlogin()}")
            #get IP address
            try:
                ip=socket.gethostbyname(socket.gethostname())
            except socket.gaierror:
                ip="127.0.0.1"
            print(f"IP Adress  : {ip}")
            print("-----------------------------------\n")

        elif command=="ghost":
            print("/nI7ia1izin6 Gh05t2h3l1... [SY2T3M 0NL1N3]\n")
            time.sleep(0.5)
            for i in range(1, 6):
                print(f"8ypas2ing s3curi7y 1ay3r {i}...")
                time.sleep(0.4) #pauses code to make it look like its doing something
            print("[SUCCESS] 5y5t3m 0v3rr1d3d. 4cce55 gr4nt3d.\n")

        elif command.startswith("open") and args:
            if "." not in args:
                args += ".com"
            if not args.startswith("http"):
                args = "http:" + args
                webbrowser.open(args)
                print(f"Opening {args} in the default web browser...\n")


        #WINDOWS PASS THROUGH
        else:
            try:
                subprocess.run(user_input, shell=True)
            except Exception as e:
                print(f"Error executing command: {e}")

if __name__ == "__main__":
    main()