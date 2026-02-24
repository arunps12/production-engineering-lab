# SECTION 17 — ANSIBLE PRACTICE

---

## PART A — CONCEPT EXPLANATION

### What is Ansible?

Ansible is an agentless automation tool for configuration management, application deployment, and orchestration. It connects to servers via SSH and runs tasks defined in YAML playbooks.

```
Control Node (your laptop)
    │
    │ SSH
    ├──→ Server 1 (web)
    ├──→ Server 2 (web)
    └──→ Server 3 (db)
```

**Why Ansible for production engineering?**
- **Reproducible server setup** — Run a playbook to bootstrap any server identically
- **Deployment automation** — Deploy Docker stacks, manage configs, restart services
- **Rollback patterns** — Revert to a previous version safely
- **Idempotent operations** — Run playbooks multiple times without side effects

### Key Concepts

**Inventory** — Defines which servers to manage:

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

**Playbook** — A YAML file defining what to do:

```yaml
- name: Configure web servers
  hosts: webservers
  become: true           # Run as root (sudo)
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: true
```

**Module** — A unit of work (install package, copy file, manage service):

| Module | Purpose | Example |
|--------|---------|---------|
| `apt` / `yum` | Install packages | `apt: name=docker.io state=present` |
| `file` | Manage files/directories | `file: path=/opt/app state=directory` |
| `copy` | Copy files to remote | `copy: src=app.conf dest=/etc/app.conf` |
| `template` | Render Jinja2 template | `template: src=env.j2 dest=/opt/app/.env` |
| `service` | Manage systemd services | `service: name=docker state=started` |
| `user` | Manage users | `user: name=deploy groups=docker` |
| `docker_compose` | Manage compose stacks | `docker_compose: project_src=/opt/app` |
| `command` / `shell` | Run arbitrary commands | `command: docker compose up -d` |
| `uri` | HTTP requests | `uri: url=http://localhost/health` |
| `wait_for` | Wait for condition | `wait_for: port=8080 timeout=30` |

### Idempotency — The #1 Ansible Principle

Every task should be safe to run multiple times:

```yaml
# GOOD — Idempotent (apt checks if already installed)
- name: Install Docker
  apt:
    name: docker.io
    state: present

# BAD — Not idempotent (mkdir fails if dir exists)
- name: Create directory
  command: mkdir /opt/app

# GOOD — Idempotent (file module checks state)
- name: Create directory
  file:
    path: /opt/app
    state: directory
    owner: deploy
    mode: '0755'
```

**Second run test:** Run the playbook twice. The second run should show all tasks as `ok` (green) with zero `changed` (yellow).

### Variables and Templates

Variables can be defined in inventory, playbooks, or passed via command line:

```yaml
# In playbook
vars:
  app_version: "1.0.0"
  db_password: "{{ lookup('env', 'DB_PASSWORD') }}"

# In inventory
[webservers:vars]
app_port=8080

# Command line
ansible-playbook deploy.yml -e "app_version=2.0.0"
```

**Jinja2 templates** render dynamic configuration:

```jinja2
# templates/env.j2
APP_VERSION={{ app_version }}
DATABASE_URL=postgresql://{{ db_user }}:{{ db_password }}@{{ db_host }}:5432/{{ db_name }}
REDIS_URL=redis://{{ redis_host }}:6379
```

### Handlers — Run Once on Change

Handlers run at the end of a play, triggered by tasks that report `changed`:

```yaml
tasks:
  - name: Copy nginx config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx       # Only triggers if config changed

handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

Even if multiple tasks notify the same handler, it runs only once.

### Deployment Patterns

**Blue-Green Deployment:**
```
1. Deploy new version to "green" stack
2. Health check green
3. Switch traffic from "blue" to "green"
4. Keep blue as rollback target
```

**Rolling Deployment:**
```yaml
- name: Deploy app
  hosts: webservers
  serial: 1              # One server at a time
  tasks:
    - name: Pull new image
      command: docker pull myapp:{{ version }}
    - name: Restart container
      command: docker compose up -d
    - name: Wait for health
      uri:
        url: http://localhost:8080/health
        status_code: 200
      retries: 10
      delay: 5
```

**Rollback Pattern:**
```yaml
- name: Rollback
  hosts: webservers
  tasks:
    - name: Stop current
      command: docker compose down
    - name: Update version
      lineinfile:
        path: /opt/app/.env
        regexp: '^APP_VERSION='
        line: 'APP_VERSION={{ previous_version }}'
    - name: Start previous
      command: docker compose up -d
```

### Common Beginner Misunderstandings

1. **"Ansible needs an agent"** — No. Ansible is agentless — it connects via SSH. No software needs to be installed on target servers (except Python).
2. **"command and shell modules are fine"** — They're not idempotent. Prefer declarative modules (`apt`, `file`, `template`). Only use `command`/`shell` with `creates:` or `when:` guards.
3. **"become: true everywhere"** — Only elevate privileges when needed (installing packages, managing services). Don't run everything as root.
4. **"Variables are global"** — Variable precedence matters. Extra vars (`-e`) override everything. Host vars override group vars.
5. **"Just put the password in the playbook"** — Use `ansible-vault` to encrypt secrets, or pass via environment variables.

---

## PART B — BEGINNER PRACTICE

### Exercise 19.B.1 — Bootstrap a Server

Run the bootstrap playbook to prepare a server with Docker and application directories:

```bash
cd practice/curriculum/19-ansible-practice

# Dry run — shows what would change
ansible-playbook -i inventory.ini ansible/bootstrap.yml --check --diff

# Apply changes
ansible-playbook -i inventory.ini ansible/bootstrap.yml

# Verify idempotency — second run should show 0 changed
ansible-playbook -i inventory.ini ansible/bootstrap.yml
```

Study what the playbook does:
- Installs Docker via package manager
- Creates application directories
- Creates a deploy user with Docker group membership
- Enables and starts the Docker service

**Practice file:** `practice/curriculum/19-ansible-practice/ansible/bootstrap.yml`

### Exercise 19.B.2 — Understand Inventory

Review the inventory file and understand host groups:

```bash
cat inventory.ini
ansible -i inventory.ini all --list-hosts
ansible -i inventory.ini local -m ping
```

Modify the inventory to add a new group and test connectivity.

**Practice file:** `practice/curriculum/19-ansible-practice/inventory.ini`

### Exercise 19.B.3 — Ad-Hoc Commands

Run one-off commands without a playbook:

```bash
# Check disk space
ansible -i inventory.ini local -a "df -h"

# Check Docker version
ansible -i inventory.ini local -a "docker --version"

# Check running containers
ansible -i inventory.ini local -a "docker ps"

# Use a module
ansible -i inventory.ini local -m file -a "path=/tmp/ansible-test state=directory"
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 19.C.1 — Deploy a Container Stack

Deploy a Docker Compose stack using Ansible with Jinja2 templates:

```bash
ansible-playbook -i inventory.ini ansible/deploy.yml -e "app_version=1.0.0"
```

Study what the playbook does:
1. Copies `docker-compose.yml` to the target
2. Renders `.env` from `templates/env.j2` with variables
3. Pulls Docker images
4. Runs `docker compose up -d`
5. Waits for the health check to pass

**Practice files:**
- `practice/curriculum/19-ansible-practice/ansible/deploy.yml`
- `practice/curriculum/19-ansible-practice/templates/env.j2`
- `practice/curriculum/19-ansible-practice/templates/docker-compose.yml`

### Exercise 19.C.2 — Rollback Pattern

Practice rolling back to a previous version:

```bash
# Deploy v1
ansible-playbook -i inventory.ini ansible/deploy.yml -e "app_version=1.0.0"

# Deploy v2
ansible-playbook -i inventory.ini ansible/deploy.yml -e "app_version=2.0.0"

# Rollback to v1
ansible-playbook -i inventory.ini ansible/rollback.yml -e "previous_version=1.0.0"
```

Study the rollback playbook:
1. Stops the current stack
2. Updates the version in `.env`
3. Restarts the stack with the old version
4. Verifies health

**Practice file:** `practice/curriculum/19-ansible-practice/ansible/rollback.yml`

### Exercise 19.C.3 — Variables and Precedence

Experiment with variable precedence:

```bash
# Default vars (from playbook)
ansible-playbook -i inventory.ini ansible/deploy.yml

# Override with inventory vars
ansible-playbook -i inventory.ini ansible/deploy.yml

# Override with extra vars (highest priority)
ansible-playbook -i inventory.ini ansible/deploy.yml -e "app_version=3.0.0 app_port=9090"
```

Order of precedence (lowest → highest):
1. Role defaults
2. Inventory group vars
3. Inventory host vars
4. Playbook vars
5. Play vars
6. Task vars
7. Extra vars (`-e`) — **always wins**

---

## PART D — ADVANCED DEBUG LAB

### Exercise 19.D.1 — Debug: Task Fails but Should Succeed

**Symptom:** `apt` module fails with `Permission denied`.

**Task:**
1. Check if `become: true` is set (needed for package installation)
2. Check if the user has sudo permissions
3. Fix: Add `become: true` at the play or task level

### Exercise 19.D.2 — Debug: Idempotency Violation

**Symptom:** Second playbook run shows `changed` tasks that should be `ok`.

**Task:**
1. Identify which tasks report `changed` on the second run
2. Common causes: `command`/`shell` without guards, template jitter (timestamps)
3. Fix: Replace `command: mkdir` with `file: state=directory`, add `creates:` guards

### Exercise 19.D.3 — Debug: Template Rendering Error

**Symptom:** `AnsibleUndefinedVariable: 'db_password' is undefined`.

**Task:**
1. Check where `db_password` should be defined (inventory, vars, extra vars)
2. Add a default: `{{ db_password | default('changeme') }}`
3. Or pass it: `ansible-playbook deploy.yml -e "db_password=secret"`

### Exercise 19.D.4 — Debug: Handler Not Running

**Symptom:** Config file changed but service not restarted.

**Task:**
1. Check the `notify` name matches the `handlers` name exactly (case-sensitive)
2. Verify the task actually reports `changed` (if template content is the same, no notification)
3. Force a handler: `ansible-playbook ... --force-handlers`

---

## PART E — PRODUCTION SIMULATION

### Scenario: Production Deployment Pipeline

Build a complete Ansible-based deployment pipeline:

1. **Bootstrap** — Install Docker, create directories, create deploy user
2. **Deploy** — Copy compose file, render environment, pull images, start stack
3. **Verify** — Health check passes within 30 seconds
4. **Rollback** — Revert to previous version if health check fails
5. **Idempotency test** — Run entire pipeline twice, second run shows zero changes

```bash
# Full deploy cycle
ansible-playbook -i inventory.ini ansible/bootstrap.yml
ansible-playbook -i inventory.ini ansible/deploy.yml -e "app_version=1.0.0"

# Verify
curl -s http://localhost:8080/health

# Upgrade
ansible-playbook -i inventory.ini ansible/deploy.yml -e "app_version=2.0.0"

# Rollback if needed
ansible-playbook -i inventory.ini ansible/rollback.yml -e "previous_version=1.0.0"
```

Advanced extensions:
6. **Secrets management** — Use `ansible-vault` to encrypt sensitive variables
7. **Rolling deployment** — Deploy to servers one at a time with `serial: 1`
8. **Monitoring integration** — Notify monitoring system before/after deploy

---

## Key Takeaways

1. **Idempotency is non-negotiable** — Every task must be safe to run multiple times. The second run should change nothing.
2. **Use declarative modules** — `apt`, `file`, `template`, `service` over `command`/`shell`.
3. **Templates for configuration** — Jinja2 templates render environment-specific configs from variables.
4. **Handlers run on change** — Use `notify` to restart services only when config actually changes.
5. **Variables have precedence** — Extra vars (`-e`) override everything. Know the precedence order.
6. **Always verify deployments** — Include health checks as part of your deployment playbook.

---
*Next: [Section 18 — Elasticsearch Practice](18-elasticsearch-practice.md)*
