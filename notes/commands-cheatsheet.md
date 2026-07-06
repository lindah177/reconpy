# Commands cheatsheet

A living reference — add commands here as you encounter them.

---

## nmap

```bash
# Fast scan — top 1000 ports
nmap -T4 -F <target>

# Full port scan
nmap -p- -T4 <target>

# Service + version detection
nmap -sV -sC <target>

# OS fingerprinting (requires root)
sudo nmap -O <target>

# Output to file
nmap -oN output.txt <target>
```

---

## Wireshark / tcpdump

```bash
# Capture on interface (tcpdump)
sudo tcpdump -i eth0 -w capture.pcap

# Filter to HTTP only
sudo tcpdump -i eth0 port 80

# Filter by host
sudo tcpdump -i eth0 host 192.168.1.1
```

Wireshark display filters:
```
tcp.flags.syn == 1              # SYN packets only
http.request.method == "POST"   # POST requests
dns                             # All DNS traffic
ip.addr == 192.168.1.100        # Filter by IP
```

---

## Linux

```bash
# File permissions
chmod 755 file        # rwxr-xr-x
chmod 600 file        # rw------- (private key)
chown user:group file

# Find files
find / -name "*.conf" 2>/dev/null
find / -perm -4000 2>/dev/null   # SUID files

# Users and groups
cat /etc/passwd
cat /etc/shadow      # hashed passwords (root only)
id                   # current user info

# Network
ss -tulnp            # open ports and processes
ip a                 # interfaces
```

---

## GPG / OpenSSL

```bash
# GPG encrypt a file
gpg -c secret.txt              # symmetric encrypt
gpg -d secret.txt.gpg          # decrypt

# Hash a file
sha256sum file.txt
echo -n "password" | sha256sum

# OpenSSL quick encrypt
openssl enc -aes-256-cbc -in plain.txt -out cipher.txt
openssl enc -d -aes-256-cbc -in cipher.txt -out plain.txt
```

---

## Git workflow (for this repo)

```bash
git clone https://github.com/lindah177/cybersec-portfolio
git checkout -b phase-1-lab-setup   # new branch per lab
git add .
git commit -m "phase-1: add Wireshark TCP handshake analysis"
git push origin phase-1-lab-setup
# then open a PR into main
```

---

*Add new sections as you progress through each phase.*
