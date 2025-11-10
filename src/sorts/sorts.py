from functools import cmp_to_key, wraps
from collections.abc import Callable, Iterable, Sized
from typing import Any, TypeVar, Optional, Protocol

from copy import copy

T = TypeVar('T')

KeyFunc = Callable[[T], Any]

KeyType = Optional[KeyFunc]
CmpType = Optional[Callable[[T, T], int]]


class SortCallable(Protocol[T]):
    def __call__(self, a: list[T], *, key: KeyType = None, cmp: CmpType = None) -> list[T]:
        ...


def multisort(sort_func: Callable[[list[T], KeyFunc], None]) -> SortCallable:
    @wraps(sort_func)
    def multisorted(a: list[T], *, key: KeyType = None, cmp: CmpType = None) -> list[T]:
        if not a:
            return []

        if key and cmp:
            raise ValueError("Both key and cmp arguments are defined")

        result = copy(a)

        if cmp:
            key = cmp_to_key(cmp)
            key_len = 0
        else:
            if not key:
                def key(x):
                    return x

            key_len = 0
            keys = key(a[0])
            if isinstance(keys, Iterable) and isinstance(keys, Sized):
                key_len = len(keys)

        if key_len:
            # sort in reverse order to keep correct element order (stable sorting)
            for key_index in range(key_len - 1, -1, -1):
                sort_func(result, lambda x: key(x)[key_index])  # type: ignore
        else:
            sort_func(result, key)

        return result

    return multisorted


@multisort
def bubble_sort(a: list[T], key: KeyFunc):
    while True:
        swapped = False
        for i in range(1, len(a)):
            if key(a[i - 1]) > key(a[i]):
                a[i - 1], a[i] = a[i], a[i - 1]
                swapped = True
        if not swapped:
            break
