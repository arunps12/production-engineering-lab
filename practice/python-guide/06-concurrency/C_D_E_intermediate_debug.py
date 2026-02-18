"""
Section 6 — Concurrency: Intermediate (C1-C5) + Debug (D1-D4) + Production (E1)
Guide: docs/python-guide/06-concurrency-async.md
"""
import asyncio


# Exercise 6.C.1 — Async HTTP Client
async def fetch_urls(urls: list[str]) -> list:
    """Fetch multiple URLs concurrently with aiohttp."""
    # TODO: pip install aiohttp
    # async with aiohttp.ClientSession() as session:
    #     tasks = [fetch_one(session, url) for url in urls]
    #     return await asyncio.gather(*tasks)
    pass


# Exercise 6.C.2 — Producer-Consumer with Queue
async def producer(queue: asyncio.Queue, items: list):
    """Produce items into the queue."""
    # TODO: for item in items: await queue.put(item)
    # TODO: await queue.put(None)  # Sentinel to stop consumer
    pass


async def consumer(queue: asyncio.Queue, name: str):
    """Consume items from the queue."""
    # TODO: while True:
    #     item = await queue.get()
    #     if item is None: break
    #     print(f"{name} processing {item}")
    pass


# Exercise 6.C.3 — Timeout and Cancellation
async def slow_operation():
    """Simulates a slow operation."""
    await asyncio.sleep(10)
    return "done"


async def with_timeout():
    """Run operation with a timeout."""
    # TODO: try:
    #     result = await asyncio.wait_for(slow_operation(), timeout=3.0)
    # except asyncio.TimeoutError:
    #     print("Timed out!")
    pass


# Exercise 6.C.4 — Semaphore for Rate Limiting
async def rate_limited_fetch(urls: list[str], max_concurrent: int = 5):
    """Fetch URLs with limited concurrency."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited(url):
        async with semaphore:
            # Only max_concurrent tasks run at once
            await asyncio.sleep(0.5)  # Simulate fetch
            return f"data from {url}"

    # TODO: return await asyncio.gather(*[limited(url) for url in urls])
    pass


# --- DEBUG LAB ---

# Exercise 6.D.1 — async def Blocks the Event Loop
import time


async def bad_handler():
    """BUG: time.sleep blocks the event loop!"""
    time.sleep(5)  # BUG!
    return "done"
    # TODO: Fix with: await asyncio.sleep(5)
    # Or: await loop.run_in_executor(None, time.sleep, 5)


# Exercise 6.D.2 — Race Condition with async
shared_data = {"count": 0}


async def increment_unsafe():
    """BUG: Read-modify-write is not atomic even in asyncio."""
    current = shared_data["count"]
    await asyncio.sleep(0)  # Yields control — another task can read same value!
    shared_data["count"] = current + 1


async def increment_safe(lock: asyncio.Lock):
    """Fixed: Use async lock."""
    # TODO: async with lock:
    #     shared_data["count"] += 1
    pass


# Exercise 6.D.4 — Task Exception Silently Swallowed
async def failing_task():
    """This task raises an exception."""
    raise ValueError("Something went wrong!")


async def main_buggy():
    """BUG: Exception is swallowed because nobody awaits the task."""
    task = asyncio.create_task(failing_task())
    await asyncio.sleep(1)
    # TODO: Fix — await the task, or add a callback to handle the exception
