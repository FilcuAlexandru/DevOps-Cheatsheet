# Bash — Locks and Timeouts


```bash
flock -n /tmp/job.lock -c "./script.sh"   # prevent overlapping cron runs — non-blocking, exits if already locked
timeout 30 curl https://slow-service      # kill a hung command after 30s
timeout -k5 30 ./script.sh                 # SIGTERM at 30s, SIGKILL 5s later if it ignores the first
```

---
