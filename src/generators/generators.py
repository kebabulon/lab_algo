import random


def rand_int_array(n: int, lo: int, hi: int, *, distinct: bool = False, seed: int | None = None) -> list[int]:
    random.seed(seed)
    if lo > hi:
        raise ValueError("lo must be lower than hi")

    m: list[int]

    if distinct:
        m = random.sample(range(lo, hi + 1), n)
    else:
        m = [random.randint(lo, hi) for _ in range(n)]

    return m


def many_duplicates(n: int, lo: int, hi: int, k_unique: int = 5, *, seed: int | None = None) -> list[int]:
    random.seed(seed)
    if lo > hi:
        raise ValueError("lo must be lower than hi")

    m = [0] * n
    unique_numbers = rand_int_array(k_unique, lo, hi)

    for i in range(n):
        m[i] = unique_numbers[i % k_unique]

    random.shuffle(m)

    return m


def reverse_sorted(n: int) -> list[int]:
    return list(reversed(range(1, n + 1)))


def rand_float_array(n: int, lo: float = 0.0, hi: float = 0.0, *, seed: int | None = None) -> list[float]:
    random.seed(seed)
    if lo > hi:
        raise ValueError("lo must be lower than hi")

    m = [random.uniform(lo, hi) for _ in range(n)]

    return m
