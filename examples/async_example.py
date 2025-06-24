import asyncio
import os
import sys

from pyquerytracker import TrackQuery

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Example 1: Basic async function
@TrackQuery()
async def fetch_data():
    await asyncio.sleep(0.2)
    return "fetched data"


# Example 2: Async function with parameters
@TrackQuery()
async def compute_sum(a, b):
    await asyncio.sleep(0.1)
    return a + b


# Example 3: Class method async tracking
class DatabaseService:
    @TrackQuery()
    async def query_users(self):
        await asyncio.sleep(0.3)
        return ["Alice", "Bob", "Charlie"]


# Example 4: Async function that raises an error
@TrackQuery()
async def fail_fast():
    await asyncio.sleep(0.05)
    raise RuntimeError("Database failure simulation")


# Example 5: Async function with slow duration to trigger logging thresholds
@TrackQuery()
async def slow_operation():
    await asyncio.sleep(0.5)
    return "slow complete"


# Run all examples
async def main():
    print("Example 1: fetch_data →", await fetch_data())
    print("Example 2: compute_sum(5, 7) →", await compute_sum(5, 7))

    service = DatabaseService()
    print("Example 3: query_users →", await service.query_users())

    try:
        await fail_fast()
    except RuntimeError as e:
        print("Example 4: fail_fast → raised:", e)

    print("Example 5: slow_operation →", await slow_operation())


if __name__ == "__main__":
    asyncio.run(main())
