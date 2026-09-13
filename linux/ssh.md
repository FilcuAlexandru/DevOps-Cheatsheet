# Linux — SSH


```bash
ssh -J bastion user@internal-host        # jump host in one line — no manual tunnel setup needed to reach a host behind another
ssh -N -L 8080:localhost:80 user@host    # local port forward, no shell — great for reaching internal dashboards
ssh -N -D 1080 user@host                  # SOCKS proxy through a single host — routes arbitrary traffic through one SSH connection
ssh-copy-id user@host                     # push your key without manual cat/append — handles the remote authorized_keys file correctly in one step
```

**Enhanced — `~/.ssh/config` aliases:**
```
Host eip-prod
    HostName 10.0.4.12
    User afilcu
    ProxyJump bastion
    ServerAliveInterval 30
```
Then just `ssh eip-prod` — no more remembering IPs, jump hosts, or usernames.

```bash
scp file.txt user@host:/remote/path/        # copy a file to a remote host — the standard one-off file transfer over SSH
scp -r localdir/ user@host:/remote/path/      # recursive copy of a directory — same as scp for a single file, but for a whole tree
sftp user@host                                 # interactive file transfer session — browse and transfer files without a fixed source/destination up front
rsync -avz -e ssh src/ user@host:/dst/           # rsync over SSH — resumable, only transfers diffs
ssh-add ~/.ssh/id_ed25519                          # load a key into the running ssh-agent — stop retyping its passphrase for every new connection
ssh-add -l                                          # list keys currently loaded in the agent — confirms which identity will actually be offered
```

**Enhanced — connection multiplexing:**
```
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```
Add this to `~/.ssh/config` once, and every subsequent SSH connection to a host you're already connected to reuses the existing TCP/auth handshake — noticeably faster for repeated `scp`/`git` operations over SSH to the same host, and each new session shares one already-authenticated connection instead of renegotiating.
