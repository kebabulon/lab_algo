from sys import setrecursionlimit
from functools import (
    cmp_to_key,
    wraps,
    partial
)
from collections.abc import Callable, Sequence
from typing import Any, TypeVar, Optional, Protocol

from math import ceil
from copy import copy

setrecursionlimit(1000000)

T = TypeVar('T')

KeyFunc = Callable[[T], Any]

KeyType = Optional[KeyFunc]
CmpType = Optional[Callable[[T, T], int]]

SortCallable = Callable[[list[T], KeyFunc], list[T]]


class MultisortCallable(Protocol[T]):
    def __call__(self, a: list[T], key: KeyType = None, cmp: CmpType = None, reverse: bool = False, *args, **kwargs) -> list[T]:
        ...


SORTS_DICT: dict[str, MultisortCallable] = {}


def multisort(stable: bool, comparing: bool) -> Callable[[SortCallable], MultisortCallable]:
    """
    Фабрика декоратора, добавляющего аргументы key, cmp, reverse и дополнительные проверки для функции сортировки
    Каждая функция сортировки добавляется в словарь SORTS_DICT
    Имплементирует принцип multisort, позволяющий использовать несравнивующие алгоритмы сортировок с несколькими ключами
    :param stable: Является ли алгоритм сортировки стабильным (несортированные значения оставляют свой изначальный порядок)
    :param comparing: Использует ли алгоритм сортировки сравения (например counting_sort использует индексацию, по-этому он не работает с cmp)
    :return: Декоратор, возращающий функцию сортировки с аргументами key, cmp и reverse
    """
    def multisort_decorator(sort_func: SortCallable) -> MultisortCallable:
        @wraps(sort_func)
        def multisorted(a: list[T], key: KeyType = None, cmp: CmpType = None, reverse: bool = False, *args, **kwargs) -> list[T]:
            if not a:
                return []

            if key and cmp:
                raise ValueError("Both key and cmp arguments are defined")

            if not comparing and cmp:
                raise ValueError("cmp for non-comparing sort")

            result = copy(a)

            if cmp:
                key = cmp_to_key(cmp)
                key_len = 0
            else:
                if not key:
                    def key(x):
                        return x

                key_len = 0
                # get key function of first element to check the length of keys
                keys = key(a[0])
                if isinstance(keys, Sequence) and not isinstance(keys, str):
                    key_len = len(keys)
                    if not comparing:
                        for i in a[1:]:
                            if len(key(i)) != key_len:
                                raise ValueError("Key function must return same length Sequence for non-comparing sorts")

            # reverse, so that unsorted elements have reverse order
            # https://docs.python.org/3/howto/sorting.html#odds-and-ends
            if reverse and stable:
                result = list(reversed(result))

            if key_len and not comparing:
                # sort in reverse order to keep correct element order (stable sorting)
                for key_index in range(key_len - 1, -1, -1):
                    result = sort_func(result, lambda x: key(x)[key_index], *args, **kwargs)  # type: ignore
            else:
                result = sort_func(result, key, *args, **kwargs)

            # if sort is stable, unsorted elements are now in reverse order
            # reverse again, so that sorted elements have reverse order
            if reverse:
                result = list(reversed(result))

            return result

        SORTS_DICT[sort_func.__name__] = multisorted

        return multisorted
    return multisort_decorator


@multisort(
    stable=True,
    comparing=True
)
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


@multisort(
    stable=False,
    comparing=True
)
def quick_sort(a: list[T], key: KeyFunc) -> list[T]:
    quick_sort_helper(a, 0, len(a) - 1, key)

    return a


@multisort(
    stable=True,
    comparing=False
)
def counting_sort(a: list[T], key: KeyFunc) -> list[T]:
    output = copy(a)

    max_key: int = key(a[0])
    min_key: int = max_key

    for v in a[1:]:
        v_key = key(v)
        if not isinstance(v_key, int):
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


def radix_sort_helper(a: list[T], key: KeyFunc, base: int = 10):
    max_key: int = max([key(x) for x in a])
    if not isinstance(max_key, int):
        raise ValueError("key function must return int")

    exp = 1
    while max_key // exp > 0:
        a = counting_sort(a, key=lambda x: (key(x) // exp) % base)
        exp *= base

    return a


@multisort(
    stable=True,
    comparing=False
)
def radix_sort(a: list[T], key: KeyFunc, base: int = 10) -> list[T]:
    positive_a: list[T] = []
    negative_a: list[T] = []

    for v in a:
        if key(v) < 0:
            negative_a.append(v)
        else:
            positive_a.append(v)

    def abs_key(x):
        return abs(key(x))

    if positive_a:
        positive_a = radix_sort_helper(positive_a, key=key, base=base)
    if negative_a:
        # reverse before sorting to keep unsorted elements order (stable)
        negative_a.reverse()
        negative_a = radix_sort_helper(negative_a, key=abs_key, base=base)
        # reverse negatinve_a because its sorted by digits
        # meaning the bigger the number, the lesser it is
        negative_a.reverse()

    return negative_a + positive_a


@multisort(
    stable=True,
    comparing=False
)
def bucket_sort(a: list[T], key: KeyFunc, buckets: int | None = None, sort: MultisortCallable | None = None) -> list[T]:
    if not sort:
        sort = bucket_sort

    if not buckets:
        buckets = ceil(len(a) / 2)
    if len(a) == 2:
        buckets = 2
    if buckets <= 0:
        raise ValueError("buckets must be positive")

    max_key: float = max([key(x) for x in a])
    min_key: float = min([key(x) for x in a])

    # keys are the same, no need to sort
    if max_key == min_key:
        return a

    def normalised_key(x):
        x = key(x)
        if not isinstance(x, (float, int)):
            raise ValueError("key function must return float")
        x -= min_key
        # 0.999999 so that key maps to [0, 1)
        x *= (0.999999 / (max_key - min_key))
        return x

    bucket_list: list[list[T]] = [[] for _ in range(buckets)]

    for v in a:
        index = int(normalised_key(v) * buckets)
        bucket_list[index].append(v)

    for i in range(buckets):
        if bucket_list[i]:
            bucket_list[i] = sort(bucket_list[i], key=key)

    # return flattened out list
    return [x for bucket in bucket_list for x in bucket]


SORTS_DICT["bucket_sort (quick_sort)"] = partial(bucket_sort, sort=quick_sort)


@multisort(
    stable=False,
    comparing=True
)
def heap_sort(a: list[T], key: KeyFunc) -> list[T]:
    start = len(a) // 2
    end = len(a)

    while end > 1:
        if start > 0:
            start -= 1
        else:
            end -= 1
            a[end], a[0] = a[0], a[end]

        root = start
        while 2 * root + 1 < end:
            child = 2 * root + 1

            if child + 1 < end and key(a[child]) < key(a[child + 1]):
                child = child + 1

            if key(a[root]) < key(a[child]):
                a[root], a[child] = a[child], a[root]
                root = child
            else:
                break

    return a
