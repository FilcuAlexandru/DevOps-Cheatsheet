# Bash — Background Jobs


```bash
long_task &        # run in background
jobs -l             # list background jobs with PIDs
fg %1 / bg %1        # bring to foreground / resume in background
disown -a            # detach all jobs from this shell — they survive shell exit
```

```bash
kill %1                    # kill background job 1 by job number, not PID
wait %1                      # block until job 1 finishes, useful before reading its output/exit code
wait -n                       # block until ANY background job finishes (not all) — good for basic parallel task management
$!                              # PID of the most recently backgrounded process — capture it right after the & line
```
