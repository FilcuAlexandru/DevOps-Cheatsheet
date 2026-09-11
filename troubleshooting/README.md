# Troubleshooting

## General approach — how to think about any problem

Before running any command, work through this in order. Most time lost in troubleshooting comes from skipping step 1 and jumping straight to guessing.

1. **Confirm the symptom precisely** — what exactly is broken, since when, and for whom (one user, one host, one region, everyone)? "It's slow" and "checkout requests over 2s since 14:03, only in eu-west" are different investigations.
2. **Ask what changed** — a deploy, a config change, a scaling event, a certificate expiry, a scheduled job. Most incidents correlate with a change; find it before you start guessing at causes.
3. **Check the obvious first** — is the process/pod actually running? Any error in the last few log lines? Any alert already fired?
4. **Work through the layers, one at a time** — network reachable → host healthy (CPU/mem/disk) → process running → application logs clean → downstream dependency (DB, API, queue) healthy. Don't skip a layer just because it "should be fine."
5. **Isolate the variable** — does it happen on every node/pod or just one? Every request or just one path? Compare the broken instance against a known-good one — the diff is usually the answer.
6. **Form one hypothesis, test it minimally** — change one thing, observe, then decide the next step. Changing five things at once means you won't know which one fixed it (or made it worse).
7. **Stop the bleeding, then find the root cause** — restarting a service is a valid first move under pressure, but it's a mitigation, not a diagnosis. Don't close the incident until you know *why*.
8. **Close the loop** — write down what happened and why, and add a monitor/alert so the next occurrence is caught automatically instead of by a user complaint.

```text
Symptom confirmed
      │
      ▼
Anything changed recently? ──yes──▶ start there, most likely cause
      │no
      ▼
Is it up at all? ──no──▶ check the process/service layer
      │yes
      ▼
One instance or all? ──one──▶ diff it against a healthy one
      │all
      ▼
Work outward: network → host → process → app logs → dependencies
```

---

**Service is down:**
```bash
systemctl status svc                    # is it even trying to run, and what's the last error
journalctl -u svc -n 100 --no-pager      # recent logs, no pager to fight with
ss -tulnp | grep <port>                   # is anything actually listening
```

**High CPU:**
```bash
top -o %CPU                     # sorted live view, heaviest CPU consumer at the top
ps -eo pid,cmd,%cpu --sort=-%cpu | head
strace -p <pid> -c              # is it doing real work or spinning on syscalls
```

**Disk full:**
```bash
df -h                                    # usage per mounted filesystem, so you know which one is actually full
du -sh --max-depth=1 /suspect | sort -rh  # biggest subdirectories first, one level deep, so you don't guess where the space went
lsof +D /path                             # check for deleted-but-still-open files holding space (df shows full, du doesn't match — classic sign)
```

**Network unreachable:**
```bash
ip route get <ip>          # which route/interface would be used
mtr <host>                   # where exactly it breaks
ss -s                          # socket summary — check for exhaustion (TIME_WAIT pileup etc.)
```

**Cert / TLS issues (familiar territory from eIP):**
```bash
openssl s_client -connect host:443 -servername host </dev/null 2>/dev/null | openssl x509 -noout -dates
keytool -list -v -keystore trust.jks | grep -A1 'Valid from'   # for Java truststores specifically
```

**Slow response times (no outright failure):**
```bash
curl -o /dev/null -s -w '%{time_total}s\n' https://endpoint    # confirm it's actually slow, not just perceived
vmstat 1 5                                                       # CPU-bound vs I/O-bound at a glance
iostat -xz 1                                                     # disk %util — a common hidden cause
kubectl top pods --sort-by=cpu                                    # if it's a specific pod hogging resources
```
Slowness is almost always one of: CPU saturation, I/O wait, a slow downstream dependency, or a bad query — check in that order, it's usually fast to rule three of the four out.

**Recent deploy broke something:**
```bash
kubectl rollout history deployment/myapp     # confirm what actually changed and when
kubectl rollout undo deployment/myapp         # roll back first, investigate after — restore service before root-causing
git log --oneline -10                          # what changed in the code between the working and broken version
kubectl diff -f manifest.yaml                   # if it's a config/manifest change, see exactly what's different
```
Rule of thumb: if a deploy correlates with the incident, roll back before you debug forward — you can investigate the rolled-back version at leisure once service is restored.

---

