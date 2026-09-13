# Docker

```bash
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'   # readable custom columns — faster to scan than the default ps output
docker logs -f --since 10m mycontainer
docker exec -it mycontainer sh                # get a shell in a running container — for poking around inside a live container
docker run --rm -it --entrypoint sh myimage   # inspect an image without running its default command — overrides the entrypoint just to look around
docker stats --no-stream                       # one-shot resource usage snapshot — --no-stream avoids the live-updating view when you just want a quick read
docker system df                                # disk usage breakdown by images/containers/volumes — shows where Docker's actually spending disk space
docker system prune -af --volumes               # reclaim space — destructive, see Production Safety
docker inspect --format '{{.State.Health.Status}}' mycontainer   # pull one field instead of parsing full JSON — scriptable without needing jq
docker build -t myimage:v1 .                    # build an image from a Dockerfile in the current directory — the standard local build step
docker pull myimage:v1                            # download an image from a registry without running it — useful to pre-fetch before a deploy
docker push myregistry/myimage:v1                   # upload an image to a registry — makes it available for others/other hosts to pull
docker tag myimage:v1 myregistry/myimage:v1           # add a new tag to an existing local image — registries often need a specific tag format before push
docker rm mycontainer                                   # remove a stopped container — frees the disk space it was holding
docker rmi myimage:v1                                     # remove a local image — frees disk space once nothing needs it anymore
docker cp mycontainer:/app/log.txt ./log.txt                # copy a file out of a container without exec-ing in — faster for a single file grab
docker top mycontainer                                         # processes running inside a container, from the host's view — like ps, but scoped to that container
docker diff mycontainer                                          # files changed vs the image's original filesystem — useful for spotting unexpected writes
```

**Enhanced — images and builds:**
```bash
docker build --no-cache -t myimage:v1 .        # force a full rebuild, ignoring cached layers — use when you suspect a stale cached layer is the problem
docker history myimage:v1                         # every layer in an image, with size — find what's bloating it
docker image prune -a                                # remove all unused images, not just dangling ones — more aggressive than a bare prune
docker run --rm -it --user 0 myimage sh                # drop in as root — overrides the image's default user, for debugging permissions
docker logs --details mycontainer                        # include extra attributes in log output — labels etc., not just the line itself
```

---

## Docker Compose

```bash
docker compose up -d                         # start everything in the background — the standard way to bring a stack up without blocking the terminal
docker compose up -d --build                  # rebuild images first, then start — needed after a Dockerfile change, otherwise up reuses the old image
docker compose down                            # stop and remove containers, networks — volumes are kept by default, add -v to also remove those
docker compose down -v                          # also remove volumes — destructive, see Production Safety
docker compose ps                                # status of every service in this project — confirms what's actually running vs defined
docker compose logs -f service_name               # follow logs for one service only — narrower than following the whole stack's combined logs
docker compose exec service_name sh                # shell into a running service — same idea as docker exec, scoped by compose service name
docker compose restart service_name                 # restart one service without touching the rest — faster than a full compose down/up
docker compose config                                # render the fully resolved config (env vars, overrides applied) — great for debugging "why isn't my variable being picked up"
```

**Enhanced:**
```bash
docker compose up -d --scale worker=3      # run 3 instances of one service — a quick way to test load-balancing or scaling behavior locally
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d   # explicitly combine multiple compose files — useful when override files aren't in the default auto-discovered location
docker compose logs -f --tail=100 service_name   # follow, but only the last 100 lines first — avoids a wall of scrollback on attach
docker compose exec service_name env               # check what env vars a service actually sees at runtime — confirms it matches what you think you set
docker compose top                                   # processes running inside each service's container — without exec-ing in first
```

## Health check

1. **Container state** — `docker ps -a` — red flag: `Restarting` (loop) or `Exited` with a non-zero code.
2. **Resource usage** — `docker stats --no-stream` — red flag: memory usage sitting right at its limit — OOM-kill is imminent, not hypothetical.
3. **Recent events** — `docker events --since 10m` — red flag: repeated `die` or `oom` events for the same container.
4. **Disk** — `docker system df` — red flag: total usage approaching the host's actual free disk, not just a high "reclaimable" number (that part is normal and expected).

## Troubleshooting

**Container exits immediately after starting:**
```bash
docker logs mycontainer              # shows the actual error — works even on an already-stopped container
docker inspect mycontainer --format '{{.State.ExitCode}}'   # exit code — 137 usually means OOM-killed, 1 is a generic app error
docker run -it --entrypoint sh myimage   # override the entrypoint to get a shell instead — for inspecting an image that doesn't normally give you one
```

**"No space left on device" but df shows free space:**
```bash
docker system df                        # Docker's own disk usage, separate from the host filesystem view — df on the host won't show this breakdown
docker system prune -af --volumes         # Docker images/layers/volumes accumulate in their own storage driver — this is almost always the real cause
```

**Two containers can't reach each other:**
```bash
docker network ls                          # confirm both containers are actually on the same network — the usual reason two containers can't reach each other
docker network inspect <network_name>        # see which containers are attached, and their IPs — confirms network membership directly instead of guessing
docker exec mycontainer1 ping mycontainer2     # containers on the same user-defined network can reach each other by name — if this fails, they're not on the same network
```

---
