# Check_MK

```bash
cmk -R                              # reload monitoring core config after changes — like a targeted daemon-reload
cmk -II <hostname>                    # rediscover services on a host from scratch (drops manual overrides on that host — see -I below for the safer version)
cmk -I <hostname>                      # discover new services only, keeps existing ones untouched
cmk -d <hostname>                        # show raw agent output for a host — the first thing to check when a check looks wrong
check_mk_agent | less                      # run the agent locally on the monitored host itself, see exactly what it reports before Check_MK even processes it
omd status                                   # status of every service in an OMD site (Check_MK's own site manager)
omd restart <site_name>                        # restart a specific monitoring site
```

**Enhanced:**
```bash
cmk --debug -v <hostname>                   # verbose + full tracebacks on a check that's failing silently otherwise
cmk --scan-parents                            # auto-detect network parent/child relationships for cleaner topology maps
tail -f ~/var/log/web.log                      # Check_MK web UI log, inside the OMD site's home — useful when WATO changes don't seem to take effect
```
A duplicate agent plugin (two versions of the same plugin both executable) silently duplicates output sections — if a check shows doubled or conflicting data, `cmk -d <hostname>` will show the duplication immediately; the fix is disabling the stale plugin version, not debugging the check itself.

## Health check

1. **Site status** — `omd status` — red flag: any component not running (core, apache, etc.).
2. **Host discovery state** — hosts with zero discovered services — red flag: a host that was added but never had `cmk -I` run against it — it looks "monitored" in the list but isn't actually checking anything.

## Troubleshooting

**Host shows as not monitored at all:**
```bash
cmk -d <hostname>                # if this returns nothing, Check_MK can't reach the agent — check network/firewall between the monitoring server and the host first
cmk -I <hostname>                  # if the agent responds but no services show, run discovery — a host with zero discovered services was probably never added properly
```

**Duplicate or conflicting check results:**
```bash
cmk -d <hostname> | grep -c "^<<<"   # count agent output sections — duplicates here mean two versions of the same plugin are both executable on the monitored host
ls -la /usr/lib/check_mk_agent/plugins/   # find and disable the stale one; the fix is removing the old plugin, not debugging the check
```

---
