"""
Exercise 6.B.5 — ProcessPoolExecutor for CPU Work
Guide: docs/python-guide/06-concurrency-async.md
"""
import time
from concurrent.futures import ProcessPoolExecutor


def heavy_computation(n: int) -> int:
    """CPU-intensive task: sum of squares."""
    return sum(i * i for i in range(n))


numbers = [10_000_000, 10_000_000, 10_000_000, 10_000_000]


def run_sequential():
    """Run computations sequentially."""
    # TODO: results = [heavy_computation(n) for n in numbers]
    pass


def run_parallel():
    """Run computations using ProcessPoolExecutor."""
    # TODO: with ProcessPoolExecutor() as executor:
    #     results = list(executor.map(heavy_computation, numbers))
    pass


if __name__ == "__main__":
    print("=== Sequential ===")
    start = time.time()
    run_sequential()
    print(f"Sequential: {time.time() - start:.2f}s\n")

    print("=== Parallel ===")
    start = time.time()
    run_parallel()
    print(f"Parallel: {time.time() - start:.2f}s")
