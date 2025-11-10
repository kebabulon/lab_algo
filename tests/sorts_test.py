import pytest

from src.sorts import sorts
from src.benchmark.generators import rand_int_array


def test_key_and_cmp():
    #  key function
    for i in range(100):
        int_array = rand_int_array(100, -1000, 1000)
        assert sorts.bubble_sort(int_array, key=lambda x: -x) == sorted(int_array, reverse=True)

    #  cmp function
    for i in range(100):
        int_array = rand_int_array(100, -1000, 1000)
        assert sorts.bubble_sort(int_array, cmp=lambda x, y: y - x) == sorted(int_array, reverse=True)

    #  both key and cmp
    with pytest.raises(ValueError):
        sorts.bubble_sort([3, 1, 2], key=lambda x: -x, cmp=lambda x, y: y - x)


def test_bubble_sort():
    #  empty array
    assert sorts.bubble_sort([]) == []

    #  100 rand_int_array
    for i in range(100):
        int_array = rand_int_array(100, -1000, 1000)
        assert sorts.bubble_sort(int_array) == sorted(int_array)
