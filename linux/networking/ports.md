# Networking — Ports


```bash
ss -tulnp               # listening TCP/UDP + PID, replaces netstat
lsof -i :443              # what's bound to a specific port
fuser -k 8080/tcp          # kill whatever's holding a port
```

```bash
ss -tan state established          # only established TCP connections, filters out listeners/time-wait noise
ss -s                                 # socket summary counts by state — quick overview of connection health
netstat -tulnp                          # the older equivalent of ss -tulnp, still common on minimal images without ss
```
