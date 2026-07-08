from flask import Flask, render_template, request, jsonify
import subprocess
import os
import platform
import socket
import time
import datetime

app = Flask(__name__)

# Store command history
command_history = []

def get_sysinfo():
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "127.0.0.1"
    
    return {
        "OS": f"{platform.system()} {platform.release()}",
        "Device": platform.node(),
        "User": os.getlogin() if os.name == 'nt' else os.environ.get('USER', 'unknown'),
        "IP Address": ip,
        "Python": platform.python_version()
    }

def execute_command(cmd):
    """Execute a command and return the output"""
    result = ""
    
    # Built-in commands
    if cmd == "help":
        result = """
=== GHOSTSHELL COMMANDS ===
sysinfo    - System reconnaissance
clear      - Clear terminal
ghost      - Stealth protocol
help       - Show this menu
exit       - Disconnect

"""
    
    elif cmd == "sysinfo":
        info = get_sysinfo()
        result = "=== SYSTEM RECONNAISSANCE ===\n"
        for key, value in info.items():
            result += f"{key:12} : {value}\n"
        result += "============================="
    
    elif cmd == "ghost":
        result = "Initiating Ghost Protocol...\n"
        for i in range(1, 6):
            result += f"Bypassing firewall layer {i}/5...\n"
            time.sleep(0.1)  # Simulated delay
        result += "[SUCCESS] Ghost mode activated."
    
    elif cmd == "clear":
        result = "CLEAR"  # Special signal to clear the terminal
    
    elif cmd in ["exit", "quit"]:
        result = "GhostShell shutting down. Stay safe."
    
    else:
        # Try to execute as system command (limited for security)
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                result = result.stdout if result.stdout else result.stderr
            else:  # Linux/Mac
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                result = result.stdout if result.stdout else result.stderr
        except Exception as e:
            result = f"[ERROR] {str(e)}"
    
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    command = data.get('command', '')
    
    if not command:
        return jsonify({'output': '', 'clear': False})
    
    result = execute_command(command)
    if isinstance(result, dict) and result.get("action")=="open":
        return jsonify(result)
    should_clear=(result=="CLEAR")

    return jsonify({
        'output':result if not should_clear else '',
        'clear': should_clear
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
