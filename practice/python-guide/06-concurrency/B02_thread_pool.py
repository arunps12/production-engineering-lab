"""
Exercise 6.B.2 — ThreadPoolExecutor
Guide: docs/python-guide/06-concurrency-async.md
"""
from concurrent.futures import ThreadPoolExecutor
import time


def download(url: str) -> str:
    """Simulate downloading a URL."""
    time.sleep(1)
    return f"data from {url}"


urls = [f"https://api.example.com/data/{i}" for i in range(10)]


def run_with_pool():
    """Use ThreadPoolExecutor to run downloads concurrently."""
    # TODO: with ThreadPoolExecutor(max_workers=5) as executor:
    #     results = list(executor.map(download, urls))
    # TODO: Print results and measure time
    pass


if __name__ == "__main__":
    start = time.time()
    run_with_pool()
    print(f"Pool: {time.time() - start:.2f}s")
