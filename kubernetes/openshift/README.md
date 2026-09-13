# Kubernetes — OpenShift

`oc` extends `kubectl` with OpenShift-specific project, build, and security workflows — every plain `kubectl` command still works, this is what's on top.

```bash
oc login https://api.cluster.example.com:6443 -u <username>   # authenticates the CLI against a cluster's API server — required before any other oc command works
oc whoami                                                        # confirm current user — useful after switching contexts/logins to avoid acting as the wrong account
oc new-project <project_name>                                      # create + switch to a new project — OpenShift's namespaced wrapper, adds quota/permissions on top of a plain namespace
oc project <project_name>                                            # switch between existing projects — changes which project subsequent commands target
oc new-app --image=<registry>/<image>:<tag> --name=<app_name>          # deploy straight from a container image — skips writing a manifest for a quick deployment
oc create route edge <route_name> --service=<service_name> --port=<port> --hostname=<hostname>   # expose a service with a TLS-terminated Route — OpenShift's built-in Ingress equivalent
oc get routes                                                            # list exposed routes and their hostnames — confirms what's actually externally reachable
oc rsh mypod                                                               # shorthand for exec -it ... sh — one less flag to type on OpenShift specifically
oc get projects                                                              # every project you can see, across the cluster — scoped to your own RBAC visibility
oc delete project <project_name>                                              # delete a project and everything in it — destructive
oc status                                                                       # quick visual summary of what's deployed in the current project — a fast overview without querying each resource type separately
oc logs -f dc/myapp                                                              # follow logs for a DeploymentConfig — OpenShift's older pre-Deployment resource
oc get build                                                                       # list builds — only relevant if using OpenShift's built-in S2I/BuildConfig pipeline
oc start-build myapp                                                                # manually trigger a new build — rebuilds without waiting for the normal trigger (e.g. a git push)
```

**Enhanced:**
```bash
oc adm policy add-scc-to-user anyuid -z <service_account> -n <project>   # grant a Security Context Constraint to a service account — needed when a pod legitimately requires a UID the default restricted-v2 SCC blocks
oc get scc                                                                  # list available SCCs and what each permits — check before requesting a broader one than actually needed
oc adm cordon <node_name> && oc adm drain <node_name> --ignore-daemonsets --delete-emptydir-data   # safely empty a node before maintenance — cordon first so nothing new schedules there, then drain
oc adm top nodes                                                              # node-level resource usage, cluster-wide — spot an overloaded node before pods start failing to schedule
oc adm top pods --sort-by=cpu -n <project>                                     # namespace-level pod resource usage — narrower than the cluster-wide view, scoped to one project
oc adm upgrade                                                                   # check current cluster version and available upgrade path — confirms what's actually running before assuming a feature exists
oc get events --sort-by='.lastTimestamp' -n <project>                              # project-scoped event stream, chronological — same idea as kubectl get events -A, narrowed down
```

## Health check

1. **Correct project active** — `oc project` — red flag: you're in the wrong project — a classic way to "fix" the wrong environment.
2. **Route actually admitted** — `oc get routes` — red flag: missing an `ADMITTED` status — the route exists but isn't actually being served.
3. **No SCC denials** — `oc get events -n <project> | grep -i scc` — red flag: any "unable to validate against any security context constraint" — the pod isn't just failing, it's being actively blocked.

## Troubleshooting

**Pod denied by Security Context Constraint:**
```bash
oc get events -n myproject --sort-by='.lastTimestamp' | grep -i scc   # the denial reason is in the event — names the exact SCC rule that blocked it, not just "denied"
oc get scc restricted-v2 -o yaml         # see exactly what the default SCC does and doesn't allow — confirms whether a broader SCC is actually needed
```
Before granting a broader SCC like `anyuid`, check whether the image can just be rebuilt to not need root — it's the safer fix and the one that survives a security review.

**Route returns 503 or doesn't resolve:**
```bash
oc get route myroute -o yaml          # confirm the route actually points at the right service and port — a common source of "route exists but doesn't work"
oc get endpoints myservice              # empty endpoints means the service has no healthy pods behind it — the route is fine, the backend isn't
```

---
