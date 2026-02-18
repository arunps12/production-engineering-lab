# SECTION 6 — CONCURRENCY & ASYNC PYTHON

---

## PART A — CONCEPT EXPLANATION

### Why Concurrency Matters

Production services handle many things simultaneously:
- Serving 100 API requests at once
- Reading files while processing data
- Making multiple API calls in parallel
- Running background tasks alongside request handling

Without concurrency, each task waits for the previous one to finish — your service is painfully slow.

### The Three Concurrency Models in Python

```
┌──────────────────┬─────────────────┬────────────────────┐
│   Threading      │  Multiprocessing │     Asyncio        │
├──────────────────┼─────────────────┼────────────────────┤
│ Multiple threads │ Multiple procs  │ Single thread,     │
│ in one process   │ separate memory │ cooperative tasks   │
├──────────────────┼─────────────────┼────────────────────┤
│ Shared memory    │ Isolated memory │ Shared memory      │
├──────────────────┼─────────────────┼────────────────────┤
│ GIL-limited      │ True parallelism│ No GIL issue       │
│ (no true ||)     │ (bypasses GIL)  │ (single thread)    │
├──────────────────┼─────────────────┼────────────────────┤
│ Best for: I/O    │ Best for: CPU   │ Best for: I/O      │
│ (network, disk)  │ (math, data)    │ (high concurrency) │
└──────────────────┴─────────────────┴────────────────────┘
```

### The GIL (Global Interpreter Lock)

CPython has a lock that allows only one thread to execute Python bytecode at a time.

**This means:**
- **Threading doesn't speed up CPU-bound work** (math, data processing)
- **Threading DOES speed up I/O-bound work** (network calls, file I/O) — because threads release the GIL while waiting for I/O
- **Multiprocessing bypasses the GIL** — each process has its own interpreter

### I/O-Bound vs CPU-Bound

**I/O-bound** — Waiting for external resources:
```python
# Waiting for network
response = requests.get("https://api.example.com")
# Waiting for disk
data = open("large_file.csv").read()
# Waiting for database
results = cursor.execute("SELECT * FROM users")
```

**CPU-bound** — Processing data:
```python
# Computing
total = sum(x**2 for x in range(10_000_000))
# Data transformation
processed = [complex_transform(item) for item in large_dataset]
```

**Rule**: Use threading/asyncio for I/O. Use multiprocessing for CPU.

### Threading

```python
import threading
import time

def download(url):
    print(f"Downloading {url}...")
    time.sleep(2)  # Simulates network I/O
    print(f"Done: {url}")

# Sequential: 6 seconds
for url in ["url1", "url2", "url3"]:
    download(url)

# Concurrent: ~2 seconds
threads = []
for url in ["url1", "url2", "url3"]:
    t = threading.Thread(target=download, args=(url,))
    threads.append(t)
    t.start()
for t in threads:
    t.join()  # Wait for all threads to finish
```

### concurrent.futures — The Modern Way

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Thread pool for I/O
with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(download, urls)

# Process pool for CPU
with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(heavy_computation, data_chunks)
```

### Asyncio — Cooperative Concurrency

asyncio uses a single thread with an event loop. Tasks voluntarily yield control when waiting:

```python
import asyncio

async def fetch(url):
    print(f"Fetching {url}...")
    await asyncio.sleep(2)  # Simulates I/O (yields control)
    print(f"Done: {url}")
    return f"data from {url}"

async def main():
    # Run concurrently
    results = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3"),
    )
    print(results)  # All three results

asyncio.run(main())  # ~2 seconds total, not 6!
```

**Key insight**: `await` is where the magic happens. It says "I'm waiting for something — let other tasks run."

### async/await Mental Model

```
Event Loop
     │
     ├── Task 1: fetch("url1") → starts download → AWAITS → resumes → done
     ├── Task 2: fetch("url2") → starts download → AWAITS → resumes → done
     └── Task 3: fetch("url3") → starts download → AWAITS → resumes → done
     
Timeline: [1 starts][2 starts][3 starts]...[wait]...[1 done][2 done][3 done]
Total: ~2 seconds (not 6!)
```

### Common Beginner Misunderstandings

1. **"async makes things faster"** — Only for I/O-bound work. `async` CPU work is actually slower (overhead of event loop).
2. **"I need threads for concurrency"** — For I/O (which is most web dev), asyncio is simpler and more efficient than threads.
3. **"More threads = faster"** — Too many threads cause context-switching overhead. Use pool sizes matching your workload.
4. **"Multiprocessing is always better"** — Process creation is expensive (~100ms). For short tasks, the overhead dominates.
5. **"I can mix sync and async freely"** — Calling sync (blocking) code inside `async def` blocks the event loop. Use `run_in_executor` for sync-in-async.

---

## PART B — BEGINNER PRACTICE

### Exercise 6.B.1 — Sequential vs Threaded

Write a function that simulates downloading 5 URLs (each taking 1 second).
First, run sequentially (5 seconds). Then run with threads (~1 second).

### Exercise 6.B.2 — ThreadPoolExecutor

Rewrite Exercise 6.B.1 using `concurrent.futures.ThreadPoolExecutor`.

### Exercise 6.B.3 — First async Program

Write an async function that does 3 things concurrently using `asyncio.gather`.

### Exercise 6.B.4 — async vs sync Timing

Write the same task both synchronously and asynchronously. Measure and compare execution time.

### Exercise 6.B.5 — ProcessPoolExecutor for CPU Work

Write a CPU-intensive function (e.g., compute fibonacci or sum of squares for large numbers).
Run it on a list of inputs using `ProcessPoolExecutor`. Compare time to sequential.

### Exercise 6.B.6 — Thread Safety Problem

Create a shared counter incremented by multiple threads. Observe the race condition.
Then fix it with `threading.Lock`.

```python
counter = 0
def increment():
    global counter
    for _ in range(100_000):
        counter += 1  # NOT thread-safe!
```

---

## PART C — INTERMEDIATE PRACTICE

### Exercise 6.C.1 — Async HTTP Client

Use `aiohttp` to make concurrent HTTP requests:
```python
import aiohttp, asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
```

### Exercise 6.C.2 — Producer-Consumer with Queue

Implement a producer-consumer pattern:
```python
import asyncio

async def producer(queue):
    for i in range(10):
        await queue.put(f"item-{i}")
        await asyncio.sleep(0.1)
    await queue.put(None)  # Sentinel

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Processing {item}")
```

### Exercise 6.C.3 — Timeout and Cancellation

```python
# Set a timeout for an async operation
try:
    result = await asyncio.wait_for(slow_operation(), timeout=5.0)
except asyncio.TimeoutError:
    print("Operation timed out!")

# Cancel a task
task = asyncio.create_task(long_running())
await asyncio.sleep(2)
task.cancel()
```

### Exercise 6.C.4 — Semaphore for Rate Limiting

Limit concurrent operations (e.g., max 5 parallel downloads):
```python
semaphore = asyncio.Semaphore(5)

async def limited_fetch(url):
    async with semaphore:
        # Only 5 instances run concurrently
        return await fetch(url)
```

### Exercise 6.C.5 — Mixing Sync and Async

Run blocking (sync) code inside an async function safely:
```python
import asyncio

def blocking_io():
    import time
    time.sleep(1)
    return "done"

async def main():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_io)
```

---

## PART D — ADVANCED DEBUG LAB

### Exercise 6.D.1 — Debug: async def Blocks the Event Loop

```python
import asyncio, time

async def bad_handler():
    time.sleep(5)  # BUG: Blocks the event loop!
    return "done"
```
Task: Fix using `await asyncio.sleep()` or `run_in_executor`.

### Exercise 6.D.2 — Debug: Race Condition

Two coroutines read-modify-write a shared dictionary. The result is wrong.
Task: Identify the race condition and fix with `asyncio.Lock`.

### Exercise 6.D.3 — Debug: Deadlock

Two threads each hold one lock and wait for the other's lock.
Task: Identify the deadlock pattern and fix by consistent lock ordering.

### Exercise 6.D.4 — Debug: Task Exception Silently Swallowed

A `create_task()` raises an exception but nobody sees it.
Task: Ensure exceptions in tasks are properly caught and logged.

---

## PART E — PRODUCTION SIMULATION

### Scenario: Concurrent Data Pipeline

Build a data pipeline that:
1. **Fetches** data from 10 URLs concurrently (async)
2. **Processes** each response (CPU work — multiprocessing)
3. **Stores** results in a database (async)
4. **Rate-limits** to max 5 concurrent requests (semaphore)
5. **Times out** after 10 seconds per URL
6. **Handles errors** gracefully (retries, logging)

---

## Key Takeaways

1. **I/O-bound → threading or asyncio. CPU-bound → multiprocessing.** Know the difference.
2. **The GIL limits threading for CPU work** — but threading still helps for I/O.
3. **asyncio is the modern standard** for I/O concurrency in Python (FastAPI uses it).
4. **`concurrent.futures` is the simplest API** — `ThreadPoolExecutor` and `ProcessPoolExecutor` cover most needs.
5. **Never block the event loop** — Use `await` for I/O, `run_in_executor` for sync code.
6. **Shared mutable state + concurrency = bugs** — Use locks, queues, or avoid sharing altogether.

---
*Next: [Section 7 — System Automation & Scripting](07-system-automation-scripting.md)*
