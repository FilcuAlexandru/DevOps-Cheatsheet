# Linux — Permissions


```bash
chmod --reference=file1 file2   # copy permissions from one file to another
getfacl file / setfacl -m u:name:rwx file   # fine-grained ACLs beyond owner/group/other
chattr +i file                    # make a file immutable, even root can't delete it without unsetting first
find / -perm -4000 2>/dev/null    # find every SUID binary — useful in a security review
sudo -l                           # what you're actually allowed to sudo, before you assume
```

```bash
chown -R user:group /path/to/dir   # change ownership recursively for a whole directory tree
umask                                 # current default permission mask for newly created files
umask 022                              # set the default mask for this shell session
id username                             # UID, GID, and every group a user belongs to
groups username                          # just the group membership, shorter form
```

**Enhanced — auditing:**
```bash
find / -perm -2000 2>/dev/null       # find every SGID binary — same security-review use case as SUID, different bit
getent passwd username                 # confirm a user actually exists and see their shell/home, works with LDAP/NIS too, not just /etc/passwd
visudo -c                               # validate /etc/sudoers syntax before it locks you out — always run this after any manual sudoers edit
```
