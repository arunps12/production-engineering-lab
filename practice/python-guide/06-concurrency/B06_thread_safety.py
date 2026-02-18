"""
Exercise 6.B.6 — Thread Safety Problem
Guide: docs/python-guide/06-concurrency-async.md
"""
import threading

counter = 0


def increment_unsafe():
    """Increment counter (NOT thread-safe!)."""
    global counter
    for _ in range(100_000):
        counter += 1  # Race condition!


def increment_safe(lock):
    """Increment counter with lock (thread-safe)."""
    global counter
    for _ in range(100_000):
        # TODO: with lock:
        #     counter += 1
        pass


def demonstrate_race_condition():
    """Show that incrementing without a lock loses updates."""
    global counter
    counter = 0

    threads = [threading.Thread(target=increment_unsafe) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Expected: 400000, Got: {counter}")
    # TODO: Observe that the result is less than 400000!


def demonstrate_thread_safety():
    """Show that a lock fixes the race condition."""
    global counter
    counter = 0
    lock = threading.Lock()

    # TODO: Create threads using increment_safe(lock)
    # TODO: Verify counter == 400000


if __name__ == "__main__":
    print("=== Race Condition Demo ===")
    demonstrate_race_condition()

    print("\n=== Thread-Safe Demo ===")
    demonstrate_thread_safety()
