# Linux — CPU and Memory


```bash
free -h                    # memory overview — quick totals for used/free/swap, human-readable
vmstat 1 5                 # 5 samples, 1s apart — watch 'r' (run queue) and 'wa' (I/O wait)
mpstat -P ALL 1            # per-core CPU usage — reveals imbalance a single averaged number from top would hide
sar -u 1 5                 # historical CPU stats — needs sysstat installed, shows usage over time instead of just right now
```

**Enhanced:**
```bash
numactl --hardware          # NUMA topology — matters on multi-socket DB/JVM hosts
pmap -x 1234 | tail -1       # total memory footprint of one process, broken down — shared vs private, more accurate than a single RSS number
smem -tk                    # accounts for shared memory properly — free and ps both double-count it across processes, this doesn't
watch -n1 'free -h'          # live-refreshing memory view without extra tools — a poor man's dashboard using only watch + free
```

```bash
top -H -p 1234              # per-thread CPU view for one process — find which thread inside a process is hot
free -m --si                  # memory in MB, SI (1000-based) units — matches how storage vendors usually report size, unlike the default binary units
cat /proc/loadavg              # raw load average + running/total process count, scriptable — parseable without stripping uptime's prose formatting
uptime                          # quick load average without the human-readable wrapper — same numbers, less text to parse
```

**Enhanced — historical and NUMA-aware:**
```bash
sar -r 1 5                    # historical memory usage samples — needs sysstat, same sar tool used with -u for CPU history
vmstat -s                       # cumulative memory/swap stats since boot — a one-shot summary instead of vmstat's repeating samples
numastat -p 1234                 # NUMA memory allocation for one process — cross-node access is a hidden latency source on multi-socket hosts
```
