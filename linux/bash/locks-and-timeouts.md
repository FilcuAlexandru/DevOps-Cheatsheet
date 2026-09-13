# Bash — Locks and Timeouts


```bash
flock -n /tmp/job.lock -c "./script.sh"   # prevent overlapping cron runs — non-blocking, exits if already locked
timeout 30 curl https://slow-service      # kill a hung command after 30s — prevents a script from hanging forever on one stuck step
timeout -k5 30 ./script.sh                 # SIGTERM at 30s, SIGKILL 5s later if it ignores the first — gives the process a chance to clean up before forcing it
```

```bash
flock -w 30 /tmp/job.lock -c "./script.sh"   # wait up to 30s for the lock instead of failing immediately — useful when a brief overlap with another run is expected
exec 200>/tmp/job.lock; flock -n 200 || exit 1   # hold a lock for the script's whole lifetime via a file descriptor — released automatically on exit
timeout --preserve-status 30 ./script.sh       # propagate the wrapped command's actual exit code — otherwise a caller only sees timeout's own 124, not what actually failed
```
