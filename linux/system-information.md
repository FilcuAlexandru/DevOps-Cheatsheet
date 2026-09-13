# Linux — System Information


```bash
cat /etc/os-release                  # distro, version — the source of truth systemd itself reads, more reliable than /etc/*-release variants
hostnamectl                          # hostname, kernel, arch, virt type — one command, everything
uname -a                             # kernel version, arch — confirms exactly what you're running before assuming a feature/syscall is available
timedatectl                          # timezone, NTP sync status — check this first on cert/log timing bugs
uptime -p                            # human-readable uptime — quick sanity check on whether a recent restart could explain a symptom
lscpu                                # CPU model, cores, sockets, cache — better than /proc/cpuinfo
lsblk -f                             # block devices + filesystem + mount, in a tree — see the whole disk layout in one readable view
dmidecode -t system                  # hardware/BIOS info — needs root, useful when a bug turns out to be hardware/firmware specific
journalctl --list-boots              # every boot this machine has had, with timestamps — confirms exactly when a restart happened
lspci                                # PCI devices — GPUs, network cards, controllers
lsusb                                # USB devices connected — confirms a device is actually recognized at the hardware level
nproc                                # number of usable CPU cores — respects cgroup limits in containers, the number that actually matters there, not the host's physical count
arch                                 # machine hardware name — confirms the CPU architecture before assuming a binary will even run
hostnamectl set-hostname myserver    # change the hostname permanently — persists across reboots, unlike a plain hostname command
timedatectl set-timezone Europe/Bucharest   # change system timezone — affects how every timestamp on the system is displayed
timedatectl set-ntp true             # enable NTP sync if it's currently off — clock drift causes confusing cert/auth failures that look unrelated
dmesg -T | tail -50                  # last 50 kernel ring buffer messages, human timestamps — recent hardware/driver events without scrolling the whole buffer
cat /proc/version                    # kernel build info — compiler, build date, builder
who -b                               # last system boot time, short form — a one-line answer instead of parsing uptime's longer output
```

**Enhanced:** `hostnamectl` and `timedatectl` in one shot tell you 80% of what you need before touching anything else — especially `timedatectl`, since silent clock drift is behind a surprising number of "random" TLS/Kerberos/cert failures.
```bash
nproc --all                          # total cores including ones a cgroup limit may be hiding from `nproc` alone — the gap between the two is itself diagnostic in containers
cat /sys/class/dmi/id/product_name   # hardware model without needing root — dmidecode usually does need it, this is the unprivileged alternative
systemd-detect-virt                  # confirms bare metal vs VM vs container — and which hypervisor
```
