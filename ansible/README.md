# Ansible

```bash
ansible-playbook site.yml                                   # run a playbook against its default inventory
ansible-playbook site.yml -i <inventory_file>                 # target a specific inventory
ansible-playbook site.yml --limit <host_or_group>               # run against a subset of hosts
ansible-playbook site.yml --check                                 # dry-run — shows what would change, changes nothing
ansible-playbook site.yml --check --diff                           # dry-run + shows the actual before/after diff per task
ansible-playbook site.yml --tags <tag_name>                          # run only tasks with a given tag
ansible <host_or_group> -m ping                                       # ad-hoc: confirm connectivity + Python interpreter
ansible <host_or_group> -m shell -a "<command>"                         # ad-hoc: run one command on a group of hosts
ansible-inventory -i <inventory_file> --list                              # see what Ansible thinks the inventory looks like
ansible-vault encrypt <file.yml>                                            # encrypt a file containing secrets
ansible-vault edit <file.yml>                                                # edit an encrypted file in place
ansible-vault view <file.yml>                                                 # view without decrypting to disk
ansible-galaxy install -r requirements.yml                                     # install roles/collections a project depends on
ansible-doc -l                                                                    # list every module available locally
ansible-doc <module_name>                                                          # full docs + examples for one module, offline
ansible-config dump --only-changed                                                   # see which config settings differ from Ansible's defaults, e.g. from ansible.cfg
ansible-playbook site.yml --list-tasks                                                 # preview every task a playbook would run, without executing anything
ansible-playbook site.yml --list-hosts                                                   # preview exactly which hosts a playbook would target
```

**Enhanced:**
```bash
ansible-playbook site.yml --syntax-check           # catch YAML/syntax errors before touching any host
ansible-playbook site.yml --step                     # confirm each task interactively, one at a time — great for a risky playbook you don't fully trust yet
ansible-playbook site.yml -vvv                         # full verbosity, including the actual module arguments sent to each host — the real debugging tool when a task fails mysteriously
ansible-inventory -i <inventory_file> --graph            # visualize group/host structure as a tree, faster to read than the raw YAML
ansible <host_or_group> -m setup -a "filter=ansible_distribution*"   # pull just OS facts from a host without a full playbook run
ansible-playbook site.yml --start-at-task="<task_name>"    # resume a long playbook from a specific task instead of rerunning everything
ansible-playbook site.yml --diff --check -e "myvar=value"     # combine a dry-run with an extra variable override, without editing the playbook or inventory
ansible all -m setup -a "filter=ansible_default_ipv4"           # pull just one fact (e.g. the default network interface/IP) across every host, fast
ansible-vault rekey <file.yml>                                     # change the encryption password on a vault-encrypted file
ansible-playbook site.yml --vault-password-file ~/.vault_pass        # supply the vault password from a file instead of typing it interactively, for automation
```

## Health check

1. **Connectivity to every host** — `ansible all -m ping` — red flag: any `UNREACHABLE` — fix connectivity before trusting any playbook result from that host.
2. **Facts gathering is consistent** — `ansible all -m setup -a "filter=ansible_distribution*"` — red flag: a host reporting a wildly different OS/version than the rest of the group — it may be in the wrong inventory group entirely.
3. **Dry-run before applying** — `ansible-playbook site.yml --check --diff` — red flag: changes proposed on hosts you expected to be untouched — a sign the play's scope (`hosts:`) is wider than intended.

## Troubleshooting

**Playbook fails on one host only:**
```bash
ansible-playbook site.yml --limit <failing_host> -vvv   # rerun against just that host with full verbosity
ansible <failing_host> -m setup | head -30                 # confirm facts gathering itself works — a surprising number of "task" failures are actually connection/facts problems
```

**"UNREACHABLE" errors:**
```bash
ansible <host> -m ping -vvv          # shows the exact SSH error — wrong key, wrong user, host key changed, etc.
ssh -vvv <ansible_user>@<host>         # reproduce the same connection manually, outside Ansible, to isolate SSH from Ansible itself
```

---
