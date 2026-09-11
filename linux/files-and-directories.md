# Linux — Files and Directories


```bash
find / -xdev -type f -size +100M 2>/dev/null   # big files, current filesystem only (no NFS crawl)
find . -mtime -1                                 # modified in the last 24h
find . -type f -newer reference_file             # anything newer than a given file
find . -name '*.log' -mtime +30 -delete           # cleanup, but see Production Safety first
```

**Enhanced:**
```bash
rsync -avz --dry-run src/ dst/    # always dry-run a sync before committing to it
xargs -P4 -I{} cmd {}              # parallelize find/xargs pipelines (4 at a time)
diff <(sort file1) <(sort file2)   # process substitution — compare without temp files
comm -23 <(sort a.txt) <(sort b.txt)  # lines in a.txt not in b.txt
```

```bash
tar -czvf archive.tar.gz mydir/     # compress a directory into a gzipped tarball
tar -xzvf archive.tar.gz               # extract it back
ln -s /path/to/target linkname          # create a symlink
stat file.txt                            # detailed metadata: size, timestamps, inode, permissions
readlink -f symlink                       # resolve a symlink to its final real path
touch newfile.txt                          # create an empty file, or bump mtime on an existing one
```

**Enhanced — bulk operations:**
```bash
find . -type f -exec md5sum {} \; | sort | uniq -w32 -d   # find duplicate files by content hash across a directory tree
rsync -avz --delete src/ dst/                                # mirror src into dst exactly, removing anything in dst that's not in src — destructive, dry-run first
tar --exclude='*.log' -czvf clean.tar.gz mydir/                # archive while excluding a pattern, avoids bundling logs/junk
```
