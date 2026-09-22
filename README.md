WTC-DCW5F95J
# Reconpy — Security Reconnaissance Toolkit

A practical cybersecurity portfolio project building three Python tools for **network reconnaissance, vulnerability assessment, and web application security**.

> **Status:** Phase 1 Complete — 3 working tools | **Timeline:** Aug 9 - Sept 25, 2025

---

## Overview

Reconpy demonstrates hands-on security skills by building real tools that work together in a complete reconnaissance workflow:

```
Port Scanner
    ↓ (finds services)
Vulnerability Scanner
    ↓ (identifies risks)
Web Reconnaissance Tool
    ↓ (web-level analysis)
Security Assessment Report
```

Each tool solves a real problem in penetration testing and security assessment.

---

## The Three Tools

### 1. Port Scanner — Network Discovery

**Location:** `tools/port-scanner/`

Performs TCP port scanning and service identification on a target.

```bash
python3 scanner.py scanme.nmap.org 1 1024 -j
```

**Features:**
- Fast TCP connection-based scanning
- Service banner grabbing
- Common port-to-service mapping
- Text and JSON output
- Timestamped reports

**Output:**
```
============================================================
  Port Scanner - Network Reconnaissance
============================================================
  Target       : scanme.nmap.org (45.33.32.156)
  Port Range   : 1 - 1024
  Scan Started : 2025-08-11 11:21:15
============================================================
  [OPEN]  Port 22     SSH             SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
  [OPEN]  Port 53     DNS             No banner
  [OPEN]  Port 80     HTTP            HTTP/1.1 200 OK
============================================================
  Scan Complete
  Open Ports Found: 3
============================================================
  Text report saved: scan_scanme.nmap.org_20250811_113007.txt
  JSON report saved : scan_scanme.nmap.org_20250811_113007.json
```

**Concepts demonstrated:**
- Socket programming (TCP/IP fundamentals)
- Network timeouts and error handling
- Service enumeration

---

### 2. Vulnerability Scanner — Risk Assessment

**Location:** `tools/vuln-scanner/`

Matches detected services against a CVE database to identify known vulnerabilities.

```bash
python3 vuln_scanner.py ../port-scanner/scan_scanme.nmap.org_20250811_113007.json
```

**Features:**
- Parses port scanner JSON output
- Version extraction from banners
- CVE database lookups
- Severity-based risk classification
- CRITICAL/HIGH/MEDIUM/LOW prioritization

**Output:**
```
======================================================================
  Vulnerability Scanner
======================================================================
  Target       : scanme.nmap.org
  Open Ports   : 3
======================================================================
  Port 22 - SSH
    Detected: OpenSSH 6.6.1
    Banner: SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
    Vulnerabilities: 2 found
      🔴 CRITICAL CVE-2014-6271
         ShellShock - Bash environment variable vulnerability affects SSH
      🟠 HIGH CVE-2015-3238
         Authentication bypass in OpenSSH 6.6.x before 6.6.1p2
  Port 53 - DNS
    Banner: No banner
    ✓ No known vulnerabilities in database
  Port 80 - HTTP
    Banner: HTTP/1.1 200 OK
    ✓ No known vulnerabilities in database
======================================================================
  Summary
======================================================================
  Total Vulnerabilities Found: 2
  Critical: 1 | High: 1
  
  ⚠️  CRITICAL vulnerabilities detected - immediate patching required!
======================================================================
```

**Concepts demonstrated:**
- Data pipeline architecture (tool-to-tool integration)
- JSON parsing and manipulation
- CVE/vulnerability research
- Risk prioritization

---

### 3. Web Reconnaissance Tool — Application Security

**Location:** `tools/web-recon/`

Performs deep reconnaissance on web applications (HTTPS, headers, technology stack, DNS, file discovery).

```bash
python3 web_recon.py google.com
python3 web_recon.py example.com -j
```

**Features:**
- SSL/TLS certificate analysis and expiry checking
- HTTP header inspection (security headers, server info)
- Technology stack detection (jQuery, React, WordPress, etc.)
- DNS record resolution
- Common web file discovery (robots.txt, sitemap.xml, etc.)
- JSON report generation

**Output:**
```
======================================================================
  Web Reconnaissance Scanner
======================================================================
  Target: google.com

[*] Fetching SSL/TLS Certificate...
  ✓ Subject: google.com
  ✓ Issuer: Google Internet Authority G3
  ✓ Expires: Aug 14 11:07:27 2025 GMT (62 days)
  ✓ Alt Names: google.com, www.google.com

[*] Analyzing HTTP Headers...
  ✓ Server: gws
  ✓ X-Frame-Options: SAMEORIGIN
  ✓ X-Content-Type-Options: nosniff
  ✓ Content-Security-Policy: ...
  ⚠️  Missing security headers: Strict-Transport-Security

[*] Detecting Technologies...
  ✓ Google Analytics detected
  ✓ jQuery detected
  ✓ Bootstrap detected

[*] Resolving DNS Records...
  ✓ A Record: 142.251.41.14
  ℹ️  No direct mail server on mail.google.com

[*] Checking Web Structure...
  ✓ robots.txt: Found
  ✓ sitemap.xml: Found

======================================================================
  Web Reconnaissance Report
======================================================================
  Target: google.com
  Scanned: 2025-08-11T15:30:45.123456
======================================================================
  ✓ HTTPS enabled
  ✓ Technologies: 3 detected
  ✓ Discoverable files: 2
======================================================================

  Report saved: web_recon_google.com_20250811_153045.json
```

**Concepts demonstrated:**
- SSL/TLS certificate handling
- HTTP protocol and headers
- Web technology fingerprinting
- Passive information gathering

---

## Complete Workflow Example

### Step 1: Scan the target

```bash
cd tools/port-scanner
python3 scanner.py example.com 1 1024 -j
# Output: scan_example.com_20250811_113007.json
```

### Step 2: Identify vulnerabilities

```bash
cd ../vuln-scanner
python3 vuln_scanner.py ../port-scanner/scan_example.com_20250811_113007.json
# Identifies CVEs for detected services
```

### Step 3: Analyze the web application

```bash
cd ../web-recon
python3 web_recon.py example.com -j
# Gathers web-level intelligence
```

### Result: Complete Security Assessment

You now have:
- Network-level reconnaissance (open ports, services)
- Vulnerability assessment (known exploits)
- Web application analysis (tech stack, headers, SSL)
- Structured JSON reports for further analysis or report generation

---

## Repository Structure

```
reconpy/
├── tools/
│   ├── port-scanner/
│   │   ├── scanner.py           # Main tool
│   │   ├── README.md            # Usage guide
│   │   └── scan_*.txt|json      # Generated reports
│   ├── vuln-scanner/
│   │   ├── vuln_scanner.py      # Main tool
│   │   ├── cve_database.json    # Vulnerability database
│   │   ├── README.md            # Usage guide
│   │   └── scan_*.json          # Generated reports
│   └── web-recon/
│       ├── web_recon.py         # Main tool
│       ├── README.md            # Usage guide
│       └── web_recon_*.json     # Generated reports
├── phase-1-foundations/
│   ├── port-scanner-project/
│   │   └── WRITEUP.md           # Portfolio writeup
│   ├── vuln-scanner-project/
│   │   └── WRITEUP.md           # Portfolio writeup
│   └── web-recon-project/
│       └── WRITEUP.md           # Portfolio writeup
├── notes/
│   └── commands-cheatsheet.md   # Command reference
└── README.md                    # This file
```

---

## Setup & Requirements

### Prerequisites
- Python 3.10+
- Linux/macOS/WSL (Windows Subsystem for Linux)
- Network connectivity to targets

### Installation

```bash
# Clone repository
git clone https://github.com/lindah177/reconpy.git
cd reconpy

# No external dependencies — uses Python standard library only
# (socket, ssl, json, urllib, argparse, re, datetime)
```

### Quick Start

```bash
# Scan a target for open ports
cd tools/port-scanner
python3 scanner.py scanme.nmap.org 1 1024 -j

# Identify vulnerabilities
cd ../vuln-scanner
python3 vuln_scanner.py ../port-scanner/scan_scanme.nmap.org_*.json

# Analyze web presence
cd ../web-recon
python3 web_recon.py scanme.nmap.org -j
```

---

## Ethical Use & Legal Scope

⚠️ **Important:** All testing conducted on:
- Hosts you own (localhost, your personal servers)
- Services explicitly authorized for testing (scanme.nmap.org, HackTheBox, TryHackMe)
- Targets with explicit written permission

**Never** scan third-party systems without permission. Unauthorized network scanning is illegal in most jurisdictions.

---

## Skills Demonstrated

### Networking & Security
- ✅ TCP/IP socket programming
- ✅ Port scanning and service enumeration
- ✅ SSL/TLS certificate analysis
- ✅ DNS resolution
- ✅ HTTP protocol and headers

### Vulnerability Research
- ✅ CVE database querying
- ✅ Version matching and fingerprinting
- ✅ Risk classification and prioritization
- ✅ Security assessment methodology

### Python Development
- ✅ Command-line argument parsing (argparse)
- ✅ JSON parsing and generation
- ✅ Exception handling (socket, SSL, HTTP errors)
- ✅ Object-oriented design
- ✅ Regular expressions for pattern matching

### DevOps & Tooling
- ✅ Modular tool architecture
- ✅ Data pipeline integration (tool-to-tool workflows)
- ✅ Report generation (text + JSON)
- ✅ Git version control

---

## Testing & Validation

All tools have been tested against real targets:

### Port Scanner
- **Target:** scanme.nmap.org
- **Results:** Correctly identified SSH (port 22), DNS (port 53), HTTP (port 80)
- **Validation:** Matches nmap/Masscan output

### Vulnerability Scanner
- **Target:** OpenSSH 6.6.1 (from scanme.nmap.org)
- **Results:** Identified 2 CVEs (CVE-2014-6271 CRITICAL, CVE-2015-3238 HIGH)
- **Validation:** Matches NVD database records

### Web Reconnaissance
- **Targets:** google.com, example.com, scanme.nmap.org
- **Results:** Successfully analyzed SSL certificates, HTTP headers, technologies, DNS
- **Validation:** Results verified against browser inspection and online tools

---

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Port Scanner | Aug 9-15 | ✅ Complete |
| Vulnerability Scanner | Aug 16-20 | ✅ Complete |
| Web Reconnaissance | Aug 21-26 | 🟡 In Progress |
| Portfolio Writeups | Aug 27-31 | ⏳ Next |

**Deadline:** September 25, 2025

---

## References

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NVD - National Vulnerability Database](https://nvd.nist.gov)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [SSL/TLS in Python](https://docs.python.org/3/library/ssl.html)
