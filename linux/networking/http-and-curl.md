# Networking — HTTP and curl


```bash
curl -o /dev/null -s -w '%{http_code} %{time_total}s\n' https://host   # status code + total time, nothing else — a minimal health check without the full response body
curl -w "@curl-format.txt" -o /dev/null -s https://host   # full timing breakdown — DNS, connect, TLS, TTFB, pinpoints exactly which phase is slow
curl -kv https://host 2>&1 | grep -A2 'subject\|expire'    # quick cert subject + expiry check — no need to drop into openssl s_client for a fast look
```
`curl-format.txt` example:
```
dns: %{time_namelookup}\nconnect: %{time_connect}\nttfb: %{time_starttransfer}\ntotal: %{time_total}\n
```

```bash
curl -I https://host                 # headers only — a HEAD request, fast check without downloading the full body
curl -L https://host                   # follow redirects — plain curl stops at the first 3xx by default
curl -X POST -d '{"key":"value"}' -H "Content-Type: application/json" https://host/api   # send a JSON POST body — the standard way to hit a JSON API from the command line
curl -u user:pass https://host           # sends HTTP Basic Authentication credentials with the request — the -u shorthand instead of building the header by hand
```
