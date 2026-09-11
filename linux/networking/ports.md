# Networking — Ports


```bash
ss -tulnp               # listening TCP/UDP + PID, replaces netstat
lsof -i :443              # what's bound to a specific port
fuser -k 8080/tcp          # kill whatever's holding a port
```
