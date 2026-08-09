# Port Scanner Project — Portfolio Writeup

## Overview

Built a **command-line port scanner in Python** that performs network reconnaissance by identifying open ports, grabbing service banners, and generating timestamped reports. This is the first tool in my cybersecurity portfolio and demonstrates understanding of network fundamentals, socket programming, and security tooling.

**Repository:** [reconpy/tools/port-scanner](https://github.com/lindah177/reconpy)

---

## The Problem

Network reconnaissance is the first phase of any security engagement. A penetration tester needs to know:
- Which ports are open on a target?
- What services are running on those ports?
- What versions are they?

This tool automates that discovery process, which would otherwise be done manually or with expensive commercial tools like Nmap.

---

## What the Tool Does

```bash
$ python3 scanner.py scanme.nmap.org 1 1024 -j
```

1. **Port scanning** — Attempts TCP connection to each port in range
2. **Service identification** — Looks up port number against known services
3. **Banner grabbing** — Sends HTTP HEAD request and captures response
4. **Reporting** — Saves both text and JSON outputs with timestamp

### Example Output

```
============================================================
  Port Scanner - Network Reconnaissance
============================================================
  Target       : scanme.nmap.org (45.33.32.156)
  Port Range   : 1 - 1024
  Scan Started : 2025-01-09 14:30:22
============================================================

  [1/1024] Scanning port 1...
  [OPEN]  Port 22     SSH             ssh-2.0-openssh_6.6.1p1 ubuntu-2ubuntu2.13
  [OPEN]  Port 53     DNS             No banner
  [OPEN]  Port 80     HTTP            http/1.1 200 ok

============================================================
  Scan Complete
  Open Ports Found: 3
============================================================

  Text report saved: scan_scanme.nmap.org_20250109_143022.txt
  JSON report saved : scan_scanme.nmap.org_20250109_143022.json
```

---

## Security Concepts Demonstrated

### 1. Network Sockets

The tool uses Python's `socket` library to establish TCP connections — the foundation of network communication:

```python
def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0
```

This is what every network tool does under the hood. Understanding sockets is critical for security work.

### 2. Banner Grabbing

Services often respond with identifying information when you connect. The tool captures this:

```python
sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
```

In a real pentest, this might reveal outdated software versions vulnerable to known exploits.

### 3. Service Enumeration

Maintaining a port-to-service database lets the tool identify what's running:

```python
COMMON_SERVICES = {
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    # ... etc
}
```

This is the start of building intelligence about a target.

### 4. Error Handling

Network operations fail unpredictably. The tool handles timeouts, connection refusals, and invalid input gracefully:

```python
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except (socket.timeout, socket.error, ConnectionRefusedError):
    return "No banner"
```

Real security tools need bulletproof error handling.

---

## Key Design Decisions

### CLI Arguments vs. User Prompts

Used `argparse` to accept command-line arguments:
```bash
python3 scanner.py <target> <start_port> <end_port> [-j]
```

**Why:** Real tools are scriptable. This lets users chain commands, automate scans, and integrate with other tools.

### Timeout Management

Set `sock.settimeout(1)` for port scans and `sock.settimeout(2)` for banner grabbing:
- **1 second** for connection attempts → fast, reasonable
- **2 seconds** for banner grabbing → services are slower to respond

**Why:** Balances speed with reliability. Too short = false negatives. Too long = tool is slow.

### Dual Output Formats

Saves both text and JSON:
- **Text** — human-readable reports for documentation
- **JSON** — machine-readable for automation and further analysis

**Why:** Penetration testing reports need both formats.

---

## What I Learned

1. **Socket programming is foundational** — every network tool is built on TCP/UDP sockets
2. **Service identification matters** — knowing the version of SSH or Apache can mean the difference between exploitable and patched
3. **Error handling is not optional** — network operations fail constantly and gracefully
4. **Timing and timeouts are critical** — set them wrong and you either get false results or waste time
5. **Real tools are scriptable** — CLI arguments > user prompts for any automation-heavy work

---

## Testing & Validation

Tested against `scanme.nmap.org` — a legitimate target hosted by Nmap for exactly this purpose.

Findings:
- Port 22 (SSH) — OpenSSH 6.6.1, Ubuntu 12.04
- Port 53 (DNS) — No banner (DNS doesn't respond to HTTP probes)
- Port 80 (HTTP) — HTTP/1.1 server responding

All findings verified against known Nmap output — no false positives.

---

## Limitations & Next Steps

### Current Limitations
- TCP only (no UDP scanning yet)
- Single-threaded (scans are sequential, not parallel)
- No service fingerprinting beyond banners
- Limited to basic HTTP service detection

### Next Steps
1. **Multi-threading** — scan 100 ports in parallel instead of sequentially
2. **UDP scanning** — services like DNS, SNMP, NTP use UDP
3. **Service fingerprinting** — match banners against known vulnerability databases
4. **Stealth options** — add timing options, packet fragmentation for IDS evasion
5. **Output formats** — CSV, XML for integration with vulnerability scanners

---

## How This Fits Into My Journey

This project represents **Phase 1: Foundations** in my cybersecurity roadmap:

✅ Hands-on network programming
✅ Understanding of common ports and services  
✅ Real security tool, not a tutorial exercise
✅ Demonstrated Python proficiency
✅ Experience with error handling and edge cases

The next project will build on this — adding more sophisticated detection, moving to vulnerability scanning, then to active exploitation.

---

## Repository

Full code, README, and usage examples: https://github.com/lindah177/reconpy/tree/main/tools/port-scanner

---

**Built:** July 2026
**Language:** Python 3.10
**Time to completion:** ~1 week
**Lines of code:** ~150 (core logic)