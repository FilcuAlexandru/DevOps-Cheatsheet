# Linux — Troubleshooting

## Health check

Run through these in order — each step's red flag tells you where to dig deeper, without guessing.

1. **Load & CPU** — `uptime` — red flag: load average sustained above the core count for more than a minute or two.
2. **Memory** — `free -h` — red flag: available memory near zero *and* swap actively growing (a little swap use alone is normal).
3. **Disk space** — `df -h` — red flag: any filesystem above 90%, especially `/` or `/var`.
4. **Disk I/O** — `iostat -xz 1` — red flag: `%util` near 100 on a device — that's your actual bottleneck, not CPU.
5. **Recent errors** — `journalctl -p err -b` — red flag: errors clustering right around when the symptom started.

## Specific problems

**Disk fills up unexpectedly:**
```bash
du -sh --max-depth=1 / 2>/dev/null | sort -rh | head   # which top-level directory is actually growing
lsof +D /var/log 2>/dev/null | awk '{print $NF}' | sort -u   # check for deleted-but-still-open files first — df and du disagreeing is the classic sign
```

**Process won't die:**
```bash
ps -eo pid,ppid,stat,cmd | grep 'Z'   # zombie processes (state Z) — these can't be killed directly, the problem is the parent not reaping them
kill -9 <parent_pid>                    # killing the parent usually clears the zombie; if the parent is PID 1, a reboot is the only fix
```

**System killed my process (OOM):**
```bash
dmesg -T | grep -i "out of memory"   # confirm it was actually the OOM killer, not a crash
grep -i oom /var/log/syslog            # OOM killer's own log entries, including which process it picked and why
```
The OOM killer picks based on a memory-usage score, not always the "obvious" culprit — always confirm from the log rather than assuming.

---
