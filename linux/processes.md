# Linux — Processes


```bash
ps -eo pid,ppid,%cpu,%mem,cmd --sort=-%mem | head   # top memory consumers, readable
pstree -p                                            # process tree with PIDs
ps -ef --forest                                      # same idea, no extra package needed
top -o %CPU                                          # sort live view by CPU
```

**Enhanced — priority and I/O control:**
```bash
nice -n 10 ionice -c3 ./heavy_script.sh   # lower CPU priority (nice) + idle I/O class (ionice) — run heavy batch jobs without starving the box
renice -n 5 -p 1234                        # change priority of an already-running process
ionice -c2 -n0 -p 1234                     # bump I/O priority of a running PID back up
taskset -c 0,1 ./script.sh                 # pin a process to specific CPU cores
chrt -r 10 ./script.sh                     # run with real-time scheduling (careful — can starve everything else)
```

**Enhanced — inspecting without killing:**
```bash
kill -0 1234              # exit code 0 = process exists, no signal actually sent — great for scripts
strace -p 1234 -f          # attach to a running process, see every syscall (find what it's stuck on)
lsof -p 1234                # every file/socket a process has open
cat /proc/1234/status       # memory, threads, state — no tools needed
cat /proc/1234/limits       # ulimits actually applied to that process
```

**Enhanced — detach safely:**
```bash
nohup ./script.sh > out.log 2>&1 &   # survives terminal close
disown -h %1                          # detach a job from the shell without nohup
setsid ./script.sh &                  # fully detach from controlling terminal (stronger than nohup)
```

```bash
pgrep -f myprocess                    # find PIDs by name/command pattern, no ps+grep pipeline needed
pkill -f myprocess                    # kill by name pattern instead of hunting for the PID first
jobs -l                               # background jobs in the current shell, with PIDs
fg %1                                  # bring background job 1 to the foreground
watch -n2 'ps aux --sort=-%cpu | head' # live-refreshing view of top CPU processes, no top needed
ulimit -a                              # every resource limit (open files, processes, memory) for the current shell
```

**Enhanced — process ancestry and namespaces:**
```bash
ps -o pid,ppid,pgid,sid,comm -p 1234   # full ancestry: parent, process group, session — useful for untangling orphaned processes
cat /proc/1234/cgroup                   # which cgroup(s) a process belongs to — the real capacity limits in a container
readlink /proc/1234/exe                  # the actual binary a running PID was launched from, even if the file was since replaced
ls -la /proc/1234/fd                      # every open file descriptor for a process, symlinked to its target
```
