from flask import Flask, request
import subprocess
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

app = Flask(__name__)

@app.route('/trigger', methods=['POST'])
def trigger():
    # Verify token
    token = request.headers.get("X-Token")
    if token != config["secret_token"]:
        return "Unauthorized", 401
    
    # Get peripheral addresses from headers
    keyboard = request.headers.get("X-Keyboard")
    mouse = request.headers.get("X-Mouse")
    
    # Disconnect peripherals first
    subprocess.run(["blueutil", "--disconnect", keyboard])
    subprocess.run(["blueutil", "--disconnect", mouse])
    
    # Connect peripherals
    subprocess.run(["blueutil", "--connect", keyboard])
    subprocess.run(["blueutil", "--connect", mouse])
    
    return "Peripherals connected!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=54123)