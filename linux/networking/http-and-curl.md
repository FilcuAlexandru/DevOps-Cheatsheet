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

```bash
curl -I https://host                 # headers only (HEAD request), fast check without downloading the body
curl -L https://host                   # follow redirects — plain curl stops at the first 3xx by default
curl -X POST -d '{"key":"value"}' -H "Content-Type: application/json" https://host/api   # send a JSON POST body
curl -u user:pass https://host           # basic auth
```
