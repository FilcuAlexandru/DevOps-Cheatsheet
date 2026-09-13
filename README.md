# DevOps Cheatsheet

<p align="center">
  <strong>A practical command reference for DevOps tooling.</strong>
</p>

<p align="center">
  <a href="https://filcualexandru.github.io/devops-cheatsheet/">
    <img src="https://img.shields.io/badge/Live%20Dashboard-Open-18181B?style=for-the-badge" alt="Live Dashboard">
  </a>
  <a href="https://github.com/FilcuAlexandru/devops-cheatsheet/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/FilcuAlexandru/devops-cheatsheet/deploy.yml?label=Build&style=for-the-badge" alt="Build">
  </a>
  <img src="https://img.shields.io/github/last-commit/FilcuAlexandru/devops-cheatsheet?style=for-the-badge" alt="Last Commit">
  <img src="https://img.shields.io/github/license/FilcuAlexandru/devops-cheatsheet?style=for-the-badge" alt="License">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Linux-000000?style=flat-square&logo=linux&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white" alt="Bash">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PowerShell-5391FE?style=flat-square&logo=powershell&logoColor=white" alt="PowerShell">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white" alt="Ansible">
  <img src="https://img.shields.io/badge/Oracle-F80000?style=flat-square&logo=oracle&logoColor=white" alt="Oracle">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
</p>

---

## Overview

DevOps Cheatsheet is a practical command reference for DevOps, infrastructure and application operations.

It brings together frequently used commands, configuration examples and operational references across multiple technologies, with a focus on fast lookup and practical day-to-day usage.

The project is designed to provide a quick answer to three questions:

> What do I run?  
> What does it do?  
> When should I use it?

The reference is maintained as Markdown and presented through an automatically generated interactive web dashboard.

---

## Live Dashboard

<p align="center">
  <a href="https://filcualexandru.github.io/devops-cheatsheet/">
    <img src="https://img.shields.io/badge/OPEN%20DEVOPS%20DASHBOARD-18181B?style=for-the-badge" alt="Open DevOps Dashboard">
  </a>
</p>

The interactive dashboard provides a faster way to browse and search the complete reference.

### Features

- Full-text search across the cheatsheet
- `/` keyboard shortcut for quick search
- Direct navigation to matching entries
- Command explanations available through tooltips
- Keyboard-accessible navigation
- Technology and topic-based organization
- Responsive interface
- Automatically generated from the Markdown source

---

## Technology Coverage

| Domain | Technologies |
|---|---|
| **Operating Systems & Shell** | Linux, Bash, Networking, systemd, Logs, Performance |
| **Containers & Orchestration** | Docker, Kubernetes, Helm, OpenShift, Argo CD |
| **Automation & Configuration** | Ansible, Vault |
| **Databases** | Oracle Database, PostgreSQL |
| **Application Servers** | WebLogic |
| **Monitoring & Observability** | Prometheus, Grafana, Checkmk |
| **Languages & Scripting** | Python, PowerShell |
| **Version Control** | Git |
| **Data & Configuration** | YAML, JSON, JQ |
| **Operations** | Troubleshooting, Production Safety, Quick Reference |

---

## What You Can Find

The cheatsheet covers common DevOps and infrastructure tasks such as:

- Linux administration
- Process and service management
- Filesystem and storage investigation
- Networking and connectivity diagnostics
- Log analysis
- systemd operations
- Performance troubleshooting
- Docker administration
- Kubernetes troubleshooting
- Helm operations
- OpenShift operations
- Git workflows
- Ansible automation
- Vault operations
- Oracle Database administration
- PostgreSQL administration
- WebLogic administration
- Prometheus and Grafana operations
- Checkmk monitoring
- Python and PowerShell usage
- YAML, JSON and JQ processing
- Production troubleshooting
- Operational safety

---

## Practical Reference

The project focuses on commands and information that are useful during real operational work.

Instead of providing only command syntax, entries are intended to make the purpose of a command immediately clear.

For example:

```bash
journalctl -u nginx -f  # Follow nginx logs in real time
```

This makes the reference useful both as a learning resource and as a quick operational lookup.

---

## Production Awareness

Commands used in infrastructure environments can have different consequences depending on the target system and environment.

Where relevant, the cheatsheet includes operational considerations for:

- Production environments
- Service restarts
- Data modification
- Process termination
- Storage operations
- Kubernetes workloads
- Database operations
- Configuration changes
- Troubleshooting

The `production-safety/` and `troubleshooting/` sections provide additional guidance for situations where operational impact needs to be considered.

> Reference first. Validate context. Execute deliberately.

---

## Source of Truth

The Markdown content is the source of truth for the project.

The web dashboard is generated from this source and should not be edited manually.

This keeps the project:

- Version controlled
- Consistent
- Reproducible
- Easy to maintain
- Automatically publishable

Content and presentation remain separated so the same reference can be maintained without manually editing generated HTML.

---

## Local Development

Install the required dependencies:

```bash
pip install -r scripts/requirements.txt
```

Build the dashboard locally:

```bash
python scripts/build.py
```

The generated output can then be reviewed before committing changes.

---

## Continuous Deployment

The dashboard is built and published automatically through GitHub Actions.

The deployment flow is:

```text
Markdown Source
      |
      v
Build
      |
      v
Generated Dashboard
      |
      v
GitHub Actions
      |
      v
GitHub Pages
      |
      v
Live Dashboard
```

Changes pushed to `main` trigger the deployment workflow.

### Deployment Flow

**Edit → Build → Validate → Commit → Push → Deploy**

---

## Contributing

Contributions are welcome.

When adding or modifying content:

1. Keep commands technically accurate.
2. Keep explanations concise and useful.
3. Follow the existing Markdown conventions.
4. Place content in the appropriate technology or operational section.
5. Build the dashboard locally when changing source content.
6. Review the generated result before committing.

The goal is to keep the reference practical, consistent and easy to use.

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for the complete license text.

---

<p align="center">
  <sub>DevOps Cheatsheet · Practical reference · Automated publishing</sub>
</p>