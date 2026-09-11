# Networking — DNS


```bash
dig +short host.example.com        # just the answer, no noise
dig +trace host.example.com         # walk the full resolution chain, root to authoritative
resolvectl query host.example.com    # on systemd-resolved hosts, shows which resolver actually answered
dig @8.8.8.8 host.example.com        # query a specific resolver directly, bypass local cache
```
