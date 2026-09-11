# Linux — Systemd

Service management and systemd's own journal — a structured, indexed log store, separate from plain-text application log files.

```bash
journalctl -u myservice -f              # follow, like tail -f but for the journal
journalctl -u myservice --since "1 hour ago"
journalctl -p err -b                     # errors only, this boot
journalctl -k                             # kernel messages only (dmesg equivalent)
journalctl --disk-usage                   # how much space the journal itself is using
journalctl -o json-pretty -u myservice   # structured output, pipeable to jq
```

**Enhanced:** `journalctl -f -u myservice --output=cat` strips the timestamp/hostname prefix — much easier to read when you just want the app's own log lines.

```bash
systemctl status myservice
systemctl list-units --failed              # everything currently broken, system-wide, one command
systemctl show myservice -p MainPID -p ActiveState   # pull specific properties, scriptable
systemd-analyze blame                       # what's slowing down boot, sorted
systemd-analyze critical-chain               # the actual dependency chain that determines boot time
systemctl edit myservice                     # drop-in override without touching the vendor unit file
systemctl daemon-reload                       # required after any unit file change
systemctl mask myservice                      # stronger than disable — prevents even manual start
systemctl start myservice                       # start a stopped service
systemctl stop myservice                          # stop a running service
systemctl restart myservice                         # stop then start
systemctl reload myservice                            # re-read config without a full restart, if the service supports it
systemctl enable myservice                              # start automatically on boot
systemctl disable myservice                               # don't start automatically on boot (doesn't stop it now)
systemctl cat myservice                                     # print the actual unit file(s) being used, including drop-in overrides, without hunting for the path
systemctl list-unit-files --type=service                      # every known service unit and its enabled/disabled state
```

**Enhanced — timers (systemd's cron alternative):**
```bash
systemctl list-timers                            # every scheduled timer and its next run time — the systemd-native way to see "what's scheduled" instead of grepping crontabs
systemctl status mytimer.timer                     # is a specific timer active and enabled
journalctl -u mytimer.service                        # a timer's logs live under its paired .service unit, not the .timer itself
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
journalctl -xeu myservice                           # -x adds explanatory help text for common failure codes, -e jumps to the end
```

**Changed the unit file but nothing happened:**
```bash
systemctl daemon-reload                # required after ANY change to a unit file — systemd caches the old definition otherwise
systemctl show myservice -p FragmentPath   # confirm which file it's actually reading from — a stray override elsewhere is a common surprise
```

**Journal is using too much disk:**
```bash
journalctl --disk-usage                          # confirm it's actually the journal, not something else
journalctl --vacuum-size=500M                       # shrink the journal down to a target size, oldest entries dropped first
journalctl --vacuum-time=7d                           # or keep by age instead of size — whichever matches your retention need
```

---
