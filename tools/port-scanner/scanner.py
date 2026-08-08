import socket
import json
from datetime import datetime
import argparse
import sys

# Common port-to-service mapping
COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP Proxy",
    8443: "HTTPS Alt",
    27017: "MongoDB",
    6379: "Redis",
}

def resolve_hostname(host):
    """Resolve hostname to IP, return original if already IP"""
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        print(f"[ERROR] Could not resolve hostname: {host}")
        sys.exit(1)

def get_service_name(port):
    """Look up service name from port number"""
    return COMMON_SERVICES.get(port, "Unknown")

def grab_banner(host, port):
    """Attempt to grab service banner from open port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        return banner.split("\n")[0] if banner else "No banner"
    except (socket.timeout, socket.error, ConnectionRefusedError):
        return "No banner"

def scan_port(host, port):
    """Test if port is open via TCP connection"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False

def run_scan(host, start_port, end_port, output_json=False):
    """Run port scan and optionally save JSON output"""
    
    # Resolve hostname to IP
    target_ip = resolve_hostname(host)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"\n{'='*60}")
    print(f"  Port Scanner - Network Reconnaissance")
    print(f"{'='*60}")
    print(f"  Target       : {host} ({target_ip})")
    print(f"  Port Range   : {start_port} - {end_port}")
    print(f"  Scan Started : {timestamp}")
    print(f"{'='*60}\n")

    open_ports = []

    # Validate port range
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("[ERROR] Invalid port range. Use 1-65535.")
        sys.exit(1)

    port_count = end_port - start_port + 1
    
    for i, port in enumerate(range(start_port, end_port + 1)):
        progress = f"{i+1}/{port_count}"
        print(f"  [{progress}] Scanning port {port}...", end="\r")
        
        if scan_port(target_ip, port):
            banner = grab_banner(target_ip, port)
            service = get_service_name(port)
            open_ports.append({
                "port": port,
                "service": service,
                "banner": banner
            })
            print(f"  [OPEN]  Port {port:<6} {service:<15} {banner}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"  Scan Complete")
    print(f"  Open Ports Found: {len(open_ports)}")
    print(f"{'='*60}\n")

    # Save text report
    txt_filename = f"scan_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(txt_filename, 'w') as f:
        f.write(f"Port Scan Report\n")
        f.write(f"{'='*60}\n")
        f.write(f"Target       : {host} ({target_ip})\n")
        f.write(f"Scanned      : {timestamp}\n")
        f.write(f"Port Range   : {start_port} - {end_port}\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"Open Ports: {len(open_ports)}\n\n")
        f.write(f"{'Port':<8} {'Service':<20} {'Banner':<40}\n")
        f.write(f"{'-'*68}\n")
        for result in open_ports:
            f.write(f"{result['port']:<8} {result['service']:<20} {result['banner']:<40}\n")
    
    print(f"  Text report saved: {txt_filename}")

    # Save JSON report if requested
    if output_json:
        json_filename = f"scan_{host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_filename, 'w') as f:
            json.dump({
                "target": host,
                "target_ip": target_ip,
                "timestamp": timestamp,
                "port_range": {"start": start_port, "end": end_port},
                "open_ports_count": len(open_ports),
                "open_ports": open_ports
            }, f, indent=2)
        print(f"  JSON report saved : {json_filename}")

    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Port scanner with banner grabbing for network reconnaissance"
    )
    parser.add_argument("host", help="Target IP or hostname")
    parser.add_argument("start", type=int, help="Start port number (1-65535)")
    parser.add_argument("end", type=int, help="End port number (1-65535)")
    parser.add_argument("-j", "--json", action="store_true", 
                        help="Also save results as JSON")
    
    args = parser.parse_args()
    
    try:
        run_scan(args.host, args.start, args.end, output_json=args.json)
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        sys.exit(0)