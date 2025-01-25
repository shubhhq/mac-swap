from zeroconf import ServiceBrowser, Zeroconf
import requests
import json
import socket
import subprocess

# Load config
with open('config.json') as f:
    config = json.load(f)

# Get peripheral addresses
print("Detecting connected peripherals...")
keyboard = subprocess.check_output(["blueutil", "--paired"]).decode()
keyboard = keyboard.split('\n')[0].split()[1]
pointer = subprocess.check_output(["blueutil", "--paired"]).decode()
pointer = [l for l in pointer.split('\n') if 'mouse' in l.lower() or 'trackpad' in l.lower()][0].split()[1]

# Format addresses
keyboard_formatted = keyboard.replace('-', ':').strip(',')
pointer_formatted = pointer.replace('-', ':').strip(',')

print(f"Keyboard: {keyboard_formatted}")
print(f"Pointer: {pointer_formatted}")

class TrustedDeviceListener:
    def __init__(self):
        self.trusted_services = []

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            hostname = name.split(".")[0]
            if hostname in config["trusted_devices"]:
                ip = socket.inet_ntoa(info.addresses[0])
                token = info.properties.get(b"token").decode()
                self.trusted_services.append({"ip": ip, "token": token, "name": hostname})
                print(f"Found trusted device: {hostname} at {ip}")

    # Add update_service method to fix the FutureWarning
    def update_service(self, zeroconf, type, name):
        pass

def send_trigger(target_ip, token):
    try:
        response = requests.post(
            f"http://{target_ip}:54123/trigger",
            headers={
                "X-Token": token,
                "X-Keyboard": keyboard_formatted,
                "X-Mouse": pointer_formatted
            },
            timeout=2
        )
        print(f"Trigger sent to {target_ip}: {response.text}")
    except Exception as e:
        print(f"Failed to send trigger: {e}")

# Discover trusted devices
zeroconf = Zeroconf()
listener = TrustedDeviceListener()
browser = ServiceBrowser(zeroconf, "_magicswitcher._tcp.local.", listener)

# Prompt user to select a device
if not listener.trusted_services:
    print("No trusted devices found.")
else:
    print("\nTrusted Devices:")
    for i, service in enumerate(listener.trusted_services):
        print(f"{i + 1}. {service['name']} ({service['ip']})")
    
    choice = int(input("Select a device: ")) - 1
    target = listener.trusted_services[choice]
    send_trigger(target["ip"], target["token"])

zeroconf.close()