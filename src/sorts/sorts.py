from functools import cmp_to_key, wraps
from collections.abc import Callable, Iterable, Sized
from typing import Any, TypeVar, Optional, Protocol

from copy import copy

T = TypeVar('T')

KeyFunc = Callable[[T], Any]

KeyType = Optional[KeyFunc]
CmpType = Optional[Callable[[T, T], int]]


class SortCallable(Protocol[T]):
    def __call__(self, a: list[T], *, key: KeyType = None, cmp: CmpType = None, reverse: bool = False) -> list[T]:
        ...


def multisort(sort_func: Callable[[list[T], KeyFunc], list[T]]) -> SortCallable:
    @wraps(sort_func)
    def multisorted(a: list[T], *, key: KeyType = None, cmp: CmpType = None, reverse: bool = False) -> list[T]:
        if not a:
            return []

        if key and cmp:
            raise ValueError("Both key and cmp arguments are defined")

        result = a

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

        # reverse, so that unsorted elements have reverse order
        if reverse:
            result = list(reversed(result))

        if key_len:
            # sort in reverse order to keep correct element order (stable sorting)
            for key_index in range(key_len - 1, -1, -1):
                result = sort_func(result, lambda x: key(x)[key_index])  # type: ignore
        else:
            result = sort_func(result, key)

        # sort is stable, meaning unsorted elements are in reverse order
        # reverse again, so that sorted elements have reverse order
        # https://docs.python.org/3/howto/sorting.html#odds-and-ends
        if reverse:
            result = list(reversed(result))

        return result

    return multisorted


@multisort
def bubble_sort(a: list[T], key: KeyFunc):
    a = copy(a)

    while True:
        swapped = False
        for i in range(1, len(a)):
            if key(a[i - 1]) > key(a[i]):
                a[i - 1], a[i] = a[i], a[i - 1]
                swapped = True
        if not swapped:
            break

    return a


def sort_by_center(a: list[T], low: int, high: int, key: KeyFunc):
    i = low

    for j in range(low, high):
        if key(a[high]) >= key(a[j]):
            a[i], a[j] = a[j], a[i]
            i += 1

    a[i], a[high] = a[high], a[i]

    return i


def quick_sort_helper(a: list[T], low: int, high: int, key: KeyFunc):
    if high > low:
        center = sort_by_center(a, low, high, key)

        quick_sort_helper(a, center + 1, high, key)
        quick_sort_helper(a, low, center - 1, key)


@multisort
def quick_sort(a: list[T], key: KeyFunc):
    a = copy(a)

    quick_sort_helper(a, 0, len(a) - 1, key)

    return a


@multisort
def counting_sort(a: list[T], key: KeyFunc):
    output = copy(a)

    max_key: int = key(a[0])
    if type(max_key) is not int:
        raise ValueError("key function must return int")

    min_key: int = max_key

    #  iterate over
    for v in a[1:]:
        v_key = key(v)
        if type(v_key) is not int:
            raise ValueError("key function must return int")

        if max_key < v_key:
            max_key = v_key
        if min_key > v_key:
            min_key = v_key

    max_key += 1
    if min_key < 0:
        max_key -= min_key
    else:
        min_key = 0

    count = [0] * max_key

    for v in a:
        count[key(v) - min_key] += 1

    for i in range(1, max_key):
        count[i] += count[i - 1]

    for v in reversed(a):
        v_key = key(v) - min_key
        count[v_key] -= 1
        output[count[v_key]] = v

    return output
