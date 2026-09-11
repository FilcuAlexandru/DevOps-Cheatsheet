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
