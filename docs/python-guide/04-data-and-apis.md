# SECTION 4 — DATA & APIs

---

## PART A — CONCEPT EXPLANATION

### Working with Files

Programs rarely live in isolation. They read data from files, process it, and write results. Understanding file I/O is fundamental.

**Mental model:** Think of a file like a book. You `open()` it, read or write content, then `close()` it when you're done. The `with` statement is like a responsible librarian who always puts the book back.

```python
# ALWAYS use 'with' — it ensures the file is closed even if errors occur
with open("data.txt", "r") as f:
    content = f.read()

# Without 'with' (risky):
f = open("data.txt", "r")
content = f.read()
f.close()   # What if an error occurs before this line? File stays open!
```

**File modes:**

| Mode | Meaning | Creates file? | Truncates? |
|------|---------|---------------|------------|
| `"r"` | Read (default) | No | No |
| `"w"` | Write | Yes | **Yes** (deletes content!) |
| `"a"` | Append | Yes | No |
| `"x"` | Exclusive create | Fails if exists | N/A |
| `"r+"` | Read + Write | No | No |

**Common mistake:** Using `"w"` mode on a file you wanted to update — it **erases everything** first.

### What is CSV?

**CSV** (Comma-Separated Values) is the simplest tabular data format. Every row is a line, every column is separated by a comma.

```
name,age,city
Alice,30,New York
Bob,25,London
Charlie,35,Tokyo
```

**Why CSV matters:** It's the universal interchange format. Excel exports it, databases export it, APIs return it. Every programming language can read it.

**Mental model:** A CSV file is a spreadsheet stored as plain text. The first row is usually headers (column names). Each following row is one record.

**Gotchas:**
- Fields with commas must be quoted: `"Smith, John",30,NYC`
- Fields with quotes must escape them: `"She said ""hello""",30,NYC`
- Different regions use `;` instead of `,` (especially in Europe)
- Always use the `csv` module — don't try to split on commas manually

### What is JSON?

**JSON** (JavaScript Object Notation) is the standard format for structured data exchange, especially with APIs.

```json
{
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "Docker"],
    "address": {
        "city": "New York",
        "state": "NY"
    },
    "is_active": true
}
```

**JSON ↔ Python mapping:**

| JSON | Python |
|------|--------|
| `{}` object | `dict` |
| `[]` array | `list` |
| `"string"` | `str` |
| `123` / `3.14` | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

**Why JSON matters:** Almost every web API speaks JSON. REST APIs send and receive JSON. Configuration files use JSON (or its cousins YAML/TOML).

### What is an API?

An **API** (Application Programming Interface) is a way for two programs to communicate. When you call an external web API, you're sending an HTTP request and receiving a response.

```
Your Script                     External API
     │                                │
     │── HTTP GET /users/42 ─────────>│
     │                                │
     │<── 200 OK {"name": "Alice"} ──│
     │                                │
```

**Key concepts:**
- **Endpoint** — the URL you call (e.g., `https://api.example.com/users`)
- **Method** — what you want to do (GET = read, POST = create, PUT = update, DELETE = delete)
- **Request body** — data you send (usually JSON, used with POST/PUT)
- **Response** — data you receive back (usually JSON)
- **Status code** — 200 (OK), 404 (not found), 500 (server error)
- **Headers** — metadata about the request (authentication, content type)

### Handling Edge Cases

**Edge cases** are scenarios that happen at the boundaries: empty input, huge input, unexpected types, network timeouts, malformed data.

**Production code handles edge cases. Tutorial code doesn't.**

```python
# Tutorial code (fragile):
def get_average(numbers):
    return sum(numbers) / len(numbers)

# Production code (robust):
def get_average(numbers):
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)
```

**Common edge cases to always check:**
1. Empty input (empty list, empty string, empty file)
2. `None` / missing values
3. Wrong types (string instead of int)
4. Very large or very small numbers
5. Network timeout / connection refused
6. Malformed data (invalid JSON, corrupted CSV)
7. File doesn't exist or no permission

**Common beginner misunderstandings:**

| Mistake | Reality |
|---------|---------|
| "I can split CSV on commas" | Quoted fields contain commas. Use the `csv` module |
| "JSON and Python dicts are the same" | JSON is a string format. Python dicts are objects. You convert between them |
| "APIs always return 200" | APIs return errors frequently. Always check the status code |
| "Network calls always work" | Networks fail. Timeouts happen. Always use try/except with requests |
| "I'll handle edge cases later" | Later never comes. Handle them as you write the code |

---

## PART B — BEGINNER PRACTICE

### Exercise 4.B.1 — Reading and Writing Text Files

```python
# Writing a file
with open("/tmp/notes.txt", "w") as f:
    f.write("Line 1: Learning Python\n")
    f.write("Line 2: Files are straightforward\n")
    f.write("Line 3: Always use 'with' statements\n")

# Reading the entire file
with open("/tmp/notes.txt") as f:
    content = f.read()
    print("=== Full content ===")
    print(content)

# Reading line by line
with open("/tmp/notes.txt") as f:
    print("=== Line by line ===")
    for i, line in enumerate(f, 1):
        print(f"  {i}: {line.rstrip()}")    # rstrip removes trailing newline

# Reading all lines into a list
with open("/tmp/notes.txt") as f:
    lines = f.readlines()
    print(f"\nTotal lines: {len(lines)}")

# Appending to a file
with open("/tmp/notes.txt", "a") as f:
    f.write("Line 4: Appended later\n")
```

### Exercise 4.B.2 — Working with CSV

```python
import csv

# Writing CSV
students = [
    {"name": "Alice", "age": 22, "grade": "A", "gpa": 3.9},
    {"name": "Bob", "age": 25, "grade": "B", "gpa": 3.2},
    {"name": "Charlie", "age": 21, "grade": "A", "gpa": 3.8},
    {"name": "Diana", "age": 23, "grade": "C", "gpa": 2.5},
]

with open("/tmp/students.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "grade", "gpa"])
    writer.writeheader()
    writer.writerows(students)

print("Written students.csv")

# Reading CSV
with open("/tmp/students.csv") as f:
    reader = csv.DictReader(f)
    
    print(f"\nHeaders: {reader.fieldnames}")
    print(f"\n{'Name':<10} {'Age':>4} {'Grade':>6} {'GPA':>5}")
    print("-" * 28)
    
    loaded_students = []
    for row in reader:
        # NOTE: CSV reader returns ALL values as strings!
        row["age"] = int(row["age"])
        row["gpa"] = float(row["gpa"])
        loaded_students.append(row)
        print(f"{row['name']:<10} {row['age']:>4} {row['grade']:>6} {row['gpa']:>5.1f}")

# Process the data
avg_gpa = sum(s["gpa"] for s in loaded_students) / len(loaded_students)
print(f"\nAverage GPA: {avg_gpa:.2f}")

honor_roll = [s["name"] for s in loaded_students if s["gpa"] >= 3.5]
print(f"Honor roll: {', '.join(honor_roll)}")
```

### Exercise 4.B.3 — Working with JSON

```python
import json

# Python dict → JSON string
data = {
    "project": "production-service",
    "version": "1.0.0",
    "dependencies": {
        "fastapi": ">=0.104",
        "uvicorn": ">=0.24",
    },
    "settings": {
        "debug": False,
        "max_workers": 4,
        "allowed_hosts": ["localhost", "0.0.0.0"],
    },
}

# Serialize to JSON string
json_string = json.dumps(data, indent=2)
print("=== JSON String ===")
print(json_string)

# Write JSON to file
with open("/tmp/config.json", "w") as f:
    json.dump(data, f, indent=2)
print("\nWritten config.json")

# Read JSON from file
with open("/tmp/config.json") as f:
    loaded = json.load(f)

print(f"\nProject: {loaded['project']}")
print(f"FastAPI version: {loaded['dependencies']['fastapi']}")
print(f"Debug mode: {loaded['settings']['debug']}")

# Parse JSON string
api_response = '{"status": "ok", "count": 42, "items": [1, 2, 3]}'
parsed = json.loads(api_response)
print(f"\nParsed API response: {parsed}")
print(f"Count: {parsed['count']}")
```

### Exercise 4.B.4 — Handling Malformed Data

```python
import json
import csv
from io import StringIO

# Bad JSON
bad_json_examples = [
    '{"name": "Alice", "age": 30}',           # Good
    '{"name": "Alice", age: 30}',              # Missing quotes on key
    '{"name": "Alice", "age": 30,}',           # Trailing comma
    'not json at all',                          # Not JSON
    '',                                        # Empty string
]

print("=== JSON Parsing ===")
for i, raw in enumerate(bad_json_examples):
    try:
        data = json.loads(raw)
        print(f"  {i}: ✓ Parsed: {data}")
    except json.JSONDecodeError as e:
        print(f"  {i}: ✗ Invalid JSON: {e.msg} at pos {e.pos}")
    except Exception as e:
        print(f"  {i}: ✗ Error: {e}")


# Bad CSV
bad_csv = """name,age,city
Alice,30,New York
Bob,,London
Charlie,thirty-five,Tokyo
,25,
"""

print("\n=== CSV Parsing ===")
reader = csv.DictReader(StringIO(bad_csv))
for i, row in enumerate(reader):
    errors = []
    
    if not row.get("name"):
        errors.append("missing name")
    
    try:
        age = int(row.get("age", ""))
        if age < 0 or age > 150:
            errors.append(f"age out of range: {age}")
    except ValueError:
        errors.append(f"invalid age: '{row.get('age')}'")
    
    if errors:
        print(f"  Row {i}: ✗ {errors}")
    else:
        print(f"  Row {i}: ✓ {row['name']}, {row['age']}, {row['city']}")
```

### Exercise 4.B.5 — Your First API Call

```python
"""
Call a free public API and process the response.
Using httpbin.org — a service designed for testing HTTP.
"""

import urllib.request
import json

# Make a GET request (no external packages needed)
url = "https://httpbin.org/get?name=Arun&language=Python"

try:
    with urllib.request.urlopen(url, timeout=10) as response:
        status = response.status
        data = json.loads(response.read().decode())
    
    print(f"Status: {status}")
    print(f"URL: {data['url']}")
    print(f"Args: {data['args']}")
    print(f"User-Agent: {data['headers']['User-Agent']}")

except urllib.error.URLError as e:
    print(f"Network error: {e}")
except json.JSONDecodeError:
    print("Response was not valid JSON")
except Exception as e:
    print(f"Unexpected error: {e}")


# POST request
post_data = json.dumps({"message": "Hello from Python!"}).encode()
req = urllib.request.Request(
    "https://httpbin.org/post",
    data=post_data,
    headers={"Content-Type": "application/json"},
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode())
    
    print(f"\nPOST status: {response.status}")
    print(f"Sent data: {result['json']}")
except urllib.error.URLError as e:
    print(f"Network error: {e}")
```

### Exercise 4.B.6 — Using the `requests` Library

```python
"""
The 'requests' library is the standard for HTTP in Python.
Much simpler than urllib.

Install: pip install requests (or uv add requests)
"""

import requests

# GET request
response = requests.get(
    "https://httpbin.org/get",
    params={"language": "Python", "level": "intermediate"},
    timeout=10,
)

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers['content-type']}")

data = response.json()   # Automatically parses JSON
print(f"URL: {data['url']}")
print(f"Args: {data['args']}")


# POST request with JSON
response = requests.post(
    "https://httpbin.org/post",
    json={"name": "Arun", "scores": [95, 87, 92]},
    timeout=10,
)
print(f"\nPOST status: {response.status_code}")
print(f"Sent: {response.json()['json']}")


# Checking for errors
response = requests.get("https://httpbin.org/status/404", timeout=10)
print(f"\n404 status: {response.status_code}")
print(f"OK? {response.ok}")   # False for 4xx and 5xx

# raise_for_status() throws an exception on error codes
try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"HTTP Error: {e}")
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 4.C.1 — CSV Data Analysis Pipeline

```python
"""
Build a complete data pipeline:
Read CSV → Clean → Analyze → Write results
"""

import csv
from collections import defaultdict
from io import StringIO

# Sample sales data
RAW_DATA = """date,product,category,quantity,unit_price,region
2024-01-05,Laptop,Electronics,2,999.99,North
2024-01-05,Mouse,Electronics,10,29.99,North
2024-01-06,Desk,Furniture,3,249.99,South
2024-01-06,Chair,Furniture,5,199.99,South
2024-01-07,Laptop,Electronics,1,999.99,East
2024-01-07,Keyboard,Electronics,8,79.99,East
2024-01-08,Desk,Furniture,2,249.99,North
2024-01-08,Monitor,Electronics,4,399.99,West
2024-01-09,Chair,Furniture,,199.99,South
2024-01-09,Laptop,Electronics,3,999.99,West
2024-01-10,Mouse,Electronics,invalid,29.99,North
"""


def load_and_clean(raw_csv):
    """Load CSV data and clean it. Returns valid records and error count."""
    reader = csv.DictReader(StringIO(raw_csv))
    records = []
    errors = 0
    
    for i, row in enumerate(reader):
        try:
            record = {
                "date": row["date"],
                "product": row["product"],
                "category": row["category"],
                "quantity": int(row["quantity"]),
                "unit_price": float(row["unit_price"]),
                "region": row["region"],
            }
            record["total"] = record["quantity"] * record["unit_price"]
            records.append(record)
        except (ValueError, TypeError) as e:
            print(f"  Skipping row {i + 1}: {e}")
            errors += 1
    
    return records, errors


def analyze(records):
    """Analyze sales records and return summary."""
    # Revenue by category
    by_category = defaultdict(float)
    for r in records:
        by_category[r["category"]] += r["total"]
    
    # Revenue by region
    by_region = defaultdict(float)
    for r in records:
        by_region[r["region"]] += r["total"]
    
    # Top products by revenue
    by_product = defaultdict(float)
    for r in records:
        by_product[r["product"]] += r["total"]
    
    top_products = sorted(by_product.items(), key=lambda x: x[1], reverse=True)
    
    # Daily revenue
    by_date = defaultdict(float)
    for r in records:
        by_date[r["date"]] += r["total"]
    
    return {
        "total_revenue": sum(r["total"] for r in records),
        "total_orders": len(records),
        "avg_order_value": sum(r["total"] for r in records) / len(records) if records else 0,
        "by_category": dict(by_category),
        "by_region": dict(by_region),
        "top_products": top_products[:5],
        "daily_revenue": dict(sorted(by_date.items())),
    }


def print_report(summary):
    """Print a formatted analysis report."""
    print("\n" + "=" * 50)
    print("  SALES ANALYSIS REPORT")
    print("=" * 50)
    
    print(f"\n  Total Revenue:    ${summary['total_revenue']:>12,.2f}")
    print(f"  Total Orders:     {summary['total_orders']:>12}")
    print(f"  Avg Order Value:  ${summary['avg_order_value']:>12,.2f}")
    
    print("\n  Revenue by Category:")
    for cat, rev in sorted(summary["by_category"].items(), key=lambda x: x[1], reverse=True):
        pct = rev / summary["total_revenue"] * 100
        bar = "█" * int(pct / 2)
        print(f"    {cat:<15} ${rev:>10,.2f}  {pct:>5.1f}%  {bar}")
    
    print("\n  Revenue by Region:")
    for region, rev in sorted(summary["by_region"].items(), key=lambda x: x[1], reverse=True):
        print(f"    {region:<10} ${rev:>10,.2f}")
    
    print("\n  Top Products:")
    for product, rev in summary["top_products"]:
        print(f"    {product:<15} ${rev:>10,.2f}")
    
    print("\n  Daily Revenue:")
    for date, rev in summary["daily_revenue"].items():
        bar = "█" * int(rev / 200)
        print(f"    {date}  ${rev:>10,.2f}  {bar}")
    
    print("\n" + "=" * 50)


# Run the pipeline
print("Loading and cleaning data...")
records, errors = load_and_clean(RAW_DATA)
print(f"Loaded {len(records)} valid records, {errors} errors\n")

summary = analyze(records)
print_report(summary)
```

### Exercise 4.C.2 — JSON Configuration Manager

```python
"""
Build a config manager that loads, validates, and merges JSON configs.
This pattern is used in almost every real application.
"""

import json
import os
from pathlib import Path


DEFAULT_CONFIG = {
    "app": {
        "name": "my-service",
        "version": "0.1.0",
        "debug": False,
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8000,
        "workers": 1,
    },
    "logging": {
        "level": "INFO",
        "format": "json",
    },
    "database": {
        "url": "sqlite:///app.db",
        "pool_size": 5,
    },
}


def deep_merge(base, overrides):
    """Deeply merge two dicts. Overrides take precedence."""
    result = base.copy()
    for key, value in overrides.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def validate_config(config):
    """Validate config and return list of errors."""
    errors = []
    
    # Required fields
    if "app" not in config:
        errors.append("Missing 'app' section")
    elif "name" not in config["app"]:
        errors.append("Missing 'app.name'")
    
    # Type checks
    if "server" in config:
        port = config["server"].get("port")
        if port is not None and (not isinstance(port, int) or port < 1 or port > 65535):
            errors.append(f"Invalid port: {port} (must be 1-65535)")
        
        workers = config["server"].get("workers")
        if workers is not None and (not isinstance(workers, int) or workers < 1):
            errors.append(f"Invalid workers: {workers} (must be >= 1)")
    
    if "logging" in config:
        level = config["logging"].get("level", "")
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if level not in valid_levels:
            errors.append(f"Invalid log level: '{level}'. Valid: {valid_levels}")
    
    return errors


def load_config(config_path=None, env_prefix="APP_"):
    """
    Load config with layered overrides:
    1. Default config
    2. Config file (if provided)
    3. Environment variables (highest priority)
    """
    config = DEFAULT_CONFIG.copy()
    
    # Layer 2: Config file
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path) as f:
                file_config = json.load(f)
            config = deep_merge(config, file_config)
            print(f"  Loaded config from {config_path}")
        except json.JSONDecodeError as e:
            print(f"  Warning: Invalid JSON in {config_path}: {e}")
    
    # Layer 3: Environment variables
    env_overrides = {}
    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            # APP_SERVER_PORT → server.port
            parts = key[len(env_prefix):].lower().split("_")
            if len(parts) == 2:
                section, setting = parts
                if section not in env_overrides:
                    env_overrides[section] = {}
                # Try to parse as int/bool
                if value.lower() in ("true", "false"):
                    value = value.lower() == "true"
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                env_overrides[section][setting] = value
    
    if env_overrides:
        config = deep_merge(config, env_overrides)
        print(f"  Applied {len(env_overrides)} env overrides")
    
    # Validate
    errors = validate_config(config)
    if errors:
        print(f"\n  Config validation errors:")
        for err in errors:
            print(f"    ✗ {err}")
    
    return config


# Demo
print("=== Loading Config ===")
config = load_config()

print(f"\n=== Final Config ===")
print(json.dumps(config, indent=2))

# Test deep merge
print(f"\n=== Testing Deep Merge ===")
override = {"server": {"port": 9000, "workers": 4}, "app": {"debug": True}}
merged = deep_merge(DEFAULT_CONFIG, override)
print(f"  Port: {merged['server']['port']}")        # 9000 (overridden)
print(f"  Host: {merged['server']['host']}")         # 0.0.0.0 (kept default)
print(f"  Debug: {merged['app']['debug']}")          # True (overridden)
```

### Exercise 4.C.3 — Calling Real APIs

```python
"""
Call real public APIs and process the responses.
These are free APIs that don't require API keys.
"""

import requests
import json


def fetch_github_user(username):
    """Fetch a GitHub user's public profile."""
    url = f"https://api.github.com/users/{username}"
    
    response = requests.get(url, timeout=10, headers={
        "Accept": "application/vnd.github.v3+json",
    })
    
    if response.status_code == 404:
        print(f"  User '{username}' not found")
        return None
    
    response.raise_for_status()
    
    data = response.json()
    return {
        "login": data["login"],
        "name": data.get("name", "N/A"),
        "bio": data.get("bio", "N/A"),
        "public_repos": data["public_repos"],
        "followers": data["followers"],
        "following": data["following"],
        "created_at": data["created_at"][:10],
    }


def fetch_github_repos(username, sort="updated", limit=5):
    """Fetch a user's public repositories."""
    url = f"https://api.github.com/users/{username}/repos"
    
    response = requests.get(url, timeout=10, params={
        "sort": sort,
        "per_page": limit,
    })
    response.raise_for_status()
    
    repos = []
    for repo in response.json():
        repos.append({
            "name": repo["name"],
            "description": repo.get("description", ""),
            "language": repo.get("language", "N/A"),
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "updated": repo["updated_at"][:10],
        })
    
    return repos


# Try it (use any GitHub username)
try:
    print("=== GitHub Profile ===")
    profile = fetch_github_user("torvalds")
    if profile:
        for key, value in profile.items():
            print(f"  {key:<15} {value}")
    
    print("\n=== Recent Repos ===")
    repos = fetch_github_repos("torvalds", limit=3)
    for repo in repos:
        print(f"  {repo['name']:<25} ⭐ {repo['stars']:<6} {repo['language']}")
        if repo["description"]:
            print(f"  {'':25} {repo['description'][:60]}")

except requests.ConnectionError:
    print("  No internet connection")
except requests.Timeout:
    print("  Request timed out")
except requests.HTTPError as e:
    print(f"  API error: {e}")
```

### Exercise 4.C.4 — Retry and Rate Limiting

```python
"""
Production API calls need retry logic and rate limit handling.
"""

import time
import requests


def api_call_with_retry(url, max_retries=3, backoff_factor=1.0, timeout=10):
    """
    Make an API call with exponential backoff retry.
    
    Retry on: connection errors, timeouts, 429 (rate limited), 500+ (server errors)
    Don't retry on: 400, 401, 403, 404 (client errors)
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            
            # Success
            if response.ok:
                return response
            
            # Rate limited — wait and retry
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", backoff_factor * attempt))
                print(f"  Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                continue
            
            # Server error — retry
            if response.status_code >= 500:
                wait = backoff_factor * (2 ** (attempt - 1))
                print(f"  Server error ({response.status_code}). Retry {attempt}/{max_retries} in {wait}s")
                time.sleep(wait)
                continue
            
            # Client error — don't retry
            response.raise_for_status()
        
        except requests.ConnectionError:
            wait = backoff_factor * (2 ** (attempt - 1))
            print(f"  Connection failed. Retry {attempt}/{max_retries} in {wait}s")
            if attempt < max_retries:
                time.sleep(wait)
        
        except requests.Timeout:
            wait = backoff_factor * (2 ** (attempt - 1))
            print(f"  Timeout. Retry {attempt}/{max_retries} in {wait}s")
            if attempt < max_retries:
                time.sleep(wait)
    
    raise requests.ConnectionError(f"Failed after {max_retries} attempts")


# Test with a real endpoint
try:
    response = api_call_with_retry("https://httpbin.org/get")
    print(f"Success: {response.status_code}")
except requests.ConnectionError as e:
    print(f"Final failure: {e}")

# Test with simulated failures
try:
    response = api_call_with_retry(
        "https://httpbin.org/status/500",  # Always returns 500
        max_retries=3,
        backoff_factor=0.5,
    )
except requests.HTTPError as e:
    print(f"Expected failure: {e}")
```

### Exercise 4.C.5 — Building an API Client Class

```python
"""
Wrap API calls in a clean client class.
This is how professional Python codebases interact with external APIs.
"""

import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherData:
    """Structured weather data."""
    city: str
    temperature_c: float
    description: str
    humidity: int
    wind_speed: float
    
    @property
    def temperature_f(self):
        return self.temperature_c * 9/5 + 32
    
    def __str__(self):
        return (
            f"{self.city}: {self.temperature_c:.1f}°C ({self.temperature_f:.1f}°F), "
            f"{self.description}, humidity {self.humidity}%, wind {self.wind_speed} m/s"
        )


class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class WeatherClient:
    """
    Client for a weather API.
    
    Demonstrates: encapsulation, error handling, data validation,
    clean interface design.
    """
    
    BASE_URL = "https://wttr.in"
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "PythonLearning/1.0",
        })
    
    def get_weather(self, city: str) -> Optional[WeatherData]:
        """Get current weather for a city."""
        if not city or not city.strip():
            raise ValueError("City name cannot be empty")
        
        try:
            url = f"{self.BASE_URL}/{city}"
            response = self.session.get(
                url,
                params={"format": "j1"},
                timeout=self.timeout,
            )
            
            if response.status_code == 404:
                raise WeatherAPIError(f"City '{city}' not found", 404)
            
            response.raise_for_status()
            data = response.json()
            
            current = data["current_condition"][0]
            return WeatherData(
                city=city,
                temperature_c=float(current["temp_C"]),
                description=current["weatherDesc"][0]["value"],
                humidity=int(current["humidity"]),
                wind_speed=float(current["windspeedKmph"]) / 3.6,
            )
        
        except requests.ConnectionError:
            raise WeatherAPIError("No internet connection")
        except requests.Timeout:
            raise WeatherAPIError(f"Request timed out after {self.timeout}s")
        except (KeyError, IndexError, ValueError) as e:
            raise WeatherAPIError(f"Unexpected API response format: {e}")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


# Usage with context manager
try:
    with WeatherClient(timeout=15) as client:
        for city in ["London", "Tokyo", "New York"]:
            try:
                weather = client.get_weather(city)
                print(f"  {weather}")
            except WeatherAPIError as e:
                print(f"  {city}: Error — {e}")
except Exception as e:
    print(f"Client error: {e}")
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 4.D.1 — Debug: CSV Encoding Issues

```python
"""
Bug: reading a CSV file with special characters crashes or shows garbled text.
"""

import csv
from io import StringIO

# Simulating a CSV with special characters
csv_with_unicode = """name,city,notes
José García,São Paulo,Açaí bowl café
Müller,München,Straße → Büro
田中太郎,東京,テスト
"""

# This works with StringIO but fails with some files:
reader = csv.DictReader(StringIO(csv_with_unicode))
for row in reader:
    print(f"  {row['name']:<15} {row['city']:<12} {row['notes']}")


# When reading from files with encoding issues:
def read_csv_safe(filepath, encodings=None):
    """Try multiple encodings to read a CSV file."""
    if encodings is None:
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]
    
    for encoding in encodings:
        try:
            with open(filepath, encoding=encoding) as f:
                content = f.read()
            print(f"  Successfully read with encoding: {encoding}")
            return content
        except UnicodeDecodeError:
            print(f"  Failed with encoding: {encoding}")
            continue
    
    raise ValueError(f"Could not read {filepath} with any encoding")


# Common encoding issues:
# 1. BOM (Byte Order Mark): file starts with \ufeff
#    Fix: use encoding="utf-8-sig" to strip BOM
#
# 2. Latin-1 characters (é, ü, ñ) saved as Latin-1 but read as UTF-8
#    Fix: use encoding="latin-1" or detect with chardet
#
# 3. Windows files with \r\n
#    Fix: csv module handles this with newline="" parameter
```

### Exercise 4.D.2 — Debug: API Response Changes

```python
"""
Bug: API that used to work now returns different JSON structure.
This happens frequently in production.
"""


def process_api_response_fragile(data):
    """FRAGILE: Assumes exact structure."""
    return {
        "id": data["results"][0]["id"],
        "name": data["results"][0]["name"],
        "email": data["results"][0]["email"],
    }


def process_api_response_robust(data):
    """ROBUST: Handles structure changes gracefully."""
    results = data.get("results", data.get("data", []))
    
    if not results:
        return {"error": "No results found"}
    
    first = results[0] if isinstance(results, list) else results
    
    return {
        "id": first.get("id", first.get("user_id", "unknown")),
        "name": first.get("name", first.get("full_name", "unknown")),
        "email": first.get("email", first.get("contact_email", "unknown")),
    }


# Test with different API response formats:
v1_response = {"results": [{"id": 1, "name": "Alice", "email": "alice@test.com"}]}
v2_response = {"data": [{"user_id": 1, "full_name": "Alice", "contact_email": "alice@test.com"}]}
v3_response = {"results": []}
v4_response = {}

for label, data in [("v1", v1_response), ("v2", v2_response), ("v3", v3_response), ("v4", v4_response)]:
    try:
        fragile = process_api_response_fragile(data)
        print(f"  {label} fragile: {fragile}")
    except (KeyError, IndexError) as e:
        print(f"  {label} fragile: CRASHED — {type(e).__name__}: {e}")
    
    robust = process_api_response_robust(data)
    print(f"  {label} robust:  {robust}")
    print()
```

### Exercise 4.D.3 — Debug: Timeout and Connection Handling

```python
"""
Simulate and handle various network failure scenarios.
"""

import requests
import time


def demonstrate_failure_modes():
    """Show common API failure modes and how to handle them."""
    
    test_cases = [
        ("Timeout", "https://httpbin.org/delay/10", {"timeout": 2}),
        ("404 Not Found", "https://httpbin.org/status/404", {"timeout": 5}),
        ("500 Server Error", "https://httpbin.org/status/500", {"timeout": 5}),
        ("Connection Refused", "http://localhost:1", {"timeout": 2}),
        ("DNS Failure", "http://this-domain-does-not-exist-12345.com", {"timeout": 2}),
    ]
    
    for label, url, kwargs in test_cases:
        print(f"\n  {label}:")
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            print(f"    ✓ Success (unexpected): {response.status_code}")
        except requests.Timeout:
            print(f"    ✗ Timeout — server took too long to respond")
            print(f"    → Fix: Increase timeout or add retry logic")
        except requests.ConnectionError as e:
            error_type = type(e.__cause__).__name__ if e.__cause__ else "Unknown"
            print(f"    ✗ Connection failed ({error_type})")
            print(f"    → Fix: Check URL, network, DNS, firewall")
        except requests.HTTPError as e:
            print(f"    ✗ HTTP {e.response.status_code}")
            if e.response.status_code == 404:
                print(f"    → Fix: Check URL path, resource may not exist")
            elif e.response.status_code >= 500:
                print(f"    → Fix: Server issue, retry with backoff")

try:
    demonstrate_failure_modes()
except Exception as e:
    print(f"\nNote: Some tests may fail without internet: {e}")
```

---

## PART E — PRODUCTION SIMULATION

### Scenario: Build a Data Processing CLI Tool

**Task:** Build a complete tool that reads data from a CSV file, enriches it by calling an API, and writes the results to JSON. This simulates a real data pipeline task.

```python
# data_pipeline.py
"""
Data Processing Pipeline

Reads employee data from CSV, looks up additional info,
and produces a JSON report.

Usage:
    python data_pipeline.py input.csv output.json
"""

import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path


def read_employees(filepath):
    """Read employee data from CSV file."""
    if not Path(filepath).exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")
    
    employees = []
    errors = []
    
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        required_fields = {"name", "department", "salary"}
        if not required_fields.issubset(set(reader.fieldnames or [])):
            missing = required_fields - set(reader.fieldnames or [])
            raise ValueError(f"CSV missing required columns: {missing}")
        
        for i, row in enumerate(reader, 1):
            try:
                employee = {
                    "name": row["name"].strip(),
                    "department": row["department"].strip(),
                    "salary": float(row["salary"]),
                    "email": row.get("email", "").strip(),
                    "start_date": row.get("start_date", "").strip(),
                }
                
                if not employee["name"]:
                    raise ValueError("Empty name")
                if employee["salary"] < 0:
                    raise ValueError(f"Negative salary: {employee['salary']}")
                
                employees.append(employee)
            except (ValueError, KeyError) as e:
                errors.append(f"Row {i}: {e}")
    
    return employees, errors


def analyze_employees(employees):
    """Analyze employee data and generate statistics."""
    if not employees:
        return {"error": "No employees to analyze"}
    
    # Department stats
    dept_stats = {}
    for emp in employees:
        dept = emp["department"]
        if dept not in dept_stats:
            dept_stats[dept] = {"count": 0, "total_salary": 0, "employees": []}
        dept_stats[dept]["count"] += 1
        dept_stats[dept]["total_salary"] += emp["salary"]
        dept_stats[dept]["employees"].append(emp["name"])
    
    for dept in dept_stats:
        dept_stats[dept]["avg_salary"] = round(
            dept_stats[dept]["total_salary"] / dept_stats[dept]["count"], 2
        )
    
    # Overall stats
    salaries = [e["salary"] for e in employees]
    
    return {
        "generated_at": datetime.now().isoformat(),
        "total_employees": len(employees),
        "salary_stats": {
            "min": min(salaries),
            "max": max(salaries),
            "average": round(sum(salaries) / len(salaries), 2),
            "total": sum(salaries),
        },
        "departments": dept_stats,
        "highest_paid": max(employees, key=lambda e: e["salary"])["name"],
        "lowest_paid": min(employees, key=lambda e: e["salary"])["name"],
    }


def write_report(report, filepath):
    """Write report to JSON file."""
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    file_size = output_path.stat().st_size
    return file_size


def print_summary(report):
    """Print a human-readable summary."""
    print("\n" + "=" * 50)
    print("  EMPLOYEE REPORT SUMMARY")
    print("=" * 50)
    
    stats = report["salary_stats"]
    print(f"\n  Total Employees:  {report['total_employees']}")
    print(f"  Total Payroll:    ${stats['total']:>12,.2f}")
    print(f"  Average Salary:   ${stats['average']:>12,.2f}")
    print(f"  Salary Range:     ${stats['min']:>12,.2f} — ${stats['max']:,.2f}")
    print(f"  Highest Paid:     {report['highest_paid']}")
    print(f"  Lowest Paid:      {report['lowest_paid']}")
    
    print(f"\n  {'Department':<20} {'Count':>6} {'Avg Salary':>12}")
    print(f"  {'-'*20} {'-'*6} {'-'*12}")
    
    for dept, info in sorted(report["departments"].items()):
        print(f"  {dept:<20} {info['count']:>6} ${info['avg_salary']:>11,.2f}")
    
    print("\n" + "=" * 50)


def main():
    """Main pipeline: Read → Analyze → Write."""
    # Create sample data if no file provided
    if len(sys.argv) < 2:
        # Generate sample CSV
        sample_csv = "/tmp/employees.csv"
        with open(sample_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "department", "salary", "email"])
            writer.writeheader()
            writer.writerows([
                {"name": "Alice Chen", "department": "Engineering", "salary": 120000, "email": "alice@company.com"},
                {"name": "Bob Smith", "department": "Engineering", "salary": 95000, "email": "bob@company.com"},
                {"name": "Charlie Brown", "department": "Marketing", "salary": 85000, "email": "charlie@company.com"},
                {"name": "Diana Ross", "department": "Engineering", "salary": 130000, "email": "diana@company.com"},
                {"name": "Eve Wilson", "department": "Marketing", "salary": 78000, "email": "eve@company.com"},
                {"name": "Frank Lee", "department": "Sales", "salary": 72000, "email": "frank@company.com"},
                {"name": "Grace Kim", "department": "Sales", "salary": 88000, "email": "grace@company.com"},
                {"name": "Hank Jones", "department": "Engineering", "salary": 115000, "email": "hank@company.com"},
            ])
        input_path = sample_csv
        output_path = "/tmp/employee_report.json"
        print(f"  Created sample data: {sample_csv}")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "report.json"
    
    # Pipeline
    start = time.perf_counter()
    
    print(f"\n  Reading: {input_path}")
    employees, errors = read_employees(input_path)
    
    if errors:
        print(f"  Warnings ({len(errors)} rows skipped):")
        for err in errors:
            print(f"    ⚠ {err}")
    
    print(f"  Loaded {len(employees)} employees")
    
    report = analyze_employees(employees)
    
    file_size = write_report(report, output_path)
    elapsed = time.perf_counter() - start
    
    print(f"  Written: {output_path} ({file_size:,} bytes)")
    print(f"  Completed in {elapsed:.3f}s")
    
    print_summary(report)


if __name__ == "__main__":
    main()
```

**Run it:**
```bash
python data_pipeline.py
# or:
python data_pipeline.py employees.csv report.json
```

**Acceptance Criteria:**
- [ ] Reads CSV with proper error handling (missing file, bad data, encoding)
- [ ] Validates all input data (required fields, types, ranges)
- [ ] Produces clean JSON output
- [ ] Handles edge cases (empty file, all invalid rows, missing columns)
- [ ] Prints readable summary to stdout
- [ ] No function longer than 25 lines
- [ ] All major functions have docstrings
- [ ] Uses `with` for all file operations
- [ ] Reports errors but doesn't crash on bad data

---

## Key Takeaways

1. **Always use `with` for files.** It guarantees cleanup even if errors occur.
2. **Use the `csv` module.** Don't split on commas manually — it breaks on quoted fields.
3. **JSON is for data exchange, not storage.** For config files, it's OK. For large datasets, consider databases.
4. **Always check API status codes.** `response.ok` or `response.raise_for_status()`.
5. **Handle network failures.** Add timeouts, retries, and specific error handling.
6. **Validate all external data.** Files, API responses, user input — trust nothing.

---

*After completing this guide, continue with the [Production Engineering Bootcamp](../curriculum/README.md) to learn FastAPI, Docker, CI/CD, and monitoring.*
