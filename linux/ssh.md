# Linux — SSH


```bash
ssh -J bastion user@internal-host        # jump host in one line, no manual tunnel
ssh -N -L 8080:localhost:80 user@host    # local port forward, no shell — great for reaching internal dashboards
ssh -N -D 1080 user@host                  # SOCKS proxy through a single host
ssh-copy-id user@host                     # push your key without manual cat/append
```

**Enhanced — `~/.ssh/config` aliases:**
```
Host eip-prod
    HostName 10.0.4.12
    User afilcu
    ProxyJump bastion
    ServerAliveInterval 30
```
Then just `ssh eip-prod` — no more remembering IPs, jump hosts, or usernames.

---
