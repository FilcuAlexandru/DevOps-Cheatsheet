# Kubernetes — ArgoCD

ArgoCD syncs cluster state to match what's declared in Git — the core of a GitOps workflow. Most day-to-day work is checking whether an app is actually in sync, and why it isn't.

```bash
argocd login <argocd_host> --username <username>            # authenticate the CLI against an ArgoCD server
argocd app list                                                # every application ArgoCD is managing, with sync/health status at a glance
argocd app get <app_name>                                        # detailed status for one app — sync state, health, resources
argocd app sync <app_name>                                         # trigger a manual sync (pull latest from Git, apply to cluster)
argocd app diff <app_name>                                           # see exactly what's different between Git and the live cluster state, before syncing
argocd app history <app_name>                                          # every past sync, with revision and timestamp
argocd app rollback <app_name> <history_id>                              # roll back to a specific prior sync
```

**Enhanced:**
```bash
argocd app sync <app_name> --prune                          # sync and also remove resources that were deleted from Git (off by default — a normal sync leaves orphaned resources alone)
argocd app set <app_name> --sync-policy automated --auto-prune --self-heal   # turn on full GitOps automation: auto-sync on Git changes, prune removed resources, and revert manual cluster drift automatically
argocd app wait <app_name> --health                            # block until an app reports healthy — useful in CI/CD pipelines after triggering a sync
argocd app resources <app_name>                                  # list every Kubernetes resource this app owns, with individual health
argocd repo list                                                   # Git repositories ArgoCD is configured to pull from
argocd cluster list                                                  # every cluster ArgoCD can deploy to, if managing more than one
```

A common source of confusion: **auto-sync ≠ self-heal**. Auto-sync reacts to Git changes; self-heal reacts to someone changing the live cluster directly (kubectl edit, a manual patch) and reverts it back to match Git. Enable both if the goal is "the cluster can never drift from Git," enable only auto-sync if manual emergency patches should be tolerated until the next intentional sync.

## Health check

1. **Sync status** — `argocd app get <app_name>` — red flag: `OutOfSync` — Git and the live cluster have diverged.
2. **Health status** — same command, different field — red flag: `Degraded` or `Missing` — the resources exist but aren't actually healthy.
3. **Last sync result** — `argocd app history <app_name>` — red flag: the most recent sync shows `Failed`, not just an older one — a stale failure isn't urgent, a fresh one is.

## Troubleshooting

**App shows `OutOfSync` but sync doesn't fix it:**
```bash
argocd app diff myapp                 # see exactly what's different — sometimes it's a field a controller keeps overwriting (e.g. replica count under an HPA)
argocd app set myapp --sync-option ApplyOutOfSyncOnly=true   # for known "always drifting" fields, tell ArgoCD to leave them alone rather than fighting a controller
```

**App is `Healthy` in ArgoCD but the app itself seems broken:**
```bash
argocd app resources myapp   # health here means "Kubernetes resources reached their expected state" — it does NOT mean your application logic is working
kubectl logs -f deployment/myapp -n mynamespace   # ArgoCD's health check passed the baton — actual app health is on you from here
```

---
