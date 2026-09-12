# Linux — CPU and Memory


```bash
free -h                    # memory overview
vmstat 1 5                 # 5 samples, 1s apart — watch 'r' (run queue) and 'wa' (I/O wait)
mpstat -P ALL 1            # per-core CPU usage
sar -u 1 5                 # historical CPU stats (needs sysstat)
```

**Enhanced:**
```bash
numactl --hardware          # NUMA topology — matters on multi-socket DB/JVM hosts
pmap -x 1234 | tail -1       # total memory footprint of one process, broken down
smem -tk                    # accounts for shared memory properly (free/ps double-count it)
watch -n1 'free -h'          # live-refreshing memory view without extra tools
```

```bash
top -H -p 1234              # per-thread CPU view for one process — find which thread inside a process is hot
free -m --si                  # memory in MB, SI units (1000-based) instead of the default binary units
cat /proc/loadavg              # raw load average + running/total process count, scriptable
uptime                          # quick load average without the human-readable wrapper
```

**Enhanced — historical and NUMA-aware:**
```bash
sar -r 1 5                    # historical memory usage samples (needs sysstat), same tool as -u for CPU
vmstat -s                       # cumulative memory/swap stats since boot, one-shot summary
numastat -p 1234                 # NUMA memory allocation for one process — cross-node access is a hidden latency source on multi-socket hosts
```
