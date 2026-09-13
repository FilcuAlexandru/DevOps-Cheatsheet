# Bash — Script Execution


```bash
bash -n script.sh          # syntax check only — catches a typo before it fails halfway through an actual run
bash -x script.sh           # trace every command as it executes — see exactly what ran and with what values, not just the final result
set -euo pipefail           # fail fast: exit on error, unset var, or failed pipe stage — put this at the top of every script
```

```bash
bash script.sh arg1 arg2         # positional args are available as $1 $2 — all of them as $@, and $# gives you the count
source ./env.sh                    # run a script in the current shell — exports persist afterward, unlike a subshell
chmod +x script.sh                  # make a script directly executable — lets you run it as ./script.sh instead of bash script.sh
#!/usr/bin/env bash                  # portable shebang — finds bash via PATH instead of assuming /bin/bash exists at that exact path
```

**Enhanced — functions and arrays:**
```bash
my_func() { echo "arg1=$1"; return 0; }   # function definition — $1 etc. are the function's own args, not the script's
local var="value"                            # inside a function, scopes a variable to that function only — always use this over a bare assignment in functions
arr=(one two three); echo "${arr[1]}"          # array literal + zero-indexed access — prints "two"
for item in "${arr[@]}"; do echo "$item"; done   # iterate an array safely — quoting survives spaces inside elements that an unquoted loop would split incorrectly
```
