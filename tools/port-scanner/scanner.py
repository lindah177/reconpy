import socket
from datetime import datetime

def grab_banner(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        return banner.split("\n")[0]
    except (socket.timeout, socket.error, ConnectionRefusedError):
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
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"\n{'='*50}")
    print(f"  Target   : {host}")
    print(f"  Ports    : {start_port} - {end_port}")
    print(f"  Started  : {timestamp}")
    print(f"{'='*50}\n")

    open_ports = []

    for port in range(start_port, end_port + 1):
        print(f"  Scanning port {port}...", end="\r")
        if scan_port(host, port):
            banner = grab_banner(host, port)
            open_ports.append((port, banner))
            print(f"  [OPEN]  Port {port:<6} {banner}")

    # Save report to file
    report_filename = f"scan_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, 'w') as f:
        f.write(f"Port Scan Report\n")
        f.write(f"{'='*50}\n")
        f.write(f"Target  : {host}\n")
        f.write(f"Scanned : {timestamp}\n")
        f.write(f"Ports   : {start_port} - {end_port}\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"Open ports found: {len(open_ports)}\n\n")
        for port, banner in open_ports:
            f.write(f"Port {port:<6} {banner}\n")

    print(f"\n{'='*50}")
    print(f"  Scan complete. {len(open_ports)} open port(s) found.")
    print(f"  Report saved to: {report_filename}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Port scanner with banner grabbing for network reconnaissance"
    )
    parser.add_argument("host", help="Target IP or hostname")
    parser.add_argument("start", type=int, help="Start port number")
    parser.add_argument("end", type=int, help="End port number")
    
    args = parser.parse_args()
    
    run_scan(args.host, args.start, args.end)