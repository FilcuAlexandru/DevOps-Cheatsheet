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
