from zeroconf import ServiceInfo, Zeroconf
import socket
import platform
# Get LAN IP (replace en0 with your active interface, e.g., en1, eth0)
# Try to get local IP first by connecting to Google DNS
# Fall back to localhost if no internet connection
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
except:
    # If no internet, default to localhost
    local_ip = "127.0.0.1"

service_type = "_magicswitcher._tcp.local."
service_name = f"shubhams-Mac-mini.{service_type}"
service_port = 54123

#print hostname using platform.node()
print(f"Using hostname: {platform.node()}")
# Use the LAN IP and set the server field
info = ServiceInfo(
    type_=service_type,
    name=service_name,
    addresses=[socket.inet_aton(local_ip)],
    port=service_port,
    server="shubhams-Mac-mini.local.",  # Must match HostName
)

zeroconf = Zeroconf(interfaces=[local_ip])
zeroconf.register_service(info)
print(f"Advertising service: {service_name} at {local_ip}:{service_port}")
input("Press Enter to exit...\n")
zeroconf.unregister_service(info)
zeroconf.close()