import subprocess

def main():
    print("Welcome to GhostShell! (Type 'exit' to quit.)")

    #keeps the shell running
    while True:
        #show promt
        user_input = input("GhostShell> ")
        #check if user wants to exit
        if user_input.lower()=='exit':
            print("Exiting GhostShell. Goodbye!")
            break

        #execute the command
        try:
            #shell=true tells python to pass your text to windows
            subprocess.run(user_input, shell=True)
        except Exception as e:
            print(f"Error occurred: {e}")

#this tells python to run the main function when the script is executed
if __name__ == "__main__":
    main()