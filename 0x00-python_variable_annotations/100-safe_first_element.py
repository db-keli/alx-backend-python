#!/usr/bin/env python3
"""Duck typing - first element of a sequence"""


from typing import Sequence, Optional, Any


# The types of the elements of the input are not know
def safe_first_element(lst: Sequence[Any]) -> Optional[Any]:
    """Safe First Element"""
    if lst:
        return lst[0]
    else:
        return None
