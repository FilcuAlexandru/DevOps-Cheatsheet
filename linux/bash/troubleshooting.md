# Bash — Troubleshooting

## Health check

Before trusting any script in production, run through this:

1. **Syntax is valid** — `bash -n script.sh` — red flag: any syntax error, obviously — don't run it.
2. **Safety flags present** — check the top of the file for `set -euo pipefail` — red flag: missing on anything that touches production; a silent partial failure is worse than a loud one.
3. **No hardcoded secrets** — `grep -in "password\|token\|api_key" script.sh` — red flag: any hit that isn't reading from an env var or a secrets manager.
4. **Destructive commands are guarded** — search for `rm -rf`, `DROP`, `DELETE` — red flag: any of these without a confirmation prompt or a `--dry-run` flag ahead of it.

**Script exits with no error message:**
```bash
bash -x ./script.sh 2>&1 | tail -30   # see the last commands executed before it died — the actual failing line is usually right before the output stops
echo $?                                 # exit code of the last command — nonzero means something failed silently
```
Most silent-exit scripts are missing `set -euo pipefail` at the top — without it, a failed command in the middle just gets skipped.

**Script works interactively but fails in cron/CI:**
```bash
env -i /bin/bash --noprofile --norc ./script.sh   # run with a stripped-down environment, closer to what cron actually provides
which <command_used_in_script>                      # confirm the command is on PATH — cron's PATH is much shorter than an interactive shell's
```

---
