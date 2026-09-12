# Kubernetes — Helm

Helm is the package manager for Kubernetes — bundles of templated manifests (charts) with configurable values, installed as a named "release."

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami   # add a chart repository
helm repo update                                              # refresh the local index of available charts
helm search repo <name>                                         # find a chart across added repos
helm install <release_name> <chart> --set <key>=<value>           # install, overriding one value inline
helm upgrade <release_name> <chart> -f custom-values.yaml           # upgrade using a full values file instead of one-off --set flags
helm list -A                                                          # every release across every namespace
helm history <release_name>                                            # revision history for a release
helm rollback <release_name> <revision_number>                           # roll back to a specific prior revision
helm uninstall <release_name>                                              # remove a release entirely
helm show values <chart>                                                     # every configurable value a chart exposes, with its default
helm show chart <chart>                                                        # chart metadata — version, description, dependencies
helm get manifest <release_name>                                                 # the exact rendered YAML currently applied for a release
helm dependency update <chart>                                                     # fetch/update a chart's subchart dependencies
```

**Enhanced:**
```bash
helm upgrade --install <release_name> <chart> --atomic --timeout 5m   # atomic upgrade: automatically rolls back if anything fails health checks — much safer than a bare upgrade for anything production-facing
helm template <release_name> <chart> -f values.yaml                     # render the final YAML locally, no cluster contact — see exactly what would be applied before it touches anything
helm lint <chart>                                                          # catch chart syntax/best-practice issues before packaging or installing
helm get values <release_name>                                              # see the actual values currently in effect for a running release, not just what's in your local file
helm diff upgrade <release_name> <chart> -f values.yaml                       # (needs the helm-diff plugin) preview exactly what an upgrade would change — the Helm equivalent of kubectl diff
```

## Health check

1. **Release status** — `helm status <release_name>` — red flag: anything other than `deployed`.
2. **Recent history** — `helm history <release_name>` — red flag: the most recent revision shows `failed` or `superseded` right after a fresh install (a bad rollout that never got cleaned up).
3. **No drift from what's declared** — `helm diff upgrade <release_name> <chart> -f values.yaml` (needs the plugin) — red flag: unexpected differences — someone patched the cluster directly instead of through Helm.

## Troubleshooting

**Release stuck in `pending-upgrade` or `pending-install`:**
```bash
helm status myrelease           # confirm it's actually stuck, not just slow
helm history myrelease            # find the last known-good revision
kubectl delete secret -l owner=helm,name=myrelease,status=pending-upgrade -n mynamespace   # Helm's lock on a stuck release lives in a Secret — removing it (carefully) unblocks the next helm command
```

**Upgrade fails halfway through:**
```bash
helm rollback myrelease                # if --atomic wasn't used, roll back manually to the last good revision
helm upgrade myrelease mychart --atomic --timeout 5m   # use --atomic next time so a failed upgrade rolls back automatically instead of leaving things half-applied
```

---
