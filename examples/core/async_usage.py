import asyncio
import logging
from pyquerytracker import TrackQuery, configure

# Configure logging to see the output
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Set a low threshold to easily see "slow" logs
configure(slow_log_threshold_ms=150, slow_log_level=logging.WARNING)


@TrackQuery()
async def fast_async_query():
    """An async function that executes quickly."""
    await asyncio.sleep(0.1)
    return "Fast async query completed"


@TrackQuery()
async def slow_async_query():
    """An async function that takes longer to execute."""
    await asyncio.sleep(0.2)
    return "Slow async query completed"


@TrackQuery()
async def failing_async_query():
    """An async function that raises an error."""
    await asyncio.sleep(0.1)
    raise ConnectionError("Could not connect to async database")


async def main():
    print("--- Testing fast async query (should be INFO log) ---")
    result1 = await fast_async_query()
    print(f"Result: {result1}\n")

    print("--- Testing slow async query (should be WARNING log) ---")
    result2 = await slow_async_query()
    print(f"Result: {result2}\n")

    print("--- Testing failing async query (should be ERROR log) ---")
    try:
        await failing_async_query()
    except ConnectionError as e:
        print(f"Caught expected error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
