# Linux — Permissions


```bash
chmod --reference=file1 file2   # copy permissions from one file to another
getfacl file / setfacl -m u:name:rwx file   # fine-grained ACLs beyond owner/group/other
chattr +i file                    # make a file immutable, even root can't delete it without unsetting first
find / -perm -4000 2>/dev/null    # find every SUID binary — useful in a security review
sudo -l                           # what you're actually allowed to sudo, before you assume
```
