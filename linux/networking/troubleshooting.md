# Networking — Troubleshooting

## Health check

Work outward from the local machine — each layer rules something out before you move to the next.

1. **Interface is up** — `ip -br a` — red flag: interface state `DOWN`.
2. **DNS resolves** — `dig +short host.example.com` — red flag: empty answer or timeout.
3. **Route exists** — `ip route get <ip>` — red flag: "no route to host" or routed through an unexpected interface.
4. **Port is reachable** — `nc -zv host 443` — red flag: connection refused (nothing listening) or timeout (firewall/network path issue) — the two point to different fixes.

**"Address already in use" when starting a service:**
```bash
ss -tulnp | grep <port>          # find what's already bound to the port — the actual fix is identifying the conflicting process, not guessing
kill <pid_from_above>              # or reconfigure one of the two services to use a different port — the alternative to killing whatever's already bound
```

**DNS resolution suddenly fails:**
```bash
cat /etc/resolv.conf                 # confirm nameservers are actually configured — an empty resolv.conf explains DNS failures immediately
dig @8.8.8.8 <hostname>                # bypass the local resolver entirely — if this works, the problem is local DNS config, not the network
systemd-resolve --status                # on systemd-resolved hosts, shows which resolver is actually active per interface — resolv.conf alone can be misleading here
```

---
