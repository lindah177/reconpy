# Vulnerability Scanner Project — Portfolio Writeup

## Overview

Built a **vulnerability assessment tool** that automatically matches detected services against a CVE database. This tool works downstream of the port scanner to identify known exploitable vulnerabilities.

**Repository:** [reconpy/tools/vuln-scanner](https://github.com/lindah177/reconpy/tree/main/tools/vuln-scanner)

---

## The Problem

After reconnaissance (finding open ports), the next phase is vulnerability assessment. Manual CVE research is tedious:
- Find what service version is running
- Search NVD database manually
- Cross-reference CVSS scores
- Prioritize by risk

This tool automates it — takes port scanner JSON output and instantly reports known vulnerabilities.

---

## What the Tool Does

```bash
python3 vuln_scanner.py scan_scanme.nmap.org_20260811_113007.json
```

1. **Parses port scan results** — reads JSON from port scanner
2. **Extracts service versions** — analyzes banners to find software versions
3. **CVE database lookup** — matches service+version against known vulnerabilities
4. **Risk assessment** — reports severity (CRITICAL, HIGH, MEDIUM, LOW)

### Example Output

Port 22 - SSH
Detected: OpenSSH 6.6.1
🔴 CRITICAL CVE-2014-6271 - ShellShock vulnerability
🟠 HIGH CVE-2015-3238 - Authentication bypass

Summary
Total Vulnerabilities Found: 2
Critical: 1 | High: 1

---

## Security Concepts Demonstrated

### 1. Version Matching Logic

The core challenge: databases have "OpenSSH 6.6" but banners show "OpenSSH 6.6.1p1". Need substring matching:

```python
for db_version, cves in service_db.items():
    if db_version.lower() in version.lower():
        vulnerabilities.extend(cves)
```

**Why this matters:** Real vulnerability scanners do this constantly — matching fuzzy version strings to known CVE databases.

### 2. JSON Data Pipeline

Takes structured output from one tool and uses it as input for the next:

```python
def load_port_scan_results(self, json_file):
    with open(json_file, 'r') as f:
        return json.load(f)
```

**Why this matters:** Security tools work in chains. Your scanner→vulnerability matcher→reporter workflow is realistic.

### 3. Risk Severity Classification

Different vulnerabilities require different responses:

```python
severity_levels = {
    "CRITICAL": 4,    # Immediate action
    "HIGH": 3,        # Urgent
    "MEDIUM": 2,      # Plan remediation
    "LOW": 1          # Monitor
}
```

**Why this matters:** Executives need to know what to prioritize. A CRITICAL beats a thousand LOWs.

---

## Key Design Decisions

### Modular Architecture

Port scanner and vulnerability scanner are **separate tools** that communicate via JSON:
- Port scanner writes JSON
- Vuln scanner reads JSON

**Why:** Each tool does one thing well. Easy to swap in/out better tools. This is Unix philosophy.

### Manual CVE Database

`cve_database.json` is hand-maintained, not API-driven:

```json
{
  "SSH": {
    "OpenSSH 6.6": [
      {
        "cve": "CVE-2014-6271",
        "severity": "CRITICAL",
        "description": "ShellShock..."
      }
    ]
  }
}
```

**Why:** Proof of concept. Real tools integrate National Vulnerability Database (NVD) API, but this shows the concept clearly.

### Severity-based Summary

Ends with a summary for quick decision-making:

**Why:** Penetration testers need one-page executive summaries before the detailed report.

---

## Testing & Validation

Tested against real scan of `scanme.nmap.org`:

**Input (from port scanner):**
- Port 22: SSH-2.0-OpenSSH_6.6.1p1
- Port 53: DNS (no banner)
- Port 80: HTTP/1.1

**Output:**
- Port 22: 2 CVEs found (CRITICAL ShellShock, HIGH auth bypass)
- Port 53/80: No matches in database

**Validation:** Findings match public NVD records for OpenSSH 6.6.x

---

## Limitations & Future Work

### Current Limitations
- CVE database is small (~6 entries)
- Only works with services supported in database
- No CVSS scoring
- No exploit availability tracking

### Next Steps
1. **Integrate NVD API** — pull real CVE data instead of hardcoding
2. **CVSS scoring** — show impact/exploitability metrics
3. **Exploit database** — flag if Metasploit/PoC exists
4. **Historical scanning** — track when vulns were patched
5. **HTML reports** — generate professional penetration test reports

---

## How This Fits Into My Journey

This is **Phase 1: Foundations + Phase 2: Offensive basics** combined:

✅ Understanding network reconnaissance
✅ Vulnerability research and assessment
✅ Risk prioritization
✅ Building tools that integrate with existing workflows
✅ JSON data handling and structured analysis

The next tool will tackle **web application reconnaissance** — moving from network-level to application-level security.

---

## Repository

Full code and CVE database: https://github.com/lindah177/reconpy/tree/main/tools/vuln-scanner

---

**Built:** August 2025
**Language:** Python 3.10
**Time to completion:** ~2 days
**Lines of code:** ~200
