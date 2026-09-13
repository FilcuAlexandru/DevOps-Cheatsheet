# Vault (HashiCorp)

```bash
export VAULT_ADDR="https://<vault_host>:8200"          # point the CLI at your Vault server — every other command needs this set first
vault login                                              # interactive login — the actual method depends on what auth backend is configured (token, LDAP, etc.)
vault status                                               # is Vault up, sealed, and which node is active — nothing else works if it's sealed
vault secrets list                                           # every secrets engine mounted — confirms what's actually available before trying to read from it
vault kv get secret/<path>                                     # read a secret from a KV v2 engine — the everyday command for pulling a stored value
vault kv get -field=<key> secret/<path>                          # pull just one field, scriptable — skips parsing the full JSON response for a single value
vault kv put secret/<path> <key>=<value>                           # creates the secret if it doesn't exist, or adds a new version if it does — KV v2 keeps history either way
vault kv list secret/<path>                                          # list keys under a path — discover what exists without reading (or having permission to read) the actual values
vault token lookup                                                     # inspect your current token — policies, TTL, renewable
vault policy list                                                        # every policy defined on this Vault — an inventory before checking what any one of them actually grants
vault policy read <policy_name>                                           # see exactly what a policy allows — confirms access before assuming a permission denial is a bug
vault kv delete secret/<path>                                               # soft-delete the current version — KV v2 keeps history, so this is recoverable, not gone for good
vault kv undelete -versions=<n> secret/<path>                                 # recover a soft-deleted version — undoes the soft-delete above if it was a mistake
vault kv metadata get secret/<path>                                             # version history and metadata for a secret — see what changed and when, without needing read access to the values themselves
vault auth list                                                                    # every auth method enabled — confirms which ways exist to actually authenticate to this Vault
vault list secret/                                                                   # list top-level paths in a KV mount — useful for discovering what exists
vault lease revoke <lease_id>                                                          # manually revoke a dynamic secret's lease — cuts off access immediately instead of waiting for natural expiry
```

**Enhanced:**
```bash
vault kv get -format=json secret/<path> | jq '.data.data'   # pull a secret as JSON and extract with jq — the practical way to use Vault output in scripts
vault kv get -version=<n> secret/<path>                        # KV v2 keeps history — read a previous version instead of the current one
vault read database/creds/<role_name>                            # dynamic secret: get a short-lived DB credential — expires automatically, no static password to leak or rotate manually
vault token renew                                                  # extend your current token's TTL — avoids losing access mid-task if the original TTL was too short
vault audit list                                                     # confirm audit logging is actually enabled — worth checking once per environment, not assuming
VAULT_TOKEN=<token> vault kv get secret/<path>                         # pass a token inline for a one-off command — careful, it hits shell history
vault kv patch secret/<path> <key>=<value>                              # update just one field without overwriting the whole secret — KV v2 only, avoids clobbering fields you didn't mean to touch
vault token create -policy=<policy_name> -ttl=1h                          # issue a short-lived scoped token — for automation, instead of sharing your own
vault secrets tune -max-lease-ttl=8h secret/                                # cap how long dynamic secrets from this mount can live — tightens the default max lease, reduces exposure window
```

**Server operations (if you're the one running Vault, not just a client):**
```bash
vault operator init -key-shares=5 -key-threshold=3   # first-time init — generates unseal keys and the initial root token; store the keys somewhere that isn't this terminal's history
vault operator unseal <unseal_key>                      # submit one unseal key — repeat key-threshold times after any restart
vault secrets enable database                             # enable a secrets engine before it can be used — nothing under that path works until it's mounted
vault policy write <policy_name> <policy_file.hcl>           # apply an access policy from an HCL file — the standard way to define what a token/role can actually do
```

## Health check

1. **Seal status** — `vault status` — red flag: `Sealed: true` — nothing else works until this is resolved.
2. **Cluster leader** (if HA) — check the leader field in `vault status` — red flag: no active leader, or frequent leader changes — points to network partitioning between nodes.
3. **Your token's health** — `vault token lookup` — red flag: TTL near zero — renew before it expires mid-task, not after.

## Troubleshooting

**Vault is sealed:**
```bash
vault status                       # confirms sealed state and how many unseal keys have been submitted — tells you exactly how far through unsealing you are
vault operator unseal <unseal_key>   # run key-threshold times total — by different key holders if properly distributed
```

**"permission denied" reading a secret you expect to have access to:**
```bash
vault token lookup                     # check which policies are actually attached to your current token — confirms your real access before assuming a permission problem
vault policy read <policy_name>          # confirm the policy actually grants the path you're trying to read — a common gap is granting secret/data/x but not secret/metadata/x, which some operations also need
```

---
