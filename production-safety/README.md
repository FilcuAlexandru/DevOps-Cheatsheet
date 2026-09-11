# Production Safety

- **Dry-run first, always:** `--dry-run`, `rsync --dry-run`, `kubectl diff`, `kubectl apply --dry-run=server` — if the tool has one, use it before the real run.
- **Destructive commands get a pause:** `alias rm='rm -i'` in your interactive shell; never alias it in scripts (breaks non-interactive automation).
- **Long-running or risky ops go in `tmux`/`screen`**, not a raw SSH session — a dropped connection shouldn't kill a migration.
- **Confirm the target before you act:**
  ```bash
  kubectl config current-context     # you WILL eventually run the right command in the wrong cluster otherwise
  echo $PS1 | grep -i prod            # visual cue in your prompt for prod boxes, worth setting up
  ```
- **Truncate, don't delete, live log files:** `: > file.log` keeps the inode a running process is writing to; `rm` on a still-open file just hides the space until the process exits.
- **Snapshot/backup before schema or config changes** — even a quick `cp file.conf file.conf.bak.$(date +%s)` beats reconstructing from memory at 2am.

---
