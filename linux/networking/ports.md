# Networking — Ports


```bash
ss -tulnp               # listening TCP/UDP + PID — the modern replacement for netstat, faster on systems with many connections
lsof -i :443              # what's bound to a specific port — confirms exactly what's using it before you assume nothing is
fuser -k 8080/tcp          # kill whatever's holding a port — a fast fix for "address already in use" without hunting for the PID first
```

```bash
ss -tan state established          # only established TCP connections — filters out listeners and time-wait noise you usually don't care about
ss -s                                 # socket summary counts by state — quick overview of connection health
netstat -tulnp                          # the older equivalent of ss -tulnp — still common on minimal images that don't have ss installed
```
