"""
Exercise 3.D.2 — Performance Debugging
Guide: docs/python-guide/03-debugging.md

Tasks:
1. Identify the O(n³) performance bottleneck
2. Optimize to O(n) using sets/dicts
3. Measure the performance difference with time.perf_counter
"""

import time


def find_common_elements_slow(list1, list2, list3):
    """Find elements common to all three lists. O(n³) — very slow!"""
    common = []
    for item1 in list1:
        for item2 in list2:
            for item3 in list3:
                if item1 == item2 == item3:
                    if item1 not in common:
                        common.append(item1)
    return common


def find_common_elements_fast(list1, list2, list3):
    """Find elements common to all three lists. Should be O(n)."""
    # TODO: Implement using sets for O(n) performance
    pass


# Generate test data
import random
n = 1000
list1 = [random.randint(0, n) for _ in range(n)]
list2 = [random.randint(0, n) for _ in range(n)]
list3 = [random.randint(0, n) for _ in range(n)]

# TODO: Time both implementations and compare
# start = time.perf_counter()
# result_slow = find_common_elements_slow(list1, list2, list3)
# slow_time = time.perf_counter() - start

# start = time.perf_counter()
# result_fast = find_common_elements_fast(list1, list2, list3)
# fast_time = time.perf_counter() - start

# print(f"Slow: {slow_time:.4f}s, Fast: {fast_time:.4f}s")
# print(f"Speedup: {slow_time / fast_time:.0f}x")
