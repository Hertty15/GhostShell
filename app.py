from flask import Flask, render_template, request, jsonify
import subprocess
import os
import platform
import socket
import datetime
import hashlib
import secrets
import string
import time
import urllib.request
import re
import base64



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
        result = "===GHOSTSHELL COMMANDS===\n"
        result += "sysinfo                  - System reconnaissance\n"
        result += "clear                    - Clear terminal\n"
        result += "ghost                    - Stealth protocol\n"
        result += "help                     - Show this menu\n"
        result += "write [file] [text]      - Creat or edit a file\n"
        result += "read [file]              - Read the contents of a file\n"
        result += "hash [text]              - Generate a SHA-256 hash\n"
        result += "genpass [num]            - Generate a secure password\n"
        result += "trace [domain]           - Find a website's IP address\n"
        result += "fetch [url]              - Sniff a website's title\n"
        result += "encode [text]            - Encrypt text to Base64\n"
        result += "decode [text]            - Decrypt Base64 text\n"
        result += "exit                     - Disconnect\n"

    
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
    
    elif cmd.startswith("write "):
        parts=cmd.split(" ", 2)
        if len(parts)<3:
            return "[ERROR] Usage: write [filename] [text]"
        
        filename=parts[1]
        text=parts[2]

        if filename in ["app.py", "requirements.txt", "index.html"]:
            return "[ERROR] Access Denied: Cannot modify system files."
        
        try:
            with open(filename, "w") as f:
                f.write(text)
            return f"[SUCCESS] File '{filename}' created/updated successfully."
        except Exception as e:
            return f"[ERROR] Could not write file: {e}"
        
    elif cmd.startswith("read "):
        filename=cmd.split(" ",1)[1]
        try:
            with open(filename, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"[ERROR] File '{filename}' not found."
        
    elif cmd.startswith("hash "):
        text=cmd[5:]
        hashed=hashlib.sha256(text.encode('utf-8')).hexdigest()
        return f"[SHA-256 HASH]\n{hashed}"
    
    elif cmd.startswith("genpass "):
        try:
            length=int(cmd.split(" ")[1])
            #characters used to buld password
            alphabet=string.ascii_letters+string.digits+string.punctuation
            #use secrets for tru cryptographic randomnses
            password=''.join(secrets.choice(alphabet) for i in range(length))
            return f"[GENERATED PASSWORD]\n{password}"
        except ValueError:
            return "[ERROR]Please provide a number after genpass"
        
    #ip tracker
    elif cmd.startswith("trace "):
        domain=cmd[6:]
        try:
            #ask the internet dns for ip of the domain
            ip=socket.gethostbyname(domain)
            return f"[NETWORK TRACE]\nDomain: {domain}\nIP Address: {ip}"
        except socket.gaierror:
            return f"[ERROR] Could not find IP for '{domain}'. Check the domain name."
        
    #web fetcher
    elif cmd.startswith("fetch"):
        url=cmd[6:]
        if not url.startswith("http"):
            url="https://"+url
        try:
            req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html=urllib.request.urlopen(req).read().decode('utf-8')
            title_match=re.search('<title>(.*?)</title>', html, re.IGNORECASE)
            if title_match:
                title=title_match.group(1)
                return f"[SUCCESS] Fetched {url}\nTitle;{title}"
            return f"[INFO] Fetched {len(html)} bytes from {url}."
        except Exception as e:
            return f"[ERROR] Could not reach {url}."
        
    #encrypt/decrypt tools
    elif cmd.startswith("encode "):
        text=cmd[7:]
        encoded=base64.b64encode(text.encode('utf-8')).decode('utf-8')
        return f"[ENCODED] {encoded}"
    
    elif cmd.startswith("decode "):
        text=cmd[7:]
        try:
            decoded=base64.b64decode(text.encode('utf-8')).decode('utf-8')
            return f"[DECODED] {decoded}"
        except:
            return "[ERROR] Invalid Base64 string."

    
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