# Linux — Processes


```bash
ps -eo pid,ppid,%cpu,%mem,cmd --sort=-%mem | head   # top memory consumers, readable — sorted so the worst offender is right at the top
pstree -p                                            # process tree with PIDs — shows parent/child relationships a flat ps list hides
ps -ef --forest                                      # same idea as pstree, no extra package needed — built into plain ps
top -o %CPU                                          # sort live view by CPU — jumps straight to the worst offender instead of scanning a default-ordered list
```

**Enhanced — priority and I/O control:**
```bash
nice -n 10 ionice -c3 ./heavy_script.sh   # lower CPU priority (nice) + idle I/O class (ionice) — run heavy batch jobs without starving the box
renice -n 5 -p 1234                        # change priority of an already-running process — nice only works at launch, this adjusts one already running
ionice -c2 -n0 -p 1234                     # bump I/O priority of a running PID back up — undo an ionice that's now slowing something down too much
taskset -c 0,1 ./script.sh                 # pin a process to specific CPU cores — stops the scheduler from bouncing it between cores, useful for consistent benchmarking
chrt -r 10 ./script.sh                     # run with real-time scheduling (careful — can starve everything else)
```

**Enhanced — inspecting without killing:**
```bash
kill -0 1234              # exit code 0 = process exists, no signal actually sent — great for scripts
strace -p 1234 -f          # attach to a running process and see every syscall — the fastest way to find exactly what it's stuck on
lsof -p 1234                # every file/socket a process has open — confirms what it's actually touching, not just what you assume
cat /proc/1234/status       # memory, threads, state — no tools needed
cat /proc/1234/limits       # ulimits actually applied to that process — the real enforced limits, not just what's configured system-wide
```

**Enhanced — detach safely:**
```bash
nohup ./script.sh > out.log 2>&1 &   # survives terminal close — the process keeps running after you disconnect or close the SSH session
disown -h %1                          # detach a job from the shell without nohup — useful for a job already running that you forgot to nohup
setsid ./script.sh &                  # fully detach from controlling terminal — stronger than nohup, no terminal signals can reach it at all
```

```bash
pgrep -f myprocess                    # find PIDs by name/command pattern — no ps+grep pipeline needed for the common case
pkill -f myprocess                    # kill by name pattern — skips the step of finding the PID first
jobs -l                               # background jobs in the current shell, with PIDs — confirms what's actually running before fg/kill-ing the wrong one
fg %1                                  # bring background job 1 to the foreground — reattaches so you can interact with it directly
watch -n2 'ps aux --sort=-%cpu | head' # live-refreshing view of top CPU processes, no top needed
ulimit -a                              # every resource limit for the current shell — open files, processes, memory, confirms what's actually enforced
```

**Enhanced — process ancestry and namespaces:**
```bash
ps -o pid,ppid,pgid,sid,comm -p 1234   # full ancestry: parent, process group, session — useful for untangling orphaned processes
cat /proc/1234/cgroup                   # which cgroup(s) a process belongs to — the real capacity limits in a container
readlink /proc/1234/exe                  # the actual binary a PID launched from — even if the file was since replaced
ls -la /proc/1234/fd                      # every open file descriptor for a process — symlinked to its target, shows exactly what files/sockets it's using
```
