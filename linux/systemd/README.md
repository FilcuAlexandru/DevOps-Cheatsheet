# Linux — Systemd

Service management and systemd's own journal — a structured, indexed log store, separate from plain-text application log files.

```bash
journalctl -u myservice -f              # follow, like tail -f but for the journal — watch a service's log live as it writes
journalctl -u myservice --since "1 hour ago"
journalctl -p err -b                     # errors only, this boot — filters out noise, scoped to since the last restart
journalctl -k                             # kernel messages only — the journal-native equivalent of dmesg, same data different tool
journalctl --disk-usage                   # how much space the journal itself is using — check before assuming disk pressure is from something else
journalctl -o json-pretty -u myservice   # structured output, pipeable to jq — parse journal entries programmatically instead of scraping text
```

**Enhanced:** `journalctl -f -u myservice --output=cat` strips the timestamp/hostname prefix — much easier to read when you just want the app's own log lines.

```bash
systemctl status myservice
systemctl list-units --failed              # everything currently broken, system-wide, one command — a fast health check before digging into any one service
systemctl show myservice -p MainPID -p ActiveState   # pull specific properties, scriptable — grab just the fields you need instead of parsing full status output
systemd-analyze blame                       # what's slowing down boot, sorted — points straight at the actual bottleneck instead of guessing
systemd-analyze critical-chain               # the actual dependency chain that determines boot time — shows what's waiting on what, not just individual unit times
systemctl edit myservice                     # drop-in override without touching the vendor unit file — survives a package update that would overwrite a direct edit
systemctl daemon-reload                       # required after any unit file change — systemd caches unit definitions, edits won't take effect without this
systemctl mask myservice                      # stronger than disable — prevents even manual start
systemctl start myservice                       # start a stopped service — brings it up immediately, doesn't affect boot-time behavior
systemctl stop myservice                          # stop a running service — takes it down immediately, doesn't affect boot-time behavior
systemctl restart myservice                         # stop then start — a full restart, as opposed to reload which avoids downtime
systemctl reload myservice                            # re-read config without a full restart — avoids downtime, but only works if the service actually supports reload
systemctl enable myservice                              # start automatically on boot — doesn't start it right now, only changes future boot behavior
systemctl disable myservice                               # don't start automatically on boot — doesn't stop it if it's already running now
systemctl cat myservice                                     # print the actual unit file(s) in use — including drop-in overrides
systemctl list-unit-files --type=service                      # every known service unit and its enabled/disabled state — a full inventory of what would start on boot
```

**Enhanced — timers (systemd's cron alternative):**
```bash
systemctl list-timers                            # every scheduled timer and its next run time — the systemd-native way to see "what's scheduled" instead of grepping crontabs
systemctl status mytimer.timer                     # is a specific timer active and enabled — confirms a scheduled job is actually going to fire
journalctl -u mytimer.service                        # a timer's logs live under its paired .service unit — checking the .timer itself won't show the job's actual output
```

## Health check

1. **Is it active** — `systemctl is-active myservice` — red flag: anything other than `active`.
2. **Recent restarts** — `systemctl show myservice -p NRestarts` — red flag: a climbing count means a crash loop, not a one-off.
3. **Other failed units** — `systemctl list-units --failed` — red flag: unrelated services also failed at the same time — points to a shared cause (disk, network) rather than this one service.
4. **Journal around the failure** — `journalctl -u myservice -p err --since "10 min ago"` — red flag: errors clustered right before it went down.

## Troubleshooting

**Service fails to start with no obvious error:**
```bash
systemctl status myservice -l                    # -l shows the full text, not truncated — the real error is often cut off without it
journalctl -xeu myservice                           # -x adds explanatory help text for common failure codes — often explains the fix, not just the error
```

**Changed the unit file but nothing happened:**
```bash
systemctl daemon-reload                # required after ANY change to a unit file — systemd caches the old definition otherwise
systemctl show myservice -p FragmentPath   # confirm which file it's actually reading from — a stray override elsewhere is a common surprise
```

**Journal is using too much disk:**
```bash
journalctl --disk-usage                          # confirm it's actually the journal eating disk — before vacuuming, make sure you're fixing the right thing
journalctl --vacuum-size=500M                       # shrink the journal to a target size — oldest entries drop first, recent history is preserved
journalctl --vacuum-time=7d                           # or keep by age instead of size — whichever matches your retention need
```

---
