# Linux — Logs

Application/system log files on disk — searching, following, rotating. (For systemd's own journal, see the separate systemd section — journalctl is a different mechanism entirely.)

```bash
tail -f /var/log/myapp/app.log                    # follow a single log file live
tail -f /var/log/myapp/*.log                         # follow multiple files at once, each line prefixed with its filename
grep -i "error" /var/log/myapp/app.log                 # case-insensitive search in a plain log file
grep -rn "connection refused" /var/log/myapp/            # recursive search across a whole log directory, with line numbers
zgrep "timeout" /var/log/myapp/app.log.2.gz               # search inside a rotated, gzip-compressed log without manually decompressing it
find /var/log -name "*.log" -mtime -1                       # every log file modified in the last 24h, across the system
find /var/log -name "*.log" -size +100M                       # find unexpectedly large log files eating disk
```

**Enhanced:**
```bash
grep -A5 -B5 "OutOfMemoryError" app.log                  # 5 lines of context before and after a match — the surrounding lines are usually what actually explains it
tail -n +1 -f app.log | grep --line-buffered "ERROR"        # follow a file live, filtered to just error lines (--line-buffered keeps grep from batching output when piped)
zcat app.log.1.gz app.log.2.gz | grep "user_id=12345"          # search across several rotated archives at once, in the order they happened
: > /var/log/myapp/app.log                                       # truncate a live log file in place, safe even while a process still has it open — rm would just hide the space until the process exits
```

**Log rotation (logrotate):**
```bash
cat /etc/logrotate.d/myapp                    # see how a specific app's rotation is configured — size/age thresholds, compression, retention count
logrotate -d /etc/logrotate.d/myapp             # dry-run: shows what WOULD happen, without actually rotating anything
logrotate -f /etc/logrotate.d/myapp               # force an out-of-cycle rotation right now, useful before a disk fills up
```

## Health check

1. **Is anything actually writing logs** — `tail -f /var/log/myapp/app.log` and watch for fresh lines during known activity — red flag: silence despite active traffic — the app may be logging somewhere else entirely.
2. **Disk headroom for logs** — `df -h /var/log` — red flag: above 90% — rotation may not be keeping up.
3. **Rotation is actually running** — check the log file's size and timestamp against what `logrotate` config expects — red flag: a file far past its configured rotation size/age means rotation silently isn't firing.

## Troubleshooting

**Can't find where an app actually logs to:**
```bash
lsof -p <pid> | grep -i log            # list open files for the process — its log file(s) show up here even with a nonstandard path
find / -xdev -name "*.log" -newer /tmp -mmin -5 2>/dev/null   # files touched in the last 5 minutes — catches an active log you don't know the location of
```

**A single log file has grown huge and is filling the disk:**
```bash
: > /var/log/myapp/app.log            # truncate in place, safe even if a process still has it open — see the Enhanced note above
logrotate -f /etc/logrotate.d/myapp     # if rotation should have caught this already, force it and check why it didn't run on schedule
```

**Searching a large log is too slow:**
```bash
grep -F "exact string" bigfile.log      # -F (fixed string) skips regex parsing — much faster when you're not actually using regex features
rg "pattern" bigfile.log                  # ripgrep, if available — multithreaded and typically far faster than grep on large files
```

---
