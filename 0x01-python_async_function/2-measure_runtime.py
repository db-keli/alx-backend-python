#!/usr/bin/env python3
"""Measure the runtime"""

import time
import asyncio

wait_n = __import__("1-concurrent_coroutines").wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    This function measures the average time taken to execute the
    wait_n function n times.

    Args:
    - n (int): The number of times to execute the wait_n function.
    - max_delay (int): The maximum delay (in seconds) for each call to wait_n.

    Returns:
    - float: The average time taken to execute the wait_n function n times.
    """
    start_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    total_time = time.time() - start_time
    return total_time / n
