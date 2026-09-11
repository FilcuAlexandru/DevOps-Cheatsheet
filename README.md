# DevOps Cheatsheet

Personal command reference, organized by platform. Source of truth is the markdown in each folder; the styled HTML site is generated from it automatically.

**Live site:** enable GitHub Pages once (Settings → Pages → Source: "GitHub Actions"), then every push to `main` rebuilds and redeploys automatically via `.github/workflows/deploy.yml`.

## Structure

Grouped by domain on the landing page:

- **OS & Shell** — [linux/](./linux/) (with [bash/](./linux/bash/), [networking/](./linux/networking/), [logs-systemd/](./linux/logs-systemd/), [performance/](./linux/performance/))
- **Containers & Orchestration** — [docker/](./docker/), [kubernetes/](./kubernetes/) (with [helm/](./kubernetes/helm/), [openshift/](./kubernetes/openshift/), [argocd/](./kubernetes/argocd/))
- **Automation & Secrets** — [ansible/](./ansible/), [vault/](./vault/)
- **Databases** — [oracle-db/](./oracle-db/), [postgresql/](./postgresql/)
- **Application Servers** — [weblogic/](./weblogic/)
- **Monitoring** — [prometheus/](./prometheus/), [grafana/](./grafana/), [checkmk/](./checkmk/)
- **Languages** — [python/](./python/), [powershell/](./powershell/)
- **Version Control** — [git/](./git/)
- **Data Formats** — [data-formats/](./data-formats/) (YAML / JSON / JQ)
- **Reference** — [troubleshooting/](./troubleshooting/), [production-safety/](./production-safety/), [quick-reference/](./quick-reference/)

## Features

- **Search** — press `/` anywhere or click the search button, type to filter across every command on the site, click a result to jump straight to it.
- **Hover tooltips** — hover (or tab-focus) any command to see what it does, without cluttering the page with permanent inline text.

## Editing content

Edit the `.md` files, not the `index.html` files — those are regenerated. Locally:

```bash
pip install -r scripts/requirements.txt
python scripts/build.py
```

Commit and push; the GitHub Action rebuilds and redeploys automatically.

## Conventions

- Each folder's `README.md` is either the content itself (single-topic folders) or an index into that folder's `.md` files (multi-file topics like `linux/`, `linux/bash/`, `linux/networking/`).
- Command lines with a trailing `  # comment` (two spaces then `#`) become hover tooltips automatically — write the comment as a short, natural explanation.
- `**Enhanced:**` paragraphs (optionally followed by a code block) render as a highlighted callout.
