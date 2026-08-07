import socket
from datetime import datetime

def grab_banner(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        # Some services need a nudge to respond
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        return banner.split("\n")[0]  # first line only
    except (socket.timeout,socket.error, ConnectionRefusedError):
        return "No banner"

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False

def run_scan(host, start_port, end_port):
    print(f"\n{'='*50}")
    print(f"  Target   : {host}")
    print(f"  Ports    : {start_port} - {end_port}")
    print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    open_ports = []

    for port in range(start_port, end_port + 1):
        print(f"  Scanning port {port}...", end="\r")
        if scan_port(host, port):
            banner = grab_banner(host, port)
            open_ports.append((port, banner))
            print(f"  [OPEN]  Port {port:<6} {banner}")

    print(f"\n{'='*50}")
    print(f"  Scan complete. {len(open_ports)} open port(s) found.")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    host = input("Enter target IP or hostname: ")
    start = int(input("Start port: "))
    end = int(input("End port: "))
    run_scan(host, start, end)