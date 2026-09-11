# Linux — Disk and Storage


```bash
df -hT                                   # usage + filesystem type
du -sh --max-depth=1 /var | sort -rh     # find what's eating a directory, sorted biggest-first
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT
findmnt                                  # mount tree, easier to read than `mount`
```

**Enhanced:**
```bash
lsof +D /var/log            # who has files open under a directory — essential before umount fails
fuser -vm /mnt/data          # what's using a mount point
iostat -xz 1                 # per-device I/O, %util column is the one that matters
ncdu /var                    # interactive du — much faster to navigate than plain du
: > /var/log/huge.log        # truncate a log file in place without deleting it (keeps the inode/fd alive — safe for a process still writing to it)
```

```bash
mount | column -t                 # currently mounted filesystems, readable columns
umount /mnt/data                    # unmount cleanly
mount -o remount,rw /                # remount root read-write if it came up read-only
fdisk -l                              # list partition tables on every disk
blkid                                  # UUID and filesystem type for every block device
du -h --max-depth=1 . | sort -rh        # same idea as before, relative to current directory
```

**Enhanced — filesystem maintenance:**
```bash
tune2fs -l /dev/sda1              # ext4 filesystem parameters — last check date, mount count, features enabled
fsck -n /dev/sda1                   # check filesystem without fixing anything (-n = answer no to all repairs) — safe on a mounted disk only for inspection
parted -l                             # partition tables with GPT support, where fdisk falls short
```
