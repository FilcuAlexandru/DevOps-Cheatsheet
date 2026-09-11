# Docker

```bash
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'   # readable custom columns
docker logs -f --since 10m mycontainer
docker exec -it mycontainer sh                # get a shell in a running container
docker run --rm -it --entrypoint sh myimage   # inspect an image without running its default command
docker stats --no-stream                       # one-shot resource usage snapshot, all containers
docker system df                                # disk usage breakdown by images/containers/volumes
docker system prune -af --volumes               # reclaim space — destructive, see Production Safety
docker inspect --format '{{.State.Health.Status}}' mycontainer   # pull one field instead of parsing full JSON
```

---

## Docker Compose

```bash
docker compose up -d                         # start everything in the background
docker compose up -d --build                  # rebuild images first, then start
docker compose down                            # stop and remove containers, networks (keeps volumes)
docker compose down -v                          # also remove volumes — destructive, see Production Safety
docker compose ps                                # status of every service in this project
docker compose logs -f service_name               # follow logs for one service only
docker compose exec service_name sh                # shell into a running service
docker compose restart service_name                 # restart one service without touching the rest
docker compose config                                # render the fully resolved config (env vars, overrides applied) — great for debugging "why isn't my variable being picked up"
```

**Enhanced:**
```bash
docker compose up -d --scale worker=3      # run 3 instances of one service, useful for quick local load testing
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d   # explicitly combine multiple compose files instead of relying on auto-discovery
docker compose logs -f --tail=100 service_name   # follow, but only the last 100 lines first — avoids a wall of scrollback on attach
docker compose exec service_name env               # check what env vars a service actually sees at runtime, not what you think you set
docker compose top                                   # processes running inside each service's container, without exec-ing in
```

## Health check

1. **Container state** — `docker ps -a` — red flag: `Restarting` (loop) or `Exited` with a non-zero code.
2. **Resource usage** — `docker stats --no-stream` — red flag: memory usage sitting right at its limit — OOM-kill is imminent, not hypothetical.
3. **Recent events** — `docker events --since 10m` — red flag: repeated `die` or `oom` events for the same container.
4. **Disk** — `docker system df` — red flag: total usage approaching the host's actual free disk, not just a high "reclaimable" number (that part is normal and expected).

## Troubleshooting

**Container exits immediately after starting:**
```bash
docker logs mycontainer              # almost always shows the actual error, even for a container that's already stopped
docker inspect mycontainer --format '{{.State.ExitCode}}'   # exit code — 137 usually means OOM-killed, 1 is a generic app error
docker run -it --entrypoint sh myimage   # override the entrypoint to get a shell instead, poke around manually
```

**"No space left on device" but df shows free space:**
```bash
docker system df                        # Docker's own disk usage, separate from the host filesystem view
docker system prune -af --volumes         # Docker images/layers/volumes accumulate in their own storage driver — this is almost always the real cause
```

**Two containers can't reach each other:**
```bash
docker network ls                          # confirm both containers are actually on the same network
docker network inspect <network_name>        # see which containers are attached, and their IPs
docker exec mycontainer1 ping mycontainer2     # containers on the same user-defined network can reach each other by name — if this fails, they're not on the same network
```

---
