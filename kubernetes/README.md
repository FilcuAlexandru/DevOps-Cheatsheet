# Kubernetes

*(commands below are `kubectl`; on OpenShift, `oc` is a superset — every `kubectl` command works with `oc` too)*

## Basic

```bash
kubectl config get-contexts                  # list every cluster/context you have configured
kubectl config use-context mycontext           # switch clusters — check this before anything destructive
kubectl config set-context --current --namespace=myns   # stop typing -n myns on every command
kubectl get pods,svc,deploy -n myns              # multiple resource types in one call
kubectl apply -f manifest.yaml                     # create or update from a manifest
kubectl delete -f manifest.yaml                     # remove everything defined in that manifest
kubectl scale deployment/myapp --replicas=3           # scale up/down manually
kubectl port-forward svc/myapp 8080:80                 # reach a cluster service from localhost, no ingress needed
kubectl cp mypod:/var/log/app.log ./app.log             # copy a file out of a running pod
```

```bash
kubectl get pods -o wide --sort-by=.status.startTime   # newest pods last, useful after a rollout
kubectl top pods --sort-by=memory                        # needs metrics-server, but invaluable
kubectl describe pod mypod                                 # events at the bottom are usually the real answer
kubectl logs -f mypod --previous                            # logs from the container BEFORE the last crash — the one you actually need for CrashLoopBackOff
kubectl get events --sort-by='.lastTimestamp' -A            # cluster-wide event stream, chronological
kubectl exec -it mypod -- sh
kubectl create namespace myns              # create a namespace
kubectl delete namespace myns                # delete a namespace and everything in it — destructive
kubectl get all -n myns                        # every common resource type in a namespace at once
kubectl label pod mypod env=prod                 # attach a label to a running resource
kubectl annotate pod mypod note="value"            # attach metadata that isn't used for selection, unlike labels
kubectl get pod mypod -o yaml                        # full resource definition as YAML, including server-set fields
kubectl edit deployment myapp                          # open a live resource in $EDITOR, applies on save
kubectl set image deployment/myapp app=myapp:v2          # update just the image of a container, no manifest edit needed
kubectl rollout status deployment/myapp                    # watch a rollout until it completes or fails
kubectl expose deployment myapp --port=80 --target-port=8080   # quickly create a Service for an existing Deployment
```

**Enhanced:**
```bash
kubectl debug node/mynode -it --image=busybox    # ephemeral debug pod on a node, no SSH needed
kubectl debug mypod -it --image=busybox --target=mypod   # attach a debug container to a running pod (great when the app image has no shell)
kubectl diff -f manifest.yaml                      # see exactly what would change, before you apply
kubectl apply -f manifest.yaml --dry-run=server     # server-side validation without applying
kubectl explain deployment.spec.strategy            # built-in field docs, no browser needed
kubectl rollout undo deployment/myapp                # instant rollback to the previous revision
kubectl rollout history deployment/myapp             # see all revisions before deciding which to roll back to
oc rsh mypod                                          # OpenShift shorthand for exec -it ... sh
oc adm top pods --sort-by=cpu -n mynamespace          # OpenShift admin-level resource view
kubectl get pods --field-selector=status.phase=Running -A   # filter server-side instead of piping through grep
kubectl get pods -l app=myapp --show-labels               # filter by label selector, see every label on the result
kubectl exec -it mypod -c sidecar -- sh                      # target a specific container inside a multi-container pod
kubectl cp mypod:/etc/config.yaml ./config.yaml -c sidecar     # same idea for kubectl cp with multiple containers
kubectl get pod mypod -o jsonpath='{.status.podIP}'              # extract exactly one field, scriptable, no jq needed
kubectl patch deployment myapp -p '{"spec":{"replicas":5}}'        # imperative partial update without a full manifest apply
kubectl wait --for=condition=Ready pod/mypod --timeout=60s           # block until a condition is met, useful in scripts/CI
kubectl auth can-i delete pods -n myns                                 # check your own RBAC permissions before you try and fail
kubectl auth can-i delete pods --as=system:serviceaccount:myns:mysa      # check what a specific service account can do
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
kubectl get nodes -o wide      # confirm there's actually capacity to schedule onto
```

**Pod stuck in `ImagePullBackOff`:**
```bash
kubectl describe pod mypod | grep -A5 Events   # wrong image tag, private registry auth missing, or a typo in the image name — the event message names which one
kubectl get secret <registry_secret> -n mynamespace   # confirm the pull secret actually exists in this namespace, secrets don't cross namespaces
```

**CrashLoopBackOff:**
```bash
kubectl logs mypod --previous            # the crash reason is in the PREVIOUS container's logs, not the new one that just started
kubectl describe pod mypod | grep -A3 "Last State"   # exit code and reason without digging through full logs
```

---
