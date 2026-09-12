# Networking — DNS


```bash
dig +short host.example.com        # just the answer, no noise
dig +trace host.example.com         # walk the full resolution chain, root to authoritative
resolvectl query host.example.com    # on systemd-resolved hosts, shows which resolver actually answered
dig @8.8.8.8 host.example.com        # query a specific resolver directly, bypass local cache
```

```bash
host host.example.com          # simplest possible DNS lookup, minimal output
nslookup host.example.com        # older tool, still common in scripts and on Windows-adjacent teams
getent hosts host.example.com      # resolves via the same path applications use (respects /etc/nsswitch.conf), not just DNS directly
cat /etc/resolv.conf                 # which nameservers this host is actually configured to use
```
