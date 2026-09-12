# Kubernetes — OpenShift

`oc` extends `kubectl` with OpenShift-specific project, build, and security workflows — every plain `kubectl` command still works, this is what's on top.

```bash
oc login https://api.cluster.example.com:6443 -u <username>   # authenticates the CLI against a cluster's API server, prompts for credentials
oc whoami                                                        # confirm current user, useful after switching contexts/logins
oc new-project <project_name>                                      # create + switch to a new project (OpenShift's namespaced wrapper)
oc project <project_name>                                            # switch between existing projects
oc new-app --image=<registry>/<image>:<tag> --name=<app_name>          # deploy straight from a container image
oc create route edge <route_name> --service=<service_name> --port=<port> --hostname=<hostname>   # expose a service with TLS-terminated Route (OpenShift's built-in Ingress)
oc get routes                                                            # list exposed routes and their hostnames
oc rsh mypod                                                               # shorthand for exec -it ... sh
oc get projects                                                              # every project you can see, across the cluster
oc delete project <project_name>                                              # delete a project and everything in it — destructive
oc status                                                                       # quick visual summary of what's deployed in the current project
oc logs -f dc/myapp                                                              # follow logs for a DeploymentConfig (OpenShift's pre-Deployment resource, still common on older clusters)
oc get build                                                                       # list builds if using OpenShift's built-in S2I/BuildConfig pipeline
oc start-build myapp                                                                # manually trigger a new build
```

**Enhanced:**
```bash
oc adm policy add-scc-to-user anyuid -z <service_account> -n <project>   # grant a Security Context Constraint to a service account — needed when a pod legitimately requires a UID the default restricted-v2 SCC blocks
oc get scc                                                                  # list available SCCs and what each permits
oc adm cordon <node_name> && oc adm drain <node_name> --ignore-daemonsets --delete-emptydir-data   # safely empty a node before maintenance — cordon first so nothing new schedules there, then drain
oc adm top nodes                                                              # node-level resource usage, cluster-wide
oc adm top pods --sort-by=cpu -n <project>                                     # namespace-level pod resource usage
oc adm upgrade                                                                   # check current cluster version and available upgrade path
oc get events --sort-by='.lastTimestamp' -n <project>                              # project-scoped event stream, chronological — same idea as kubectl get events -A, narrowed down
```

## Health check

1. **Correct project active** — `oc project` — red flag: you're in the wrong project — a classic way to "fix" the wrong environment.
2. **Route actually admitted** — `oc get routes` — red flag: missing an `ADMITTED` status — the route exists but isn't actually being served.
3. **No SCC denials** — `oc get events -n <project> | grep -i scc` — red flag: any "unable to validate against any security context constraint" — the pod isn't just failing, it's being actively blocked.

## Troubleshooting

**Pod denied by Security Context Constraint:**
```bash
oc get events -n myproject --sort-by='.lastTimestamp' | grep -i scc   # the denial reason is in the event, naming the exact SCC rule that blocked it
oc get scc restricted-v2 -o yaml         # see exactly what the default SCC does and doesn't allow
```
Before granting a broader SCC like `anyuid`, check whether the image can just be rebuilt to not need root — it's the safer fix and the one that survives a security review.

**Route returns 503 or doesn't resolve:**
```bash
oc get route myroute -o yaml          # confirm the route actually points at the right service and port
oc get endpoints myservice              # empty endpoints means the service has no healthy pods behind it — the route is fine, the backend isn't
```

---
