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
