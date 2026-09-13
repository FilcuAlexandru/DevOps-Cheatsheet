Da. Îți livrez **tot README-ul într-un singur chenar de text**, într-un singur bloc Markdown, fără alte chenare sau blocuri separate.

````
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

DevOps Cheatsheet is a practical command reference for infrastructure, automation, application operations, monitoring, observability and troubleshooting.

It brings together commonly used commands, operational patterns and diagnostic techniques across the DevOps toolchain, with an emphasis on clarity, speed and real-world operational use.

The reference is designed to answer three questions quickly:

> What do I run?  
> What does it do?  
> When should I use it?

The Markdown files are the single source of truth. The interactive web dashboard is generated automatically from the same content.

---

## Live Dashboard

<p align="center">
  <a href="https://filcualexandru.github.io/devops-cheatsheet/">
    <img src="https://img.shields.io/badge/OPEN%20DEVOPS%20DASHBOARD-18181B?style=for-the-badge" alt="Open DevOps Dashboard">
  </a>
</p>

The interactive dashboard provides a focused interface for quickly finding and using commands without navigating through raw Markdown files.

### Dashboard Features

- Full-text search across the complete reference
- `/` keyboard shortcut for instant search
- Direct navigation to matching commands
- Hover and keyboard-accessible command tooltips
- Technology and domain-based navigation
- Responsive interface
- Automatically generated from the source Markdown

---

## Technology Coverage

| Domain | Coverage |
|---|---|
| **OS & Shell** | Linux, Bash, Networking, Logs, systemd, Performance |
| **Containers & Orchestration** | Docker, Kubernetes, Helm, OpenShift, Argo CD |
| **Automation & Secrets** | Ansible, Vault |
| **Databases** | Oracle Database, PostgreSQL |
| **Application Servers** | WebLogic |
| **Monitoring & Observability** | Prometheus, Grafana, Checkmk |
| **Languages** | Python, PowerShell |
| **Version Control** | Git |
| **Data & Configuration** | YAML, JSON, JQ |
| **Operations** | Troubleshooting, Production Safety, Quick Reference |

---

## Operational Focus

The reference is built around common infrastructure and operations workflows rather than isolated command memorization.

Typical use cases include:

- System administration
- Application troubleshooting
- Service and process investigation
- Network diagnostics
- Container operations
- Kubernetes troubleshooting
- Infrastructure automation
- Database operations
- Application server administration
- Log analysis
- Performance investigation
- Monitoring and observability
- Production incident response

The goal is to provide a reliable starting point when a command, syntax or diagnostic workflow is needed quickly.

---

## Automation & Monitoring

Bash, Python and PowerShell are treated not only as scripting languages, but also as operational automation tools.

Scripts can be used for:

- System and application health checks
- Metric collection
- Log processing
- Service validation
- Infrastructure diagnostics
- Automated remediation
- Operational reporting
- Monitoring integrations

Where appropriate, scripts can be designed to integrate with platforms such as Prometheus, Grafana and Checkmk.

This allows simple command-line utilities to evolve into reusable operational tooling.

---

## Script Standards

Operational scripts should follow consistent conventions so they remain readable, maintainable and suitable for production environments.

### Bash

Bash scripts should use clear section headers and concise comments:

```bash
###############################################################################################
# cpu-usage-monitor.sh                                                                       #
###############################################################################################
```

Scripts should:

- Use clear variable names
- Validate required parameters
- Handle errors explicitly
- Return meaningful exit codes
- Avoid unnecessary external commands
- Support logging where appropriate
- Be safe to run repeatedly when possible
- Provide useful output for operators
- Be designed for automation and monitoring integration where required

### Python

Python scripts should prioritize:

- Clear module structure
- Functions with defined responsibilities
- Argument parsing
- Exception handling
- Logging instead of uncontrolled console output
- Meaningful exit codes
- Configuration through arguments or environment variables
- Reusable components
- Monitoring and metrics integration where appropriate

### PowerShell

PowerShell scripts should prioritize:

- Structured functions
- Parameter validation
- Explicit error handling
- Objects rather than text parsing where possible
- Meaningful exit codes
- Reusable functions
- Logging
- Compatibility with automation environments
- Monitoring integration where appropriate

### Monitoring Integration

When operational scripts collect health or performance information, they should be designed so the collected information can be exposed to monitoring systems when required.

Possible integrations include:

- Prometheus metrics
- Grafana dashboards
- Checkmk local checks
- HTTP health endpoints
- Structured JSON output
- Log-based monitoring
- Exit-code based monitoring

The goal is to make scripts useful both interactively and as components of an automated observability workflow.

---

## Command Conventions

### Inline Command Explanations

Commands can include a concise explanation using two spaces followed by `#`:

```bash
journalctl -u nginx -f  # Follow nginx logs in real time
```

The trailing comment is automatically converted into a tooltip in the generated dashboard.

Explanations should be:

- Concise
- Technically accurate
- Easy to understand
- Focused on the purpose of the command

Avoid using comments to repeat obvious syntax. The goal is to provide useful operational context.

### Enhanced Sections

Important operational information can be highlighted using:

```markdown
**Enhanced:** This section contains additional operational context.

```bash
example command
```
```

Enhanced sections are rendered as highlighted callouts in the dashboard.

---

## Production Awareness

Infrastructure commands can have very different consequences depending on the environment in which they are executed.

The reference therefore distinguishes between general command usage and operational considerations where appropriate.

Before executing potentially disruptive commands in production, consider:

- Scope of impact
- Target environment
- Service dependencies
- Active workloads
- Data integrity
- Rollback options
- Change procedures
- Monitoring and validation

The `production-safety/` and `troubleshooting/` sections provide additional operational guidance.

> Reference first. Validate context. Execute deliberately.

---

## Source of Truth

The Markdown files are the authoritative source for all cheatsheet content.

Generated HTML should not be edited manually.

The build process transforms the Markdown source into the dashboard presentation layer, keeping content and presentation separated.

This provides:

- Version-controlled documentation
- Consistent formatting
- Reproducible builds
- Automated publishing
- A single maintained source

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

Review the generated output before committing changes.

---

## Continuous Deployment

The dashboard is automatically built and deployed through GitHub Actions.

```text
              Markdown Source
                     |
                     v
              Build Pipeline
                     |
                     v
              Generated HTML
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

The publishing workflow is:

**Edit → Build → Validate → Commit → Push → Deploy**

---

## Editing Workflow

The recommended workflow is:

```text
1. Locate the relevant topic
2. Edit the Markdown source
3. Build the dashboard locally
4. Validate the generated output
5. Commit the change
6. Push to main
7. Verify the deployed dashboard
```

Keep individual changes focused and preserve the existing Markdown conventions.

---

## Design Principles

### Practical

Prioritize commands and workflows that are useful in real operational environments.

### Fast

Make frequently needed information discoverable with minimal navigation.

### Clear

Prefer concise explanations and consistent terminology.

### Context-Aware

Document not only syntax, but also operational purpose and relevant considerations.

### Automation-Ready

Prefer approaches that can evolve from manual commands into repeatable automation.

### Observable

Where appropriate, make scripts and operational workflows compatible with monitoring and observability systems.

### Maintainable

Keep the source content structured, version-controlled and independent from the presentation layer.

---

## Quick Reference

For high-frequency operational tasks, start with:

- `quick-reference/`
- `troubleshooting/`
- `production-safety/`

These sections provide a fast path to commonly required commands, diagnostic workflows and operational safeguards.

---

## License

MIT License

---

<p align="center">
  <sub>DevOps Cheatsheet · Practical reference · Automated publishing</sub>
</p>
````