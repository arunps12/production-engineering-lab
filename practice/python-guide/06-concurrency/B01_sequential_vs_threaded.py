"""
Exercise 6.B.1 — Sequential vs Threaded
Guide: docs/python-guide/06-concurrency-async.md
"""
import time
import threading


def download(url: str) -> str:
    """Simulate downloading a URL (takes 1 second)."""
    print(f"Downloading {url}...")
    time.sleep(1)
    print(f"Done: {url}")
    return f"data from {url}"


urls = ["url1", "url2", "url3", "url4", "url5"]


def run_sequential():
    """Run downloads one at a time."""
    # TODO: Loop through urls, call download() for each
    # Measure total time — should be ~5 seconds
    pass


def run_threaded():
    """Run downloads using threads."""
    # TODO: Create a thread for each URL
    # TODO: Start all threads, then join all threads
    # Measure total time — should be ~1 second
    pass


if __name__ == "__main__":
    print("=== Sequential ===")
    start = time.time()
    run_sequential()
    print(f"Sequential: {time.time() - start:.2f}s\n")

    print("=== Threaded ===")
    start = time.time()
    run_threaded()
    print(f"Threaded: {time.time() - start:.2f}s")
