# Module 19 — Ansible Practice

## Goals

- Write idempotent Ansible playbooks for server bootstrapping
- Deploy a Docker Compose stack via Ansible
- Implement a rollback pattern for container deployments
- Understand inventory, variables, templates, and handlers

## Prerequisites

- Python 3.11+ with `uv` or pip
- Ansible installed (`pip install ansible` or `uv pip install ansible`)
- SSH access to a target host (or use `connection: local` for local practice)
- Docker installed on the target host

## Setup

```bash
cd practice/curriculum/19-ansible-practice

# Install Ansible
pip install ansible

# Verify
ansible --version

# Test local connection
ansible -i inventory.ini local -m ping
```

---

## Exercise 19.1 — Bootstrap a VM

### Objective

Create an idempotent playbook that prepares a server with Docker and required directories.

### Steps

1. Review the playbook:

```bash
cat ansible/bootstrap.yml
```

2. Run against local machine:

```bash
ansible-playbook -i inventory.ini ansible/bootstrap.yml --check --diff
```

The `--check` flag shows what **would** change without making changes.

3. Run for real:

```bash
ansible-playbook -i inventory.ini ansible/bootstrap.yml
```

4. Run again to verify idempotency:

```bash
ansible-playbook -i inventory.ini ansible/bootstrap.yml
```

Expected: all tasks show `ok` (green), none show `changed` (yellow).

### What the playbook does

- Installs Docker (via package manager)
- Installs Docker Compose plugin
- Creates application directories (`/opt/app`, `/opt/app/data`, `/opt/app/logs`)
- Creates a deploy user with Docker group membership
- Enables and starts Docker service

### Key Concept: Idempotency

Every task should be safe to run multiple times without side effects:

| Ansible Module | Idempotent? | Example |
|---------------|------------|---------|
| `apt` / `yum` | Yes | `apt: name=docker.io state=present` |
| `file` | Yes | `file: path=/opt/app state=directory` |
| `user` | Yes | `user: name=deploy groups=docker` |
| `command` | **No** | `command: mkdir /opt/app` — use `file` instead |
| `shell` | **No** | Avoid unless necessary; use `creates:` guard |

### Deliverables

- [ansible/bootstrap.yml](ansible/bootstrap.yml) — server bootstrap playbook

---

## Exercise 19.2 — Deploy a Container Stack

### Objective

Deploy a Docker Compose application stack via Ansible, including environment configuration from a Jinja2 template.

### Steps

1. Review the playbook and template:

```bash
cat ansible/deploy.yml
cat templates/env.j2
```

2. Run the deployment:

```bash
ansible-playbook -i inventory.ini ansible/deploy.yml -e "app_version=1.0.0"
```

3. Verify the deployment:

```bash
docker compose -f /opt/app/docker-compose.yml ps
curl -s http://localhost:8080/health
```

### What the playbook does

- Copies `docker-compose.yml` to the target host
- Renders `.env` file from Jinja2 template with variables
- Pulls latest images
- Runs `docker compose up -d`
- Waits for health check to pass

### Variables

Variables are defined in:
- `inventory.ini` (host-specific)
- `-e` flag (command-line overrides)
- `ansible/deploy.yml` `vars:` section (defaults)

### Deliverables

- [ansible/deploy.yml](ansible/deploy.yml) — deployment playbook
- [templates/env.j2](templates/env.j2) — environment template
- [templates/docker-compose.yml](templates/docker-compose.yml) — compose template

---

## Exercise 19.3 — Rollback Pattern

### Objective

Demonstrate rolling back to a previous version by changing the image tag.

### Steps

1. Deploy version 1.0.0:

```bash
ansible-playbook -i inventory.ini ansible/deploy.yml -e "app_version=1.0.0"
```

2. Deploy version 2.0.0 (simulated bad release):

```bash
ansible-playbook -i inventory.ini ansible/deploy.yml -e "app_version=2.0.0"
```

3. Rollback to 1.0.0:

```bash
ansible-playbook -i inventory.ini ansible/rollback.yml -e "app_version=1.0.0"
```

4. Verify:

```bash
docker compose -f /opt/app/docker-compose.yml ps
```

### What the rollback playbook does

- Stops current containers
- Updates `.env` with the previous version tag
- Pulls the specified version
- Starts containers with the old version
- Verifies health check passes

### Rollback Strategies

| Strategy | Pros | Cons |
|----------|------|------|
| **Tag-based** (this exercise) | Simple, fast | Requires image registry |
| **Blue-green** | Zero downtime, instant switch | Needs 2x resources |
| **Canary** | Gradual rollout, early detection | Complex routing |
| **Git revert + redeploy** | Full audit trail | Slower |

### Deliverables

- [ansible/rollback.yml](ansible/rollback.yml) — rollback playbook

---

## Project Structure

```
19-ansible-practice/
├── README.md
├── inventory.ini
├── ansible/
│   ├── bootstrap.yml
│   ├── deploy.yml
│   └── rollback.yml
└── templates/
    ├── env.j2
    └── docker-compose.yml
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ansible: command not found` | `pip install ansible` |
| SSH connection refused | Check `ansible_connection: local` in inventory for local practice |
| Permission denied | Run with `--become` flag or use `become: true` in playbook |
| Docker not found | Run bootstrap.yml first |
| `changed` on every run | Replace `command`/`shell` with idempotent modules |

## Next Steps

- Module 20: CI/CD Practice (automate these playbooks in a pipeline)
