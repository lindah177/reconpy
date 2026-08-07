import socket
from datetime import datetime

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0  # True if port is open
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
            open_ports.append(port)
            print(f"  [OPEN]  Port {port}")

    print(f"\n{'='*50}")
    print(f"  Scan complete. {len(open_ports)} open port(s) found.")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    host = input("Enter target IP or hostname: ")
    start = int(input("Start port: "))
    end = int(input("End port: "))
    run_scan(host, start, end)