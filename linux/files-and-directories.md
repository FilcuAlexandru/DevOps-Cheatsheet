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
