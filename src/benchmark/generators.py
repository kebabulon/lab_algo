import random


def rand_int_array(n: int, lo: int, hi: int, *, distinct=False, seed=None) -> list[int]:
    random.seed(seed)

    m: list[int]

    if distinct:
        m = random.sample(range(lo, hi + 1), n)
    else:
        m = [random.randint(lo, hi) for _ in range(n)]

    return m
