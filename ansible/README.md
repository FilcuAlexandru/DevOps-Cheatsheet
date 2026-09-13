# Ansible

```bash
ansible-playbook site.yml                                   # run a playbook against its default inventory — the standard way to apply it
ansible-playbook site.yml -i <inventory_file>                 # target a specific inventory — overrides the default, useful when managing multiple environments
ansible-playbook site.yml --limit <host_or_group>               # run against a subset of hosts — narrows scope without editing the playbook or inventory
ansible-playbook site.yml --check                                 # dry-run — shows what would change, changes nothing
ansible-playbook site.yml --check --diff                           # dry-run + shows the actual before/after diff per task — see exactly what would change before committing to it
ansible-playbook site.yml --tags <tag_name>                          # run only tasks with a given tag — skips the rest of a long playbook when you just need one part
ansible <host_or_group> -m ping                                       # ad-hoc: confirm connectivity + Python interpreter — the fastest sanity check before trusting any playbook run against a host
ansible <host_or_group> -m shell -a "<command>"                         # ad-hoc: run one command on a group of hosts — no playbook needed for a quick one-off
ansible-inventory -i <inventory_file> --list                              # see what Ansible thinks the inventory looks like — confirms hosts/groups resolved the way you expect
ansible-vault encrypt <file.yml>                                            # encrypt a file containing secrets — safe to commit to git once encrypted
ansible-vault edit <file.yml>                                                # edit an encrypted file in place — decrypts, opens your editor, re-encrypts on save automatically
ansible-vault view <file.yml>                                                 # view without decrypting to disk — reads the content without leaving a plaintext copy behind
ansible-galaxy install -r requirements.yml                                     # install roles/collections a project depends on — required before a playbook using them will actually run
ansible-doc -l                                                                    # list every module available locally — discover what's installed without searching docs online
ansible-doc <module_name>                                                          # full docs + examples for one module — offline, faster than searching online docs mid-task
ansible-config dump --only-changed                                                   # see which config settings differ from Ansible's defaults — confirms what ansible.cfg is actually overriding
ansible-playbook site.yml --list-tasks                                                 # preview every task a playbook would run — a structural check before running anything for real
ansible-playbook site.yml --list-hosts                                                   # preview exactly which hosts a playbook would target — catches a wrong host pattern before it runs
```

**Enhanced:**
```bash
ansible-playbook site.yml --syntax-check           # catch YAML/syntax errors before touching any host — cheap to run, saves a failed run partway through
ansible-playbook site.yml --step                     # confirm each task interactively, one at a time — great for a risky playbook you don't fully trust yet
ansible-playbook site.yml -vvv                         # full verbosity, including the actual module arguments sent to each host — the real debugging tool when a task fails mysteriously
ansible-inventory -i <inventory_file> --graph            # visualize group/host structure as a tree — much faster to read than the raw inventory YAML
ansible <host_or_group> -m setup -a "filter=ansible_distribution*"   # pull just OS facts from a host — no full playbook run needed for a quick fact check
ansible-playbook site.yml --start-at-task="<task_name>"    # resume a long playbook from a specific task — avoids rerunning already-completed steps after a failure
ansible-playbook site.yml --diff --check -e "myvar=value"     # dry-run with a variable override — no playbook/inventory edits needed
ansible all -m setup -a "filter=ansible_default_ipv4"           # pull one fact across every host — fast, no full playbook run
ansible-vault rekey <file.yml>                                     # change the encryption password on a vault-encrypted file — needed after a password rotation
ansible-playbook site.yml --vault-password-file ~/.vault_pass        # supply the vault password from a file — needed for automation
```

## Health check

1. **Connectivity to every host** — `ansible all -m ping` — red flag: any `UNREACHABLE` — fix connectivity before trusting any playbook result from that host.
2. **Facts gathering is consistent** — `ansible all -m setup -a "filter=ansible_distribution*"` — red flag: a host reporting a wildly different OS/version than the rest of the group — it may be in the wrong inventory group entirely.
3. **Dry-run before applying** — `ansible-playbook site.yml --check --diff` — red flag: changes proposed on hosts you expected to be untouched — a sign the play's scope (`hosts:`) is wider than intended.

## Troubleshooting

**Playbook fails on one host only:**
```bash
ansible-playbook site.yml --limit <failing_host> -vvv   # rerun against just that host with full verbosity — isolates the failure and shows exactly what Ansible did
ansible <failing_host> -m setup | head -30                 # confirm facts gathering itself works — a surprising number of "task" failures are actually connection/facts problems
```

**"UNREACHABLE" errors:**
```bash
ansible <host> -m ping -vvv          # shows the exact SSH error — wrong key, wrong user, host key changed, etc.
ssh -vvv <ansible_user>@<host>         # reproduce the connection manually — isolates SSH issues from Ansible itself
```

---
