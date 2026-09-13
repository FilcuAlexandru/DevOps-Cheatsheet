# Networking — Connectivity


```bash
mtr host.example.com          # ping + traceroute combined, live — best first tool for "is it the network"
nc -zv host 443                 # quick TCP port check — no telnet needed, nc does the same job and is more commonly preinstalled now
tcpdump -i any port 443 -w cap.pcap   # capture for later analysis in Wireshark — save traffic now, dig into it properly later with a GUI
tcpdump -i eth0 -nn host 10.0.0.5 and port 443   # filtered live capture, no DNS lookups — faster and cleaner output than letting tcpdump resolve every address
```

**Enhanced:**
```bash
mtr --report --report-cycles 10 host.example.com   # non-interactive report mode — 10 cycles then exit, perfect for pasting into a ticket or a script instead of the live TUI view
```
