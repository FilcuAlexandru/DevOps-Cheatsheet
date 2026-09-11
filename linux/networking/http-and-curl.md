# Networking — HTTP and curl


```bash
curl -o /dev/null -s -w '%{http_code} %{time_total}s\n' https://host   # status code + total time, nothing else
curl -w "@curl-format.txt" -o /dev/null -s https://host   # full timing breakdown (DNS, connect, TLS, TTFB)
curl -kv https://host 2>&1 | grep -A2 'subject\|expire'    # quick cert subject + expiry check without openssl
```
`curl-format.txt` example:
```
dns: %{time_namelookup}\nconnect: %{time_connect}\nttfb: %{time_starttransfer}\ntotal: %{time_total}\n
```

---
