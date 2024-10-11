#!/usr/bin/env python3
"""
Type Checking Module. Advanced for function zoom Array
"""
from typing import List, Generator, Any


def zoom_array(lst: List[int], factor: int = 2) -> List[Any]:
    """Zoom Array function: Zooms an array factor times"""
    zoomed_in: List[Any] = [
        item for item in lst
        for i in range(int(factor))
    ]
    return zoomed_in


array: List[int] = [12, 72, 91]

zoom_2x: List[Any] = zoom_array(array)

zoom_3x: List[Any] = zoom_array(array, 3)
