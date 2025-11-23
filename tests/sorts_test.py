import pytest

from src.sorts import sorts
from src.generators.generators import (
    rand_int_array,
    many_duplicates,
    rand_float_array
)

from tests.constants import SORT_LOOPS, SORT_N, SORT_LO, SORT_HI


def test_multisort():
    # empty array
    assert sorts.bubble_sort([]) == []

    # key function
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.bubble_sort(int_array, key=lambda x: -x) == sorted(int_array, reverse=True)

    # cmp function
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.bubble_sort(int_array, cmp=lambda x, y: y - x) == sorted(int_array, reverse=True)

    # array of non-number values
    for _ in range(SORT_LOOPS):
        list_array = [[1, x] for x in rand_int_array(SORT_N, SORT_LO, SORT_HI)]

        def key(x):
            return x[1]

        assert sorts.bubble_sort(list_array, key=key) == sorted(list_array, key=key)

    # multisort array by value
    for _ in range(SORT_LOOPS):
        many_duplicates_array = many_duplicates(SORT_N, SORT_LO, SORT_HI)
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        list_array = [x for x in zip(many_duplicates_array, int_array)]
        assert sorts.bubble_sort(list_array) == sorted(list_array)

    # multisort array by key
    for _ in range(SORT_LOOPS):
        many_duplicates_array = many_duplicates(SORT_N, SORT_LO, SORT_HI)
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        list_array = [x for x in zip(many_duplicates_array, int_array)]

        def key(x):
            return (-x[0], x[1])

        assert sorts.bubble_sort(list_array, key=key) == sorted(list_array, key=key)

    # reverse
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.bubble_sort(int_array, reverse=True) == sorted(int_array, reverse=True)

    # reverse with key
    for _ in range(SORT_LOOPS):
        many_duplicates_array = many_duplicates(SORT_N, SORT_LO, SORT_HI)
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        list_array = [x for x in zip(many_duplicates_array, int_array)]

        def key(x):
            return x[0]

        assert sorts.bubble_sort(list_array, key=key, reverse=True) == sorted(list_array, key=key, reverse=True)

    # both key and cmp
    with pytest.raises(ValueError):
        sorts.bubble_sort([3, 1, 2], key=lambda x: -x, cmp=lambda x, y: y - x)

    # cmp for non-comparing sort
    with pytest.raises(ValueError):
        sorts.counting_sort([3, 1, 2], cmp=lambda x: -x)

    # key function must return same length Sequence for non-comparing sorts
    with pytest.raises(ValueError):
        sorts.counting_sort([(3, 1), (1, 2, 3), (5,)])


def test_bubble_sort():
    # rand_int_array
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.bubble_sort(int_array) == sorted(int_array)

    # stable
    for _ in range(SORT_LOOPS):
        many_duplicates_array = many_duplicates(SORT_N, SORT_LO, SORT_HI)
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        list_array = [x for x in zip(many_duplicates_array, int_array)]

        def key(x):
            return x[0]

        assert sorts.bubble_sort(list_array, key=key) == sorted(list_array, key=key)


def test_quick_sort():
    # rand_int_array
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.quick_sort(int_array) == sorted(int_array)

    # not stable
    for _ in range(SORT_LOOPS):
        many_duplicates_array = many_duplicates(SORT_N, SORT_LO, SORT_HI)
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        list_array = [x for x in zip(many_duplicates_array, int_array)]

        def key(x):
            return x[0]

        assert sorts.quick_sort(list_array, key=key) != sorted(list_array, key=key)


def test_counting_sort():
    # rand_int_array
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.counting_sort(int_array) == sorted(int_array)

    # stable
    for _ in range(SORT_LOOPS):
        many_duplicates_array = many_duplicates(SORT_N, SORT_LO, SORT_HI)
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        list_array = [x for x in zip(many_duplicates_array, int_array)]

        def key(x):
            return x[0]

        assert sorts.counting_sort(list_array, key=key) == sorted(list_array, key=key)


def test_radix_sort():
    # rand_int_array
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.radix_sort(int_array) == sorted(int_array)

    # stable
    for _ in range(SORT_LOOPS):
        many_duplicates_array = many_duplicates(SORT_N, SORT_LO, SORT_HI)
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        list_array = [x for x in zip(many_duplicates_array, int_array)]

        def key(x):
            return x[0]

        assert sorts.radix_sort(list_array, key=key) == sorted(list_array, key=key)

    # base argument
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.radix_sort(int_array, base=2) == sorted(int_array)


def test_bucket_sort():
    # rand_float_array
    for _ in range(SORT_LOOPS):
        float_array = rand_float_array(SORT_N)
        assert sorts.bucket_sort(float_array) == sorted(float_array)

    # rand_int_array
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.bucket_sort(int_array) == sorted(int_array)

    # stable
    for _ in range(SORT_LOOPS):
        many_duplicates_array = many_duplicates(SORT_N, SORT_LO, SORT_HI)
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        list_array = [x for x in zip(many_duplicates_array, int_array)]

        def key(x):
            return x[0]

        assert sorts.bucket_sort(list_array, key=key) == sorted(list_array, key=key)

    # sort argument
    for _ in range(SORT_LOOPS):
        float_array = rand_float_array(SORT_N)
        assert sorts.bucket_sort(float_array, sort=sorts.bubble_sort) == sorted(float_array)
        assert sorts.bucket_sort(float_array, sort=sorts.quick_sort) == sorted(float_array)

    # buckets argument
    buckets = SORT_N // 5
    for _ in range(SORT_LOOPS):
        float_array = rand_float_array(SORT_N)
        assert sorts.bucket_sort(float_array, buckets=buckets, sort=sorts.quick_sort) == sorted(float_array)


def test_heap_sort():
    # rand_int_array
    for _ in range(SORT_LOOPS):
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        assert sorts.heap_sort(int_array) == sorted(int_array)

    # not stable
    for _ in range(SORT_LOOPS):
        many_duplicates_array = many_duplicates(SORT_N, SORT_LO, SORT_HI)
        int_array = rand_int_array(SORT_N, SORT_LO, SORT_HI)
        list_array = [x for x in zip(many_duplicates_array, int_array)]

        def key(x):
            return x[0]

        assert sorts.heap_sort(list_array, key=key) != sorted(list_array, key=key)
