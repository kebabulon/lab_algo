from functools import cmp_to_key
from collections.abc import Callable
from typing import Any, TypeVar

from copy import copy

T = TypeVar('T')

KeyType = Callable[[T], Any] | None
CmpType = Callable[[T, T], int] | None


def get_key_func(key: KeyType, cmp: CmpType) -> Callable[[T], Any]:
    if key and cmp:
        raise ValueError("Both key and cmp arguments are defined")
    if key:
        return key
    if cmp:
        return cmp_to_key(cmp)

    return lambda x: x


def bubble_sort(a: list[T], key: KeyType = None, cmp: CmpType = None) -> list[T]:
    key_func = get_key_func(key, cmp)
    m = copy(a)

    while True:
        swapped = False
        for i in range(1, len(m)):
            if key_func(m[i - 1]) > key_func(m[i]):
                m[i - 1], m[i] = m[i], m[i - 1]
                swapped = True
        if not swapped:
            break
    return m
