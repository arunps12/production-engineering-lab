"""
Exercise 6.B.3 — First async Program
Guide: docs/python-guide/06-concurrency-async.md
"""
import asyncio


async def task_one():
    """Simulate an async task."""
    print("Task 1 starting...")
    await asyncio.sleep(1)
    print("Task 1 done!")
    return "result_1"


async def task_two():
    """Simulate an async task."""
    print("Task 2 starting...")
    await asyncio.sleep(1)
    print("Task 2 done!")
    return "result_2"


async def task_three():
    """Simulate an async task."""
    print("Task 3 starting...")
    await asyncio.sleep(1)
    print("Task 3 done!")
    return "result_3"


async def main():
    """Run all tasks concurrently with asyncio.gather."""
    # TODO: results = await asyncio.gather(task_one(), task_two(), task_three())
    # TODO: print(results)
    # Should take ~1 second total, not 3
    pass


if __name__ == "__main__":
    asyncio.run(main())
