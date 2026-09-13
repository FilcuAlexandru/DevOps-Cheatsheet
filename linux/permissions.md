# Linux — Permissions


```bash
chmod --reference=file1 file2   # copy permissions from one file to another — replicate a known-good config instead of setting bits manually
getfacl file / setfacl -m u:name:rwx file   # fine-grained ACLs beyond owner/group/other — grant access to a specific extra user without changing group ownership
chattr +i file                    # make a file immutable — even root can't delete or modify it without unsetting this attribute first
find / -perm -4000 2>/dev/null    # find every SUID binary — useful in a security review
sudo -l                           # what you're actually allowed to sudo — confirms real permissions instead of assuming from the sudoers file alone
```

```bash
chown -R user:group /path/to/dir   # change ownership recursively for a whole directory tree — the standard fix after copying files in as the wrong user
umask                                 # current default permission mask for newly created files — explains why new files come out with certain permissions
umask 022                              # set the default mask for this shell session — changes permissions on files created from here on, not existing ones
id username                             # UID, GID, and every group a user belongs to — confirms actual group membership, not just what you assume
groups username                          # just the group membership, shorter form — same info as id, less to parse
```

**Enhanced — auditing:**
```bash
find / -perm -2000 2>/dev/null       # find every SGID binary — same security-review use case as SUID, different bit
getent passwd username                 # confirm a user exists and see their shell/home — works with LDAP/NIS too
visudo -c                               # validate /etc/sudoers syntax before it locks you out — always run this after any manual sudoers edit
```
