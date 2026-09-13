# Linux — Disk and Storage


```bash
df -hT                                   # usage + filesystem type — confirms both how full a disk is and what kind of filesystem it is
du -sh --max-depth=1 /var | sort -rh     # find what's eating a directory, sorted biggest-first — narrows a full disk down to the actual culprit fast
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT
findmnt                                  # mount tree, easier to read than plain mount — a cleaner hierarchical view of what's mounted where
```

**Enhanced:**
```bash
lsof +D /var/log            # who has files open under a directory — essential before umount fails
fuser -vm /mnt/data          # what's using a mount point — confirms what's actually holding it open before an unmount fails
iostat -xz 1                 # per-device I/O — the %util column is the one that actually tells you if a disk is the bottleneck
ncdu /var                    # interactive du — much faster to navigate than plain du
: > /var/log/huge.log        # truncate a log file in place without deleting it (keeps the inode/fd alive — safe for a process still writing to it)
```

```bash
mount | column -t                 # currently mounted filesystems, readable columns — confirms what's mounted where without parsing raw output
umount /mnt/data                    # unmount cleanly — fails loudly if something still has an open file on it, rather than silently corrupting data
mount -o remount,rw /                # remount root read-write — recovers from a filesystem that mounted read-only after an unclean shutdown
fdisk -l                              # list partition tables on every disk — confirms the actual partition layout before making any changes
blkid                                  # UUID and filesystem type for every block device — the identifiers /etc/fstab actually relies on
du -h --max-depth=1 . | sort -rh        # same idea as the disk-usage command above, relative to the current directory instead of root
```

**Enhanced — filesystem maintenance:**
```bash
tune2fs -l /dev/sda1              # ext4 filesystem parameters — last check date, mount count, features enabled
fsck -n /dev/sda1                   # check filesystem without fixing anything (-n = answer no to all repairs) — safe on a mounted disk only for inspection
parted -l                             # partition tables with GPT support — fdisk historically struggled with GPT disks, parted doesn't
```
