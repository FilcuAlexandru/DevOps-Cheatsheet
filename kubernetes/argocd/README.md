# Kubernetes — ArgoCD

ArgoCD syncs cluster state to match what's declared in Git — the core of a GitOps workflow. Most day-to-day work is checking whether an app is actually in sync, and why it isn't.

```bash
argocd login <argocd_host> --username <username>            # authenticate the CLI against an ArgoCD server — required before any other argocd command works
argocd app list                                                # every application ArgoCD is managing, with sync/health status at a glance — a fleet-wide overview in one command
argocd app get <app_name>                                        # detailed status for one app — sync state, health, resources
argocd app sync <app_name>                                         # trigger a manual sync — pulls the latest from Git and applies it to the cluster right now, instead of waiting for auto-sync
argocd app diff <app_name>                                           # preview the diff between Git and the live cluster — before syncing
argocd app history <app_name>                                          # every past sync, with revision and timestamp — confirms exactly when and what was last deployed
argocd app rollback <app_name> <history_id>                              # roll back to a specific prior sync — undoes a bad deploy using the history above
argocd app delete <app_name>                                               # remove an app from ArgoCD — has its own flag for deleting underlying resources too
argocd proj list                                                             # ArgoCD projects — groupings that scope which repos/clusters/namespaces an app can use
argocd app logs <app_name> -f                                                  # stream an app's pod logs via the ArgoCD CLI — no kubectl context switch needed
```

**Enhanced:**
```bash
argocd app sync <app_name> --prune                          # sync and also remove resources that were deleted from Git (off by default — a normal sync leaves orphaned resources alone)
argocd app set <app_name> --sync-policy automated --auto-prune --self-heal   # turn on full GitOps automation — auto-sync, prune, and auto-revert drift
argocd app wait <app_name> --health                            # block until an app reports healthy — useful in CI/CD pipelines after triggering a sync
argocd app resources <app_name>                                  # list every Kubernetes resource this app owns, with individual health — narrows a degraded app down to the specific resource
argocd repo list                                                   # Git repositories ArgoCD is configured to pull from — confirms the actual source before assuming a sync issue
argocd cluster list                                                  # every cluster ArgoCD can deploy to — relevant if this instance manages more than just its own cluster
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
argocd app set myapp --sync-option ApplyOutOfSyncOnly=true   # tell ArgoCD to leave a field alone — for fields that always drift against a controller
```

**App is `Healthy` in ArgoCD but the app itself seems broken:**
```bash
argocd app resources myapp   # health here means "Kubernetes resources reached their expected state" — it does NOT mean your application logic is working
kubectl logs -f deployment/myapp -n mynamespace   # ArgoCD's health check passed the baton — actual app health is on you from here
```

---
