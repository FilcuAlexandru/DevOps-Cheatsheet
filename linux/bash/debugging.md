# Bash — Debugging


```bash
set -x   # turn tracing on mid-script
set +x   # turn it back off (bracket only the suspicious block)
trap 'echo "failed at line $LINENO"' ERR   # know exactly where a script died
PS4='+ $(date "+%T") ${BASH_SOURCE}:${LINENO}: '   # timestamped trace output when combined with set -x
```

**Enhanced:**
```bash
exec 5>debug.log; BASH_XTRACEFD=5; set -x   # send xtrace output to its own file descriptor/file instead of stderr — lets you debug a script without its trace lines mixing into real stderr output that other tools might parse
```

```bash
shellcheck script.sh          # static analysis — catches quoting bugs, unused vars, and common mistakes before you run anything
bash -u script.sh               # treat unset variables as an error and exit — catches typos in variable names
echo "DEBUG: var=$var" >&2       # a poor man's breakpoint — send debug output to stderr so it doesn't pollute stdout a caller might be parsing
```
