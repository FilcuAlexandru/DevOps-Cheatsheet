# Prometheus

```bash
promtool check config prometheus.yml               # validate config before reloading — catches typos before they break scraping
promtool check rules alerts.yml                       # validate alerting rules syntax — catches a broken rule before it's reloaded and silently fails
curl -X POST http://<host>:9090/-/reload               # hot-reload config without restarting the process — picks up scrape/rule changes with zero downtime
curl http://<host>:9090/api/v1/targets | jq '.data.activeTargets[] | select(.health!="up")'   # which targets are currently down — confirms scraping is actually working before trusting any metric from it
curl -g 'http://<host>:9090/api/v1/query?query=up'        # run a PromQL query straight from the CLI — no UI needed for a quick check or scripting
curl -g 'http://<host>:9090/api/v1/query_range?query=up&start=<start>&end=<end>&step=60s'   # same query, but over a time range — needed for graphing, not just checking the current value
curl http://<host>:9090/api/v1/rules   # every alerting/recording rule currently loaded, with state — confirms a rule actually made it in after a reload
curl http://<host>:9090/api/v1/labels    # every label name Prometheus knows about — useful for discovering what you can actually filter/group by
curl -g 'http://<host>:9090/api/v1/label/job/values'   # every distinct value for one label — e.g. every job name being scraped
```

**More PromQL:**
```promql
avg_over_time(node_load1[5m])                             # average of a gauge metric over a window — smooths out noise a single instant value would show
max by (instance) (node_memory_MemAvailable_bytes)          # per-instance max — isolates the worst host instead of an average that hides it
count(up == 1)                                                 # how many targets are currently up, as a single number — a fast health count for a dashboard or alert
topk(5, rate(http_requests_total[5m]))                           # the 5 highest values right now — fastest way to find the noisiest series
```

**PromQL — the queries you'll actually reach for:**
```promql
rate(http_requests_total[5m])                          # per-second request rate over a 5-minute window — the standard way to turn a counter into a usable rate
increase(http_requests_total[1h])                        # total increase over the window — good for counting events, not rates
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))   # p95 latency from a histogram metric — shows the experience of slower requests, not just the average
up == 0                                                    # every target Prometheus currently can't scrape — the up==0 query is the fastest way to spot a scraping failure
sum by (job) (rate(errors_total[5m]))                        # error rate grouped by job — the standard "what's on fire" query
```

**Enhanced:**
```bash
curl -s http://<host>:9090/api/v1/status/tsdb | jq        # TSDB stats — series count, chunk count, memory — useful when Prometheus itself is slow
curl -s http://<host>:9093/api/v2/silences                 # list active Alertmanager silences — confirms nobody muted the exact alert you're chasing
amtool alert query --alertmanager.url=http://<host>:9093     # query current firing alerts from the CLI — no UI needed to check what's actually firing right now
amtool silence add alertname=<alert_name> --alertmanager.url=http://<host>:9093 --duration=2h --comment="planned maintenance"   # create a silence from the CLI — scriptable for maintenance windows
promtool query instant http://<host>:9090 'up'                 # run a query via promtool instead of raw curl+jq — cleaner output, no manual JSON parsing
```

## Health check

1. **Targets** — `/api/v1/targets` — red flag: any target `health != "up"`.
2. **TSDB size/memory** — `/api/v1/status/tsdb` — red flag: series count or memory climbing steadily — usually a cardinality problem (see Enhanced above).
3. **Alertmanager silences** — `/api/v2/silences` — red flag: an active silence you don't recognize — someone may have muted the exact alert you're chasing.

## Troubleshooting

**Target shows as `down`:**
```bash
curl http://<host>:9090/api/v1/targets | jq '.data.activeTargets[] | select(.health!="up") | {job: .labels.job, error: .lastError}'   # the actual scrape error, per target — the real reason a target is down, not just that it is
curl http://<target_host>:<target_port>/metrics   # confirm the target's endpoint is reachable — independent of Prometheus
```

**Prometheus itself is slow or using too much memory:**
```bash
curl -s http://<host>:9090/api/v1/status/tsdb | jq '.data.seriesCountByMetricName[:10]'   # top metrics by series count — cardinality explosions are the usual cause
```
A single label with high cardinality (like a raw user ID or request ID as a label value) can silently create millions of series — this query finds the offender fast.

---
