# Bash — Script Execution


```bash
bash -n script.sh          # syntax check only, doesn't run anything
bash -x script.sh           # trace every command as it executes
set -euo pipefail           # fail fast: exit on error, unset var, or failed pipe stage — put this at the top of every script
```

```bash
bash script.sh arg1 arg2         # positional args available as $1 $2, all of them as $@, count as $#
source ./env.sh                    # run a script in the CURRENT shell, so its variable exports persist afterward (vs a subshell with bash script.sh)
chmod +x script.sh                  # make a script directly executable with ./script.sh
#!/usr/bin/env bash                  # portable shebang — finds bash via PATH instead of assuming /bin/bash exists at that exact path
```

**Enhanced — functions and arrays:**
```bash
my_func() { echo "arg1=$1"; return 0; }   # function definition — $1 etc. are the function's own args, not the script's
local var="value"                            # inside a function, scopes a variable to that function only — always use this over a bare assignment in functions
arr=(one two three); echo "${arr[1]}"          # array literal + zero-indexed access — prints "two"
for item in "${arr[@]}"; do echo "$item"; done   # iterate an array safely, quoted to survive spaces in elements
```
