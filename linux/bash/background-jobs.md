# Bash — Background Jobs


```bash
long_task &        # run in background
jobs -l             # list background jobs with PIDs
fg %1 / bg %1        # bring to foreground / resume in background
disown -a            # detach all jobs from this shell — they survive shell exit
```
