# Linux — System Information


```bash
cat /etc/os-release                  # distro, version
hostnamectl                          # hostname, kernel, arch, virt type — one command, everything
uname -a                             # kernel version, arch
timedatectl                          # timezone, NTP sync status — check this first on cert/log timing bugs
uptime -p                            # human-readable uptime
lscpu                                # CPU model, cores, sockets, cache — better than /proc/cpuinfo
lsblk -f                             # block devices + filesystem + mount, in a tree
dmidecode -t system                  # hardware/BIOS info (needs root)
journalctl --list-boots              # every boot this machine has had, with timestamps
```

**Enhanced:** `hostnamectl` and `timedatectl` in one shot tell you 80% of what you need before touching anything else — especially `timedatectl`, since silent clock drift is behind a surprising number of "random" TLS/Kerberos/cert failures.
