from sys import setrecursionlimit
from functools import cmp_to_key, wraps
from collections.abc import Callable, Sequence
from typing import Any, TypeVar, Optional, Protocol

from copy import copy

setrecursionlimit(1000000)

T = TypeVar('T')

KeyFunc = Callable[[T], Any]

KeyType = Optional[KeyFunc]
CmpType = Optional[Callable[[T, T], int]]

SortCallable = Callable[[list[T], KeyFunc], list[T]]


class MultisortCallable(Protocol[T]):
    def __call__(self, a: list[T], *, key: KeyType = None, cmp: CmpType = None, reverse: bool = False) -> list[T]:
        ...


def power_sort(a: list[T], *, key: KeyType = None, cmp: CmpType = None, reverse: bool = False) -> list[T]:
    a = copy(a)

    if key and cmp:
        raise ValueError("Both key and cmp arguments are defined")

    if key:
        a.sort(key=key, reverse=reverse)
    elif cmp:
        a.sort(key=cmp_to_key(cmp), reverse=reverse)
    else:
        a.sort(reverse=reverse)

    return a


sorts_dict: dict[str, MultisortCallable] = {
    ".sort() (powersort)": power_sort
}


def multisort(stable: bool) -> Callable[[SortCallable], MultisortCallable]:
    def multisort_decorator(sort_func: SortCallable) -> MultisortCallable:
        @wraps(sort_func)
        def multisorted(a: list[T], *, key: KeyType = None, cmp: CmpType = None, reverse: bool = False) -> list[T]:
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
                if isinstance(keys, Sequence):
                    key_len = len(keys)

            # reverse, so that unsorted elements have reverse order
            # https://docs.python.org/3/howto/sorting.html#odds-and-ends
            if reverse and stable:
                result = list(reversed(result))

            if key_len:
                if stable:
                    # sort in reverse order to keep correct element order (stable sorting)
                    for key_index in range(key_len - 1, -1, -1):
                        result = sort_func(result, lambda x: key(x)[key_index])  # type: ignore
                else:
                    raise ValueError("Multiple keys are not supported for unstable sorts")
            else:
                result = sort_func(result, key)

            # if sort is stable, unsorted elements are now in reverse order
            # reverse again, so that sorted elements have reverse order
            if reverse:
                result = list(reversed(result))

            return result

        sorts_dict[sort_func.__name__] = multisorted

        return multisorted
    return multisort_decorator


@multisort(stable=True)
def bubble_sort(a: list[T], key: KeyFunc) -> list[T]:
    while True:
        swapped = False
        for i in range(1, len(a)):
            if key(a[i - 1]) > key(a[i]):
                a[i - 1], a[i] = a[i], a[i - 1]
                swapped = True
        if not swapped:
            break

    return a


def sort_by_center(a: list[T], low: int, high: int, key: KeyFunc) -> int:
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


@multisort(stable=False)
def quick_sort(a: list[T], key: KeyFunc) -> list[T]:
    quick_sort_helper(a, 0, len(a) - 1, key)

    return a


@multisort(stable=True)
def counting_sort(a: list[T], key: KeyFunc) -> list[T]:
    output = copy(a)

    max_key: int = key(a[0])
    if type(max_key) is not int:
        raise ValueError("key function must return int")

    min_key: int = max_key

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
