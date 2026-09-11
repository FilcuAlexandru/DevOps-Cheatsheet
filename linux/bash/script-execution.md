# Bash — Script Execution


```bash
bash -n script.sh          # syntax check only, doesn't run anything
bash -x script.sh           # trace every command as it executes
set -euo pipefail           # fail fast: exit on error, unset var, or failed pipe stage — put this at the top of every script
```
