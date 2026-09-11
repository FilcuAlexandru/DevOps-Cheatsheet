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
lspci                                # PCI devices — GPUs, network cards, controllers
lsusb                                # USB devices connected
nproc                                # number of usable CPU cores, respects cgroup limits (containers)
arch                                 # machine hardware name (x86_64, aarch64, etc.)
hostnamectl set-hostname myserver    # change the hostname permanently, survives reboot
timedatectl set-timezone Europe/Bucharest   # change system timezone
timedatectl set-ntp true             # enable NTP sync if it's currently off
dmesg -T | tail -50                  # last 50 kernel ring buffer messages, human timestamps
cat /proc/version                    # kernel build info — compiler, build date, builder
who -b                               # last system boot time, short form
```

**Enhanced:** `hostnamectl` and `timedatectl` in one shot tell you 80% of what you need before touching anything else — especially `timedatectl`, since silent clock drift is behind a surprising number of "random" TLS/Kerberos/cert failures.
```bash
nproc --all                          # total cores including ones a cgroup limit may be hiding from `nproc` alone — the gap between the two is itself diagnostic in containers
cat /sys/class/dmi/id/product_name   # hardware model without needing root (dmidecode usually does)
systemd-detect-virt                  # confirms whether you're on bare metal, a VM, or a container, and which hypervisor
```
