"""
Exercise 3.C.5 — Recursive Bug Hunting
Guide: docs/python-guide/03-debugging.md

These recursive functions have bugs. Debug them.
"""


# Bug: Missing base case leads to infinite recursion
def flatten(nested_list):
    """Flatten a nested list into a single list."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        # BUG: What happens with non-list items? They're never added
    return result


# Bug: Off-by-one in base case
def binary_search(arr, target, low=0, high=None):
    """Binary search for target in sorted array."""
    if high is None:
        high = len(arr)  # BUG: should be len(arr) - 1

    if low > high:
        return -1

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid)  # BUG: should be mid - 1


# TODO: Fix both bugs and test
data = [1, [2, 3], [4, [5, 6]], 7]
print(f"Flatten: {flatten(data)}")  # Should be [1, 2, 3, 4, 5, 6, 7]

sorted_arr = [1, 3, 5, 7, 9, 11, 13, 15]
print(f"Search 7: index {binary_search(sorted_arr, 7)}")    # Should be 3
print(f"Search 10: index {binary_search(sorted_arr, 10)}")  # Should be -1
