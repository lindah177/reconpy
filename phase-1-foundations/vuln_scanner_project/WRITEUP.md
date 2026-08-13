# Vulnerability Scanner

Matches open ports and services from the port scanner against a CVE database to identify known vulnerabilities.

## Usage

First, run the port scanner and save JSON output:
```bash
python3 ../port-scanner/scanner.py scanme.nmap.org 1 1024 -j
```

Then run the vulnerability scanner on the JSON output:
```bash
python3 vuln_scanner.py ../port-scanner/scan_scanme.nmap.org_*.json
```

## How it works

1. **Loads port scan results** from JSON file
2. **Extracts service versions** from banners (e.g., "OpenSSH 6.6.1" from SSH banner)
3. **Matches against CVE database** for known vulnerabilities
4. **Reports severity** — CRITICAL, HIGH, MEDIUM, LOW, INFO

## Output