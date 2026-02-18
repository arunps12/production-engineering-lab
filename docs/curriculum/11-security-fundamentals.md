# SECTION 11 — SECURITY FUNDAMENTALS FOR DEVOPS

---

## PART A — CONCEPT EXPLANATION

### Why Security is Every Engineer's Responsibility

Security isn't just the "security team's job." As a DevOps engineer, you:
- **Deploy code** — You control what runs in production
- **Manage secrets** — API keys, database passwords, certificates
- **Configure infrastructure** — Firewalls, networks, access control
- **Build CI/CD pipelines** — A compromised pipeline compromises everything

### The Security Mindset

Think in terms of **attack surface** — every exposed port, endpoint, dependency, and credential is a potential entry point.

**Principle of Least Privilege**: Give the minimum access needed, nothing more.
```
# BAD: Run as root
USER root

# GOOD: Run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### Authentication vs Authorization

**Authentication (AuthN)**: "Who are you?" → Verify identity
**Authorization (AuthZ)**: "What can you do?" → Verify permissions

```
Request → [Authentication] → [Authorization] → Resource
          "Is this user       "Can this user
           who they           access this
           claim to be?"      resource?"
```

### JWT (JSON Web Tokens)

JWTs are the most common API authentication method:

```
Header.Payload.Signature

Header:  {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "user123", "role": "admin", "exp": 1700000000}
Signature: HMAC-SHA256(header + payload, secret)
```

**Key properties:**
- Self-contained (no server-side session storage needed)
- Signed (tamper-proof, but NOT encrypted — payload is just base64)
- Expirable (use short lifetimes: 15-60 minutes)

### HTTPS and TLS

**TLS (Transport Layer Security)** encrypts communication between client and server:

```
Client                                 Server
  |──── ClientHello (supported ciphers) ──→|
  |←── ServerHello + Certificate ──────────|
  |──── Key Exchange ─────────────────────→|
  |←── Encrypted Connection ──────────────→|
```

**In production:**
- Always use HTTPS (never HTTP)
- TLS termination typically at the load balancer or reverse proxy
- Use Let's Encrypt for free certificates
- Redirect HTTP → HTTPS

### Secrets Management

**NEVER do this:**
```python
# BAD — Secrets in code
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://admin:password123@db:5432/prod"
```

**DO this:**
```python
# GOOD — Secrets from environment
import os
API_KEY = os.environ["API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
```

**Secret storage hierarchy** (least to most secure):
1. Environment variables (minimum acceptable)
2. `.env` files (dev only, never commit)
3. Docker secrets / Kubernetes secrets
4. Vault (HashiCorp Vault, AWS Secrets Manager)

### OWASP Top 10 (Simplified)

The most critical web application security risks:

1. **Injection** — SQL injection, command injection
2. **Broken Authentication** — Weak passwords, exposed tokens
3. **Sensitive Data Exposure** — Unencrypted PII, secrets in logs
4. **XML External Entities (XXE)** — Rarely relevant with JSON APIs
5. **Broken Access Control** — Users accessing other users' data
6. **Security Misconfiguration** — Default passwords, debug mode in production
7. **Cross-Site Scripting (XSS)** — Injecting scripts (less relevant for APIs)
8. **Insecure Deserialization** — Trusting serialized data from clients
9. **Using Components with Known Vulnerabilities** — Outdated dependencies
10. **Insufficient Logging and Monitoring** — Not detecting attacks

### Common Beginner Misunderstandings

1. **"HTTPS is enough"** — HTTPS protects transport, not application logic. You still need auth, input validation, etc.
2. **"Environment variables are secure"** — They're better than hardcoding, but they're visible in process lists, logs, and Docker inspect. Use proper secret management in production.
3. **"JWT is encrypted"** — JWT payload is base64-encoded, not encrypted. Anyone can read it. The signature only prevents tampering.
4. **"I'll add security later"** — Security is exponentially harder to retrofit. Build it in from the start.
5. **"We're too small to be attacked"** — Automated scanners attack everything. Bots don't check company size.

---

## PART B — BEGINNER PRACTICE

### Exercise 11.B.1 — Environment Variables for Secrets

Create an application that reads all configuration from environment variables:
```python
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    API_KEY = os.environ.get("API_KEY")
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
    
    @classmethod
    def validate(cls):
        if cls.SECRET_KEY == "change-me-in-production":
            raise ValueError("SECRET_KEY not configured!")
        if not cls.API_KEY:
            raise ValueError("API_KEY is required!")
```

### Exercise 11.B.2 — .env Files with python-dotenv

```bash
# Create .env file (NEVER commit this!)
echo 'SECRET_KEY=my-super-secret-key-12345' > .env
echo 'DATABASE_URL=postgresql://user:pass@localhost/db' >> .env
echo 'API_KEY=sk-test-key' >> .env
echo '.env' >> .gitignore
```

```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env into os.environ
```

### Exercise 11.B.3 — Input Validation

```python
from pydantic import BaseModel, Field, validator
import re

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=8)
    
    @validator("email")
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v
    
    @validator("username")
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("Username must be alphanumeric")
        return v
```

### Exercise 11.B.4 — SQL Injection Prevention

```python
# BAD — SQL Injection vulnerability
username = input("Username: ")
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
# Input: ' OR 1=1 -- → Returns ALL users!

# GOOD — Parameterized query
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

### Exercise 11.B.5 — Password Hashing

```python
# pip install bcrypt
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

Never store plaintext passwords. Never use MD5 or SHA for passwords (use bcrypt, argon2, or scrypt).

### Exercise 11.B.6 — HTTPS with FastAPI (Development)

```python
# Generate self-signed cert for development:
# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Run with HTTPS:
# uvicorn app:app --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### Exercise 11.B.7 — Dependency Vulnerability Scanning

```bash
# Check for known vulnerabilities in your dependencies
pip install pip-audit
pip-audit

# Or with uv:
uv pip audit

# GitHub: Enable Dependabot in your repository settings
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 11.C.1 — JWT Authentication in FastAPI

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Exercise 11.C.2 — Role-Based Access Control (RBAC)

```python
from functools import wraps

def require_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, token=Depends(verify_token), **kwargs):
            if token["role"] not in allowed_roles:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, token=token, **kwargs)
        return wrapper
    return decorator

@app.get("/admin/users")
@require_role("admin")
async def list_users(token: dict = Depends(verify_token)):
    return {"users": [...]}
```

### Exercise 11.C.3 — Rate Limiting for API Protection

Implement rate limiting middleware:
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        # Remove old requests
        self.requests[client_id] = [
            t for t in self.requests[client_id] if now - t < self.window
        ]
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        self.requests[client_id].append(now)
        return True
```

### Exercise 11.C.4 — Secrets in Docker

```yaml
# docker-compose.yml
services:
  app:
    build: .
    secrets:
      - db_password
      - api_key
    environment:
      DATABASE_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

### Exercise 11.C.5 — Security Headers

Add security headers to your FastAPI app:
```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

### Exercise 11.C.6 — Audit Logging

Log all security-relevant events:
```python
import logging

audit_logger = logging.getLogger("audit")

def log_auth_event(event_type: str, user_id: str, ip: str, success: bool):
    audit_logger.info(
        "auth_event",
        extra={
            "event_type": event_type,  # "login", "logout", "token_refresh"
            "user_id": user_id,
            "ip_address": ip,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 11.D.1 — Debug: Secrets Leaked in Docker Image

Symptom: `docker history` shows your secret in a RUN layer.
```dockerfile
# BAD
RUN echo "SECRET=abc123" > /app/.env
# Even if you delete it later, it's in the layer history!
```
Task: Use multi-stage builds or Docker secrets to avoid this.

### Exercise 11.D.2 — Debug: JWT Token Never Expires

Symptom: Tokens issued months ago still work.
Task: Check that `exp` claim is set and validated.

### Exercise 11.D.3 — Debug: SQL Injection in Production

Symptom: Database contains unexpected `'; DROP TABLE users; --` entries.
Task: Find the unparameterized query, fix it, audit all queries.

### Exercise 11.D.4 — Debug: CORS Allows Everything

Symptom: `Access-Control-Allow-Origin: *` in production.
```python
# BAD
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# GOOD
app.add_middleware(CORSMiddleware, allow_origins=["https://yourdomain.com"])
```

### Exercise 11.D.5 — Debug: Sensitive Data in Logs

Symptom: Passwords, tokens, and PII appear in application logs.
Task: Implement a log sanitizer that redacts sensitive fields.

---

## PART E — PRODUCTION SIMULATION

### Scenario: Secure a Production API

You've inherited an insecure API. Harden it:

1. **Remove hardcoded secrets** → Move to environment variables
2. **Add authentication** → JWT with expiry
3. **Add authorization** → Role-based access (admin, user, readonly)
4. **Add input validation** → Pydantic models for all endpoints
5. **Add rate limiting** → 100 req/min per IP
6. **Add security headers** → All standard headers
7. **Add audit logging** → Log all auth events
8. **Scan dependencies** → Run pip-audit, fix vulnerabilities
9. **Docker security** → Non-root user, multi-stage build, no secrets in layers
10. **Test** → Write tests for auth, RBAC, rate limiting, injection prevention

---

## Key Takeaways

1. **Never hardcode secrets** — Use environment variables at minimum, secret managers in production.
2. **Always validate input** — Never trust user input. Parameterize queries. Validate with Pydantic.
3. **Authentication and authorization are different** — Implement both.
4. **JWT tokens must expire** — Use short lifetimes (15-60 min) with refresh tokens.
5. **Security is continuous** — Scan dependencies regularly, audit logs, update packages.
6. **Principle of least privilege** — Minimum permissions everywhere (users, containers, CI, databases).

---
*Next: [Section 12 — Cloud & Infrastructure Basics](12-cloud-infrastructure-basics.md)*
