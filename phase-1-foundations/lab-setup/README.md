# Lab setup

Document your home lab configuration here as you build it.

---

## Network topology

```
[Host machine]
     |
  [NAT Network: 10.0.2.0/24]
     |          |
  [Kali]   [Metasploitable2]
```

*Update this diagram with your actual IP ranges.*

---

## VMs

| VM | OS | IP | Purpose |
|----|----|----|---------|
| Kali Linux | Kali 2024.x | 10.0.2.x | Attack machine |
| Metasploitable2 | Ubuntu | 10.0.2.x | Vulnerable target |
| DVWA | Ubuntu + Apache | 10.0.2.x | Web app target |

---

## Setup checklist

- [ ] VirtualBox installed
- [ ] Kali Linux VM created (at least 2GB RAM, 20GB disk)
- [ ] Metasploitable2 imported
- [ ] Both VMs on the same NAT network
- [ ] Kali can ping Metasploitable2
- [ ] Metasploitable2 services confirmed with `nmap`

---

## Notes

Add any setup quirks, troubleshooting steps, or configuration choices here.
