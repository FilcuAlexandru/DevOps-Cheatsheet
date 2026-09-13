# Linux — Logs

Application/system log files on disk — searching, following, rotating. (For systemd's own journal, see the separate systemd section — journalctl is a different mechanism entirely.)

```bash
tail -f /var/log/myapp/app.log                    # follow a single log file live — watch new lines appear as they're written
tail -f /var/log/myapp/*.log                         # follow multiple files at once, each line prefixed with its filename — correlate events across services without switching terminals
grep -i "error" /var/log/myapp/app.log                 # case-insensitive search in a plain log file — catches a match regardless of how it was capitalized
grep -rn "connection refused" /var/log/myapp/            # recursive search across a whole log directory, with line numbers — find a match without knowing which file it's in
zgrep "timeout" /var/log/myapp/app.log.2.gz               # search inside a rotated, gzip-compressed log — no need to manually decompress it first
find /var/log -name "*.log" -mtime -1                       # every log file modified in the last 24h, across the system — finds active logs you don't already know the location of
find /var/log -name "*.log" -size +100M                       # find unexpectedly large log files eating disk — the fast way to spot what's actually filling /var/log
awk '/2026-09-10 14:0/,/2026-09-10 14:1/' app.log             # print only lines within a time window — precise on huge logs where grep -A/-B isn't
journalctl --since "10 minutes ago" -o cat                      # check whether an app is actually logging to the journal instead of a file — confirms you're looking in the right place at all
head -n 100 app.log                                               # first 100 lines — useful for checking a log's format/header before writing a real filter
```

**Enhanced:**
```bash
grep -A5 -B5 "OutOfMemoryError" app.log                  # 5 lines of context before and after a match — the surrounding lines are usually what actually explains it
tail -n +1 -f app.log | grep --line-buffered "ERROR"        # follow a file live, filtered to error lines — --line-buffered avoids grep batching when piped
zcat app.log.1.gz app.log.2.gz | grep "user_id=12345"          # search across several rotated archives at once, in the order they happened — reconstructs a timeline that spans multiple rotated files
: > /var/log/myapp/app.log                                       # truncate a live log file in place, safe even while a process still has it open — rm would just hide the space until the process exits
```

**Log rotation (logrotate):**
```bash
cat /etc/logrotate.d/myapp                    # see how a specific app's rotation is configured — size/age thresholds, compression, retention count
logrotate -d /etc/logrotate.d/myapp             # dry-run: shows what WOULD happen — confirms the rotation config is correct before it actually runs for real
logrotate -f /etc/logrotate.d/myapp               # force an out-of-cycle rotation right now — useful as an emergency move before a disk actually fills up
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
logrotate -f /etc/logrotate.d/myapp     # force rotation now — then check why it didn't run on schedule
```

**Searching a large log is too slow:**
```bash
grep -F "exact string" bigfile.log      # -F (fixed string) skips regex parsing — much faster when you're not actually using regex features
rg "pattern" bigfile.log                  # ripgrep, if available — multithreaded and typically far faster than grep on large files
```

---
