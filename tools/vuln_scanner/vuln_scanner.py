import json
import sys
import argparse
from pathlib import Path

class VulnerabilityScanner:
    def __init__(self, cve_db_path="cve_database.json"):
        self.cve_db = self.load_cve_database(cve_db_path)
        self.severity_levels = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1,
            "INFO": 0
        }
    
    def load_cve_database(self, db_path):
        """Load CVE database from JSON file"""
        try:
            with open(db_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] CVE database not found: {db_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON in CVE database: {db_path}")
            sys.exit(1)
    
    def load_port_scan_results(self, json_file):
        """Load results from port scanner JSON output"""
        try:
            with open(json_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] Scan results file not found: {json_file}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON in scan results: {json_file}")
            sys.exit(1)
    
    def extract_service_version(self, banner, service):
        """Try to extract version info from banner"""
        if not banner or banner == "No banner":
            return None
        
        # Extract version for known services
        if service == "SSH" and "openssh" in banner.lower():
            # Example: ssh-2.0-openssh_6.6.1p1 ubuntu-2ubuntu2.13
            parts = banner.lower().split()
            for part in parts:
                if "openssh" in part:
                    version = part.split("_")[-1].replace("openssh_", "")
                    # Normalize to major.minor format
                    return f"OpenSSH {version.split('p')[0]}"
        
        return None
    
    # def find_vulnerabilities(self, service, version):
    #     """Find CVEs for a given service and version"""
    #     vulnerabilities = []
        
    #     if service not in self.cve_db:
    #         return vulnerabilities
        
    #     service_db = self.cve_db[service]
        
    #     # Exact version match
    #     if version and version in service_db:
    #         vulnerabilities.extend(service_db[version])
        
    #     # Partial match - check if database version is contained in detected version
    #     # e.g., "OpenSSH 6.6" matches "OpenSSH 6.6.1"
    #     if version:
    #         for db_version, cves in service_db.items():
    #             if db_version.lower() in version.lower() and db_version not in (version or ""):
    #                 vulnerabilities.extend(cves)
        
    #     return vulnerabilities

    def find_vulnerabilities(self, service, version):
        """Find CVEs for a given service and version"""
        vulnerabilities = []
        
        if service not in self.cve_db:
            return vulnerabilities
        
        service_db = self.cve_db[service]
        
        # Exact version match
        if version and version in service_db:
            vulnerabilities.extend(service_db[version])
        
        # Partial match
        if version:
            for db_version, cves in service_db.items():
                if db_version.lower() in version.lower():
                    if db_version not in version:  # simplified check
                        vulnerabilities.extend(cves)
        

        return vulnerabilities
    
    def format_severity(self, severity):
        """Format severity with emoji"""
        emoji_map = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🔵",
            "INFO": "ℹ️"
        }
        return f"{emoji_map.get(severity, '❓')} {severity}"
    
    def scan(self, json_file):
        """Run vulnerability scan on port scanner output"""
        results = self.load_port_scan_results(json_file)
        
        target = results.get("target", "Unknown")
        open_ports = results.get("open_ports", [])
        
        print(f"\n{'='*70}")
        print(f"  Vulnerability Scanner")
        print(f"{'='*70}")
        print(f"  Target       : {target}")
        print(f"  Open Ports   : {len(open_ports)}")
        print(f"{'='*70}\n")
        
        if not open_ports:
            print("  No open ports to scan.\n")
            return
        
        total_vulns = 0
        high_risk_count = 0
        critical_count = 0
        
        for port_info in open_ports:
            port = port_info.get("port")
            service = port_info.get("service", "Unknown")
            banner = port_info.get("banner", "No banner")
            
            # Try to extract version from banner
            version = self.extract_service_version(banner, service)
            
            print(f"  Port {port} - {service}")
            if version:
                print(f"    Detected: {version}")
            print(f"    Banner: {banner[:60]}")
            
            # Find vulnerabilities
            vulns = self.find_vulnerabilities(service, version)
            
            if vulns:
                print(f"    Vulnerabilities: {len(vulns)} found")
                for vuln in vulns:
                    severity = vuln.get("severity", "INFO")
                    cve = vuln.get("cve", "Unknown")
                    desc = vuln.get("description", "No description")
                    
                    print(f"      {self.format_severity(severity)} {cve}")
                    print(f"         {desc}")
                    
                    total_vulns += 1
                    if severity == "CRITICAL":
                        critical_count += 1
                    elif severity == "HIGH":
                        high_risk_count += 1
            else:
                print(f"    No known vulnerabilities in database")
            
            print()
        
        # Summary
        print(f"{'='*70}")
        print(f"  Summary")
        print(f"{'='*70}")
        print(f"  Total Vulnerabilities Found: {total_vulns}")
        print(f"  Critical: {critical_count} | High: {high_risk_count}")
        
        if critical_count > 0:
            print(f"\n  CRITICAL vulnerabilities detected - immediate patching required!")
        elif high_risk_count > 0:
            print(f"\n  HIGH-risk vulnerabilities found - plan patching soon")
        else:
            print(f"\n  No critical/high-risk vulnerabilities in database")
        
        print(f"{'='*70}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Vulnerability scanner for port scanner JSON output"
    )
    parser.add_argument("scan_file", help="JSON file from port scanner")
    parser.add_argument("-d", "--database", default="cve_database.json",
                        help="Path to CVE database JSON (default: cve_database.json)")
    
    args = parser.parse_args()
    
    scanner = VulnerabilityScanner(args.database)
    scanner.scan(args.scan_file)