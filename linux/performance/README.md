# Performance

```bash
uptime                     # load average — compare to core count, not to 1.0
vmstat 1                    # check the 'r' (run queue) and 'wa' (I/O wait) columns — 'r' over core count means CPU-bound, high 'wa' means I/O-bound
perf top                     # live, per-function CPU profiling — needs perf installed, shows exactly which function is hot in real time
strace -c ./binary            # syscall summary — which syscalls dominate, and how many
iostat -xz 1                  # %util near 100 on a device means that's your actual bottleneck, not just a busy-looking number
sar -q 1 5                     # historical load average + run queue length — needs sysstat, shows the trend instead of a single snapshot
dstat                           # combined CPU/disk/net/memory view, one screen — a friendlier vmstat+iostat+ifstat
htop                             # interactive top with per-core bars and a tree view — easier mouse-driven sorting than plain top
```

**Enhanced:**
```bash
pidstat -p <pid> 1                       # per-process CPU/context-switch breakdown over time — narrower and clearer than top when you already know which process to watch
perf record -p <pid> -g -- sleep 10        # profile one process for 10s with call graphs — then `perf report` to see hot functions
perf stat ./binary                           # summary counters for one run — instructions, cache misses, context switches, branch mispredicts
iotop -o                                       # like top but for disk I/O — -o hides processes doing zero I/O, so only active ones show
```

## Health check

1. **Load & CPU** — `uptime` — red flag: load average sustained above the core count.
2. **I/O wait** — `vmstat 1` — red flag: high `wa` column consistently, not just a momentary spike.
3. **Swap activity** — `free -h` — red flag: swap actively growing, not just present (a little used swap at rest is normal).
4. **Per-core imbalance** — `mpstat -P ALL 1` — red flag: one core pegged near 100% while others sit idle — points to a single-threaded bottleneck, not overall capacity.

## Troubleshooting

**Server feels slow but no single process looks bad in `top`:**
```bash
vmstat 1 5                          # check 'r' (run queue) and 'wa' (I/O wait) columns — a slowdown can be system-wide contention, not one process
mpstat -P ALL 1                       # per-core breakdown — one pegged core hiding behind an average that looks fine is a common trap
```

**High load average but low CPU usage:**
```bash
ps -eo stat,pid,cmd | grep "^D"    # D-state processes count toward load average but not CPU% — usually I/O-bound
iostat -xz 1                         # confirm which device those D-state processes are actually waiting on — narrows a stuck process down to a specific disk
```

**Suspected memory leak, not sure which process:**
```bash
watch -n5 'ps -eo pid,cmd,%mem,rss --sort=-rss | head -10'   # watch top memory consumers over time — a steadily climbing RSS on one process is the tell
```

---
