# Bash — Background Jobs


```bash
long_task &        # run in background — doesn't block the terminal until the command finishes
jobs -l             # list background jobs with PIDs — confirms what's actually running before fg/kill-ing the wrong one
fg %1 / bg %1        # bring to foreground / resume in background — reattach or unpause a specific job by number
disown -a            # detach all jobs from this shell — they survive shell exit
```

```bash
kill %1                    # kill background job 1 by job number — no need to look up the PID first
wait %1                      # block until job 1 finishes — useful before reading its output or exit code, which aren't ready until it completes
wait -n                       # block until ANY background job finishes (not all) — good for basic parallel task management
$!                              # PID of the most recently backgrounded process — capture it right after the & line
```
