# Networking — DNS


```bash
dig +short host.example.com        # just the answer, no noise — dig's default output is verbose, this strips it to the one line you actually want
dig +trace host.example.com         # walk the full resolution chain, root to authoritative — shows exactly which server answered at each step
resolvectl query host.example.com    # on systemd-resolved hosts, shows which resolver actually answered — confirms which of possibly several configured resolvers responded
dig @8.8.8.8 host.example.com        # query a specific resolver directly — bypasses local cache, confirms what that resolver actually has
```

```bash
host host.example.com          # simplest possible DNS lookup — minimal output when you just need the answer, not the full dig report
nslookup host.example.com        # older tool, still common in scripts and on Windows-adjacent teams — same job as dig, different output format
getent hosts host.example.com      # resolves via the same path applications use — respects /etc/nsswitch.conf, not just DNS
cat /etc/resolv.conf                 # which nameservers this host is actually configured to use — confirms the real config before assuming DNS is misconfigured
```
