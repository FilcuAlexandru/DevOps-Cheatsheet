# Vault (HashiCorp)

```bash
export VAULT_ADDR="https://<vault_host>:8200"          # point the CLI at your Vault server
vault login                                              # interactive login (token, LDAP, etc. depending on configured auth method)
vault status                                               # is Vault up, sealed, and which node is active
vault secrets list                                           # every secrets engine mounted (kv, database, pki, etc.)
vault kv get secret/<path>                                     # read a secret from a KV v2 engine
vault kv get -field=<key> secret/<path>                          # pull just one field, scriptable
vault kv put secret/<path> <key>=<value>                           # creates the secret if it doesn't exist yet, or adds a new version if it does
vault kv list secret/<path>                                          # list keys under a path, without reading values
vault token lookup                                                     # inspect your current token — policies, TTL, renewable
vault policy list                                                        # every policy defined on this Vault
vault policy read <policy_name>                                           # see exactly what a policy allows
```

**Enhanced:**
```bash
vault kv get -format=json secret/<path> | jq '.data.data'   # pull a secret as JSON and extract with jq — the practical way to use Vault output in scripts
vault kv get -version=<n> secret/<path>                        # KV v2 keeps history — read a previous version instead of the current one
vault read database/creds/<role_name>                            # dynamic secret: get a short-lived DB credential instead of a static password
vault token renew                                                  # extend your current token's TTL before it expires mid-task
vault audit list                                                     # confirm audit logging is actually enabled — worth checking once per environment, not assuming
VAULT_TOKEN=<token> vault kv get secret/<path>                         # pass a token inline for a one-off command without a full login (careful with shell history)
```

**Server operations (if you're the one running Vault, not just a client):**
```bash
vault operator init -key-shares=5 -key-threshold=3   # first-time init — generates unseal keys and the initial root token; store the keys somewhere that isn't this terminal's history
vault operator unseal <unseal_key>                      # submit one unseal key; needs to be run key-threshold times after any restart, unless auto-unseal is configured
vault secrets enable database                             # enable a secrets engine (here, dynamic database credentials) before it can be used
vault policy write <policy_name> <policy_file.hcl>           # apply an access policy from an HCL file
```

## Health check

1. **Seal status** — `vault status` — red flag: `Sealed: true` — nothing else works until this is resolved.
2. **Cluster leader** (if HA) — check the leader field in `vault status` — red flag: no active leader, or frequent leader changes — points to network partitioning between nodes.
3. **Your token's health** — `vault token lookup` — red flag: TTL near zero — renew before it expires mid-task, not after.

## Troubleshooting

**Vault is sealed:**
```bash
vault status                       # confirms sealed state and how many unseal keys have been submitted so far
vault operator unseal <unseal_key>   # needs to be run key-threshold times total, by different key holders if keys are properly distributed
```

**"permission denied" reading a secret you expect to have access to:**
```bash
vault token lookup                     # check which policies are actually attached to your current token
vault policy read <policy_name>          # confirm the policy actually grants the path you're trying to read — a common gap is granting secret/data/x but not secret/metadata/x, which some operations also need
```

---
