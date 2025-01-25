from zeroconf import ServiceInfo, Zeroconf
import socket
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

# Get local IP
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Advertise service
service_type = "_magicswitcher._tcp.local."
service_name = f"{hostname}.{service_type}"
service_port = 54123

info = ServiceInfo(
    service_type,
    service_name,
    addresses=[socket.inet_aton(local_ip)],
    port=service_port,
    properties={"token": config["secret_token"]},  # Share token for verification
)

zeroconf = Zeroconf()
zeroconf.register_service(info)
print(f"Advertising service: {service_name}")
input("Press Enter to exit...\n\n")
zeroconf.unregister_service(info)
zeroconf.close()