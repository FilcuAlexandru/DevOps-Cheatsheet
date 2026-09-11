# Grafana

```bash
curl -H "Authorization: Bearer <api_key>" http://<host>:3000/api/dashboards/uid/<uid>   # export a dashboard's JSON via API
curl -H "Authorization: Bearer <api_key>" -X POST http://<host>:3000/api/dashboards/db \    # import/update a dashboard from JSON
  -H "Content-Type: application/json" -d @dashboard.json
curl -H "Authorization: Bearer <api_key>" http://<host>:3000/api/datasources                # list configured data sources
curl -H "Authorization: Bearer <api_key>" http://<host>:3000/api/alertmanager/grafana/api/v2/alerts   # current alert state via API
curl -H "Authorization: Bearer <api_key>" http://<host>:3000/api/dashboards/uid/<uid>/versions   # every saved version of a dashboard, with who changed it
curl -H "Authorization: Bearer <api_key>" http://<host>:3000/api/org/users   # every user in the current organization and their role
curl -H "Authorization: Bearer <api_key>" http://<host>:3000/api/folders   # every dashboard folder — useful before scripting a bulk import into the right place
curl -H "Authorization: Bearer <api_key>" -X POST http://<host>:3000/api/annotations -d '{"text":"deploy v2.3","tags":["deploy"]}' -H "Content-Type: application/json"   # push an annotation marker onto graphs, e.g. from a CI/CD pipeline after a deploy
```

**Enhanced:**
```bash
curl -H "Authorization: Bearer <api_key>" http://<host>:3000/api/health   # quick liveness check — separate from whether dashboards actually render correctly
curl -H "Authorization: Bearer <api_key>" http://<host>:3000/api/search?query=<dashboard_name>   # find a dashboard's UID by name, first step before any API call that needs it
```
Dashboards-as-code beats manual export/import once you have more than a couple: keep the JSON in git and provision via the `provisioning/dashboards` config, so a dashboard's history lives in version control, not only in Grafana's own database.

## Health check

1. **Grafana itself** — `/api/health` — red flag: anything other than `"database": "ok"`.
2. **Each data source** — `/api/datasources/<id>/health` — red flag: a specific data source failing while others succeed — narrows the problem to that connection, not Grafana as a whole.

## Troubleshooting

**Dashboard shows "No data" but the data source works elsewhere:**
```bash
curl -H "Authorization: Bearer <api_key>" http://<host>:3000/api/datasources/proxy/<datasource_id>/api/v1/query?query=up   # query the data source through Grafana's own proxy — isolates whether the problem is Grafana's connection or the panel's query
```
Check the panel's actual time range next — "No data" is very often just a time window with nothing in it, not a broken connection.

**Data source shows unreachable:**
```bash
curl -H "Authorization: Bearer <api_key>" -X POST http://<host>:3000/api/datasources/<id>/health   # Grafana's own connectivity test for that data source, without touching a dashboard
```

---
