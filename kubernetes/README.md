# Kubernetes

*(commands below are `kubectl`; on OpenShift, `oc` is a superset — every `kubectl` command works with `oc` too)*

## Basic

```bash
kubectl config get-contexts                  # list every cluster/context you have configured — confirms which clusters kubectl even knows about
kubectl config use-context mycontext           # switch clusters — check this before anything destructive
kubectl config set-context --current --namespace=myns   # stop typing -n myns on every command — sets the default namespace for this context session
kubectl get pods,svc,deploy -n myns              # multiple resource types in one call — faster than three separate get commands
kubectl apply -f manifest.yaml                     # create or update from a manifest — the standard way to apply any change declaratively
kubectl delete -f manifest.yaml                     # remove everything defined in that manifest — cleaner than deleting resources one by one
kubectl scale deployment/myapp --replicas=3           # scale up/down manually — a quick override outside of an HPA or a manifest edit
kubectl port-forward svc/myapp 8080:80                 # reach a cluster service from localhost — no ingress or public exposure needed just to poke at it
kubectl cp mypod:/var/log/app.log ./app.log             # copy a file out of a running pod — grab a log or config file without exec-ing in first
```

```bash
kubectl get pods -o wide --sort-by=.status.startTime   # newest pods last — quickly confirms a rollout actually replaced the old pods
kubectl top pods --sort-by=memory                        # needs metrics-server installed, but invaluable for spotting a resource-hungry pod fast
kubectl describe pod mypod                                 # events at the bottom are usually the real answer — most people stop reading before they get there
kubectl logs -f mypod --previous                            # logs from the container BEFORE the last crash — the one you actually need for CrashLoopBackOff
kubectl get events --sort-by='.lastTimestamp' -A            # cluster-wide event stream, chronological — catches things happening outside the namespace you were watching
kubectl exec -it mypod -- sh
kubectl create namespace myns              # creates a namespace — a logical partition for grouping related resources with its own RBAC boundary
kubectl delete namespace myns                # delete a namespace and everything in it — destructive
kubectl get all -n myns                        # every common resource type in a namespace at once — a fast full picture instead of querying each type separately
kubectl label pod mypod env=prod                 # attach a label to a running resource — labels are what selectors (Services, Deployments) actually match against
kubectl annotate pod mypod note="value"            # attach metadata that isn't used for selection — good for notes/links, unlike labels which selectors match against
kubectl get pod mypod -o yaml                        # full resource definition as YAML — includes server-set fields your original manifest never had
kubectl edit deployment myapp                          # open a live resource in $EDITOR — applies immediately on save, no separate apply step
kubectl set image deployment/myapp app=myapp:v2          # update just the image of a container — no manifest edit needed for the most common single change
kubectl rollout status deployment/myapp                    # watch a rollout until it completes or fails — blocks instead of you polling get pods repeatedly
kubectl expose deployment myapp --port=80 --target-port=8080   # quickly create a Service for an existing Deployment — skips writing a Service manifest by hand
```

**Enhanced:**
```bash
kubectl debug node/mynode -it --image=busybox    # ephemeral debug pod on a node — no SSH access to the node itself required
kubectl debug mypod -it --image=busybox --target=mypod   # attach a debug container to a running pod — for images with no shell
kubectl diff -f manifest.yaml                      # see exactly what would change — catches a typo or unintended diff before it actually applies
kubectl apply -f manifest.yaml --dry-run=server     # server-side validation without applying — catches errors the API server would reject, without committing to them
kubectl explain deployment.spec.strategy            # built-in field docs, no browser needed — faster than searching the Kubernetes docs site mid-task
kubectl rollout undo deployment/myapp                # instant rollback to the previous revision — the fastest way to undo a bad deploy
kubectl rollout history deployment/myapp             # see all revisions before deciding which to roll back to — rolling back blind can pick the wrong one
oc rsh mypod                                          # OpenShift shorthand for exec -it ... sh — one less flag to remember on OpenShift specifically
oc adm top pods --sort-by=cpu -n mynamespace          # OpenShift admin-level resource view — shows more than a regular user's view would
kubectl get pods --field-selector=status.phase=Running -A   # filter server-side instead of piping through grep — faster and doesn't rely on text matching a field name
kubectl get pods -l app=myapp --show-labels               # filter by label selector — --show-labels reveals every label, not just the one you filtered on
kubectl exec -it mypod -c sidecar -- sh                      # target a specific container inside a multi-container pod — exec without -c hits the first container by default, which may be the wrong one
kubectl cp mypod:/etc/config.yaml ./config.yaml -c sidecar     # same idea as exec -c, but for copying files out of a specific container in a multi-container pod
kubectl get pod mypod -o jsonpath='{.status.podIP}'              # extract exactly one field, scriptable — no piping through jq needed for a simple lookup
kubectl patch deployment myapp -p '{"spec":{"replicas":5}}'        # imperative partial update — changes one field without needing a full manifest apply
kubectl wait --for=condition=Ready pod/mypod --timeout=60s           # block until a condition is met — useful in scripts/CI instead of polling in a loop yourself
kubectl auth can-i delete pods -n myns                                 # check your own RBAC permissions before you try and fail — confirms ahead of time instead of hitting a 403
kubectl auth can-i delete pods --as=system:serviceaccount:myns:mysa      # check what a specific service account can do — useful when debugging a pod's permission errors, not just your own
```

## Health check

1. **Node health** — `kubectl get nodes` — red flag: any node `NotReady`.
2. **Pod status cluster-wide** — `kubectl get pods -A | grep -v Running` — red flag: anything not `Running` or `Completed`.
3. **Recent events** — `kubectl get events -A --sort-by='.lastTimestamp'` — red flag: the same `Warning` event repeating on one object — a single event is often noise, a repeat is a pattern.
4. **Resource pressure** — `kubectl top nodes` — red flag: any node near 100% CPU or memory — new pods may be failing to schedule because of it.

## Troubleshooting

**Pod stuck in `Pending`:**
```bash
kubectl describe pod mypod   # events at the bottom almost always say why — insufficient CPU/memory, no matching node, unbound PVC
kubectl get nodes -o wide      # confirm there's actually capacity to schedule onto — a Pending pod is often just waiting on resources, not broken
```

**Pod stuck in `ImagePullBackOff`:**
```bash
kubectl describe pod mypod | grep -A5 Events   # wrong image tag, private registry auth missing, or a typo in the image name — the event message names which one
kubectl get secret <registry_secret> -n mynamespace   # confirm the pull secret exists in this namespace — secrets don't cross namespaces
```

**CrashLoopBackOff:**
```bash
kubectl logs mypod --previous            # the crash reason is in the PREVIOUS container's logs — the new one just started and hasn't crashed yet
kubectl describe pod mypod | grep -A3 "Last State"   # exit code and reason without digging through full logs — the fast path when you just need the "why", not the whole log
```

---
