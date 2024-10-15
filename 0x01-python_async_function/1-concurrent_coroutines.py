#!/usr/bin/env python3
""" Let's execute multiple coroutines at the same time with async"""

import asyncio
from typing import List

wait_random = __import__("0-basic_async_syntax").wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    spawn wait_random n times with the specified max_delay.

    Args:
    - n (int): the number of times to spawn wait_random coroutine.
    - max_delay (int): the maximum delay for each wait_random coroutine.

    Returns:
    - List[float]: a list of the delays for each wait_random coroutine.

    This function creates n tasks, each running the wait_random coroutine
    with the specified max_delay. The tasks are added to a list and then
    executed concurrently using asyncio.as_completed. The delays for each
    task are then appended to a list and returned.
    """
    delays = []
    tasks = []
    for _ in range(n):
        tasks.append(asyncio.create_task(wait_random(max_delay)))
    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)
    return delays
