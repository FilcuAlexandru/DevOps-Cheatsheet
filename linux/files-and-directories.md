# Linux — Files and Directories


```bash
find / -xdev -type f -size +100M 2>/dev/null   # big files, current filesystem only — -xdev skips crawling mounted NFS shares that would slow this way down
find . -mtime -1                                 # modified in the last 24h — narrows a huge directory down to what actually changed recently
find . -type f -newer reference_file             # anything newer than a given file — compare against a timestamp marker instead of a fixed time window
find . -name '*.log' -mtime +30 -delete           # cleanup — destructive, see Production Safety before running this against anything that matters
```

**Enhanced:**
```bash
rsync -avz --dry-run src/ dst/    # always dry-run a sync before committing to it — confirms what would actually change before it does
xargs -P4 -I{} cmd {}              # parallelize find/xargs pipelines — 4 at a time, much faster on a large file set
diff <(sort file1) <(sort file2)   # process substitution — compare without temp files
comm -23 <(sort a.txt) <(sort b.txt)  # lines in a.txt not in b.txt — a set difference without writing a script for it
```

```bash
tar -czvf archive.tar.gz mydir/     # compress a directory into a gzipped tarball — the standard way to bundle and shrink a folder for transfer
tar -xzvf archive.tar.gz               # extract it back — reverses the tar step above, unpacking the archive into files again
ln -s /path/to/target linkname          # create a symlink — a pointer to another path, not a copy of its contents
stat file.txt                            # detailed metadata: size, timestamps, inode, permissions — more than ls -l shows in one line
readlink -f symlink                       # resolve a symlink to its final real path — follows a chain of links to where they actually point
touch newfile.txt                          # create an empty file, or bump mtime on an existing one — the classic use for confirming a script actually ran
```

**Enhanced — bulk operations:**
```bash
find . -type f -exec md5sum {} \; | sort | uniq -w32 -d   # find duplicate files by content hash across a directory tree — catches true duplicates even with different filenames
rsync -avz --delete src/ dst/                                # mirror src into dst exactly, removing anything in dst that's not in src — destructive, dry-run first
tar --exclude='*.log' -czvf clean.tar.gz mydir/                # archive while excluding a pattern — avoids bundling logs/junk that would just bloat the archive
```
