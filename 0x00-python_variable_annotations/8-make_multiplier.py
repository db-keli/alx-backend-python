#!/usr/bin/env python3
"""Complex types - functions"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Creates a multiplier"""

    def mFunc(x: float) -> float:
        """multiplier function"""
        return x * multiplier

    return mFunc
