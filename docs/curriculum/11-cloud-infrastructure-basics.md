# SECTION 11 — CLOUD & INFRASTRUCTURE BASICS

---

## PART A — CONCEPT EXPLANATION

### Why Cloud Knowledge is Essential

Modern applications run in the cloud. Understanding cloud fundamentals helps you:
- **Deploy anywhere** — AWS, GCP, Azure, or on-premise
- **Scale on demand** — Handle traffic spikes without over-provisioning
- **Automate infrastructure** — Infrastructure as Code (IaC) eliminates manual setup
- **Reduce costs** — Right-size resources, use spot instances, auto-scale

### Cloud Service Models

```
┌─────────────────────────────────────────────────────┐
│ SaaS (Software as a Service)                        │
│ Gmail, Slack, GitHub — You use the application      │
├─────────────────────────────────────────────────────┤
│ PaaS (Platform as a Service)                        │
│ Heroku, Cloud Run, App Engine — You deploy code     │
├─────────────────────────────────────────────────────┤
│ IaaS (Infrastructure as a Service)                  │
│ EC2, GCE, VMs — You manage servers                  │
├─────────────────────────────────────────────────────┤
│ Physical Hardware (On-Premise)                      │
│ You manage everything                               │
└─────────────────────────────────────────────────────┘
```

**As you go down**: More control, more responsibility.

### Core Cloud Services (AWS terminology, similar across providers)

**Compute:**
- **EC2 / GCE** — Virtual machines
- **Lambda / Cloud Functions** — Serverless (pay per invocation)
- **ECS / Cloud Run** — Container orchestration

**Storage:**
- **S3 / GCS** — Object storage (files, images, backups)
- **EBS / Persistent Disk** — Block storage (attached to VMs)

**Database:**
- **RDS / Cloud SQL** — Managed PostgreSQL/MySQL
- **ElastiCache / Memorystore** — Managed Redis

**Networking:**
- **VPC** — Virtual Private Cloud (isolated network)
- **Load Balancer** — Distribute traffic across instances
- **Route 53 / Cloud DNS** — DNS management
- **CloudFront / CDN** — Content delivery network

### Infrastructure as Code (IaC)

Manual infrastructure = configuration drift, undocumented changes, unreproducible environments.

**IaC principle**: Define infrastructure in version-controlled files, apply changes programmatically.

```
Manual:                        IaC:
Click "Create VM" in console → terraform apply
SSH in, install packages     → ansible-playbook
Modify firewall rules        → git commit + terraform apply
```

### Terraform Basics

Terraform is the most widely used IaC tool. It uses **HCL** (HashiCorp Configuration Language):

```hcl
# Define a provider
provider "aws" {
  region = "us-east-1"
}

# Define a resource
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  
  tags = {
    Name = "production-web"
  }
}
```

**Terraform workflow:**
```bash
terraform init      # Download providers
terraform plan      # Preview changes
terraform apply     # Apply changes
terraform destroy   # Tear down everything
```

**State**: Terraform maintains a `terraform.tfstate` file that maps configuration to real resources. In teams, store state remotely (S3, Terraform Cloud).

### 12-Factor App Methodology

The 12-Factor App is a set of best practices for building cloud-native applications:

1. **Codebase** — One codebase, many deploys
2. **Dependencies** — Explicitly declare and isolate
3. **Config** — Store in environment variables
4. **Backing Services** — Treat as attached resources
5. **Build, Release, Run** — Strictly separate stages
6. **Processes** — Execute as stateless processes
7. **Port Binding** — Export services via port binding
8. **Concurrency** — Scale out via the process model
9. **Disposability** — Fast startup, graceful shutdown
10. **Dev/Prod Parity** — Keep environments similar
11. **Logs** — Treat as event streams
12. **Admin Processes** — Run admin tasks as one-off processes

### Common Beginner Misunderstandings

1. **"Cloud is just someone else's computer"** — It's managed infrastructure with APIs, auto-scaling, global distribution, and managed services.
2. **"Serverless means no servers"** — Servers exist, you just don't manage them. You still need to think about cold starts, timeouts, and limits.
3. **"Terraform is only for big companies"** — Even a single VM benefits from IaC. Start small.
4. **"Cloud is always cheaper"** — Misconfigured cloud can be very expensive. Monitor costs.
5. **"I need to learn all AWS services"** — Focus on compute, storage, database, networking. That's 90% of what you need.

---

## PART B — BEGINNER PRACTICE

### Exercise 11.B.1 — Cloud Mental Model

Draw a diagram of a typical production deployment:
```
Internet → DNS → Load Balancer → [App Server 1] → Database
                                 [App Server 2] → Cache (Redis)
                                 [App Server 3] → Object Storage (S3)
```

Identify which cloud service handles each component.

### Exercise 11.B.2 — SSH into a Remote Server

```bash
# Generate SSH key pair (if you don't have one)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Copy public key to server
ssh-copy-id user@server-ip

# Connect
ssh user@server-ip

# Run commands remotely
ssh user@server-ip "uname -a && df -h && free -m"
```

### Exercise 11.B.3 — SCP and File Transfer

```bash
# Copy file to remote server
scp local-file.txt user@server:/remote/path/

# Copy from remote to local
scp user@server:/remote/file.txt ./local-file.txt

# Copy directory recursively
scp -r ./my-project user@server:/home/user/
```

### Exercise 11.B.4 — First Terraform Configuration

Install Terraform and create a local resource (no cloud account needed):
```hcl
# main.tf — Creates a local file
terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
    }
  }
}

resource "local_file" "hello" {
  content  = "Hello from Terraform!"
  filename = "${path.module}/hello.txt"
}

output "file_path" {
  value = local_file.hello.filename
}
```

```bash
terraform init
terraform plan
terraform apply
cat hello.txt
terraform destroy
```

### Exercise 11.B.5 — Terraform Variables and Outputs

```hcl
# variables.tf
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "development"
}

variable "app_name" {
  description = "Application name"
  type        = string
}

# main.tf
resource "local_file" "config" {
  content  = "environment=${var.environment}\napp=${var.app_name}"
  filename = "${path.module}/${var.environment}.env"
}

output "config_path" {
  value = local_file.config.filename
}
```

```bash
terraform apply -var="app_name=my-service"
```

### Exercise 11.B.6 — Object Storage Concepts

Understand S3/GCS patterns:
```
Bucket: my-company-backups
├── production/
│   ├── db-backup-2025-01-01.sql.gz
│   ├── db-backup-2025-01-02.sql.gz
│   └── db-backup-2025-01-03.sql.gz
├── logs/
│   ├── access-2025-01.log.gz
│   └── error-2025-01.log.gz
└── artifacts/
    ├── app-v1.0.0.tar.gz
    └── app-v1.1.0.tar.gz
```

Practice with MinIO (S3-compatible, runs locally):
```bash
docker run -d -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=password \
  minio/minio server /data --console-address ":9001"
```

### Exercise 11.B.7 — Environment Parity with Docker

Create identical dev/staging/prod environments using Docker Compose + env files:
```bash
# .env.development
DATABASE_URL=sqlite:///dev.db
LOG_LEVEL=debug
DEBUG=true

# .env.production
DATABASE_URL=postgresql://user:pass@db:5432/prod
LOG_LEVEL=info
DEBUG=false

# Run with specific environment
docker compose --env-file .env.development up
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 11.C.1 — Terraform Modules

Create a reusable module:
```
modules/
└── app-config/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf

environments/
├── dev/
│   └── main.tf      ← Uses module with dev settings
├── staging/
│   └── main.tf      ← Uses module with staging settings
└── prod/
    └── main.tf      ← Uses module with prod settings
```

### Exercise 11.C.2 — Terraform State Management

```hcl
# Remote state backend (S3-compatible)
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}
```

Practice: Initialize with local state, then migrate to a backend.

### Exercise 11.C.3 — Docker Registry

Push images to a container registry:
```bash
# Using Docker Hub (free tier)
docker login
docker tag my-app:latest username/my-app:v1.0.0
docker push username/my-app:v1.0.0

# Using GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker tag my-app:latest ghcr.io/username/my-app:v1.0.0
docker push ghcr.io/username/my-app:v1.0.0
```

### Exercise 11.C.4 — Health Checks and Readiness

Implement Kubernetes-style health checks:
```python
@app.get("/health/live")   # Am I running? (liveness)
async def liveness():
    return {"status": "alive"}

@app.get("/health/ready")  # Am I ready to serve traffic? (readiness)
async def readiness():
    # Check database, cache, dependencies
    db_ok = await check_database()
    cache_ok = await check_cache()
    if db_ok and cache_ok:
        return {"status": "ready"}
    raise HTTPException(status_code=503, detail="Not ready")
```

### Exercise 11.C.5 — Load Testing

Use `hey` or `wrk` to load test your service:
```bash
# Install hey
go install github.com/rakyll/hey@latest

# 1000 requests, 50 concurrent
hey -n 1000 -c 50 http://localhost:8000/health

# Or with Python (locust):
# pip install locust
```

### Exercise 11.C.6 — Blue-Green Deployment Concept

Simulate a blue-green deployment with Docker:
```bash
# Blue (current version) running on port 8000
docker run -d --name blue -p 8000:8000 myapp:v1

# Green (new version) running on port 8001
docker run -d --name green -p 8001:8000 myapp:v2

# Test green
curl http://localhost:8001/health

# Switch traffic (update nginx/LB to point to green)
# Stop blue
docker stop blue
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 11.D.1 — Debug: Terraform State Drift

Symptom: `terraform plan` shows changes even though you didn't change config.
Cause: Someone manually modified the resource outside Terraform.
Task: Use `terraform refresh` or `terraform import` to reconcile.

### Exercise 11.D.2 — Debug: SSH Connection Refused

Symptom: `ssh: connect to host x.x.x.x port 22: Connection refused`
Task: Diagnose — Is sshd running? Is the firewall blocking port 22? Is the IP correct? Check security groups.

### Exercise 11.D.3 — Debug: Container Registry Auth Failure

Symptom: `docker push` fails with "unauthorized"
Task: Check login credentials, token expiry, repository permissions.

### Exercise 11.D.4 — Debug: High Cloud Bill

Symptom: Monthly bill jumped from $50 to $500.
Task: Audit resources — unused VMs, oversized instances, forgotten load balancers, excessive data transfer.

### Exercise 11.D.5 — Debug: Terraform Destroy Stuck

Symptom: `terraform destroy` hangs on a resource.
Task: Check for dependencies, manual resource locks, or resources modified outside Terraform.

---

## PART E — PRODUCTION SIMULATION

### Scenario: Deploy from Laptop to Production

Take your capstone project and create a full deployment pipeline:

1. **Local** → Docker Compose (dev environment)
2. **Registry** → Push image to GitHub Container Registry
3. **IaC** → Terraform config for deployment (use local provider for practice)
4. **CI/CD** → GitHub Actions builds, tests, pushes image, and triggers deploy
5. **Monitoring** → Health checks verify deployment success
6. **Rollback** → If health check fails, switch back to previous version

Deliverables:
- Terraform configuration for all resources
- CI/CD pipeline that builds and pushes Docker image
- Deployment script with health check verification
- Rollback procedure documented and tested

---

## Key Takeaways

1. **Cloud is APIs for infrastructure** — Learn the core services: compute, storage, database, networking.
2. **Infrastructure as Code is non-negotiable** — Never click-ops in production. Version control everything.
3. **Start with Terraform locally** — Practice IaC concepts without a cloud account using local providers.
4. **Environment parity prevents surprises** — Docker + env files keep dev/staging/prod consistent.
5. **Health checks are critical** — Liveness and readiness probes prevent deploying broken services.
6. **Cost awareness is a DevOps skill** — Monitor spending, right-size resources, clean up unused infrastructure.

---
*Next: [Section 12 — Nginx & Reverse Proxy](12-nginx-reverse-proxy.md)*
