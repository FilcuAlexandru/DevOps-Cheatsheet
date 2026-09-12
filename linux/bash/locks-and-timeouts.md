# Bash — Locks and Timeouts


```bash
flock -n /tmp/job.lock -c "./script.sh"   # prevent overlapping cron runs — non-blocking, exits if already locked
timeout 30 curl https://slow-service      # kill a hung command after 30s
timeout -k5 30 ./script.sh                 # SIGTERM at 30s, SIGKILL 5s later if it ignores the first
```

```bash
flock -w 30 /tmp/job.lock -c "./script.sh"   # wait up to 30s for the lock instead of failing immediately
exec 200>/tmp/job.lock; flock -n 200 || exit 1   # hold a lock for the rest of the script's lifetime via a file descriptor, released automatically on exit
timeout --preserve-status 30 ./script.sh       # propagate the wrapped command's actual exit code instead of timeout's own 124
```
