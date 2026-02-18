"""
Section 12 — Cloud: Health Checks + Load Testing (C4-C5)
Guide: docs/curriculum/12-cloud-infrastructure-basics.md
"""


# Exercise 12.C.4 — Health Checks (Liveness + Readiness)
# from fastapi import FastAPI, HTTPException
# app = FastAPI()

async def liveness():
    """Am I running?"""
    # TODO: return {"status": "alive"}
    pass


async def readiness():
    """Am I ready to serve traffic?"""
    # TODO: Check database, cache, dependencies
    # TODO: Return 503 if not ready
    pass


# Exercise 12.C.5 — Load Testing Script
def load_test(url: str, num_requests: int = 100, concurrency: int = 10):
    """Simple load test using concurrent.futures."""
    # TODO: Use ThreadPoolExecutor to make concurrent requests
    # TODO: Track response times, status codes, errors
    # TODO: Print summary (avg latency, p99, error rate)
    pass


# --- DEBUG LAB ---

# Exercise 12.D.2 — Debug: SSH Connection Refused
# TODO: Checklist:
# [ ] Is sshd running on the server?
# [ ] Correct IP address?
# [ ] Port 22 open in firewall/security group?
# [ ] SSH key added to authorized_keys?

# Exercise 12.D.4 — Debug: High Cloud Bill
# TODO: Audit resources:
# [ ] Unused VMs still running?
# [ ] Oversized instances?
# [ ] Forgotten load balancers?
# [ ] Excessive data transfer?
