def factorial(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def fibo(n: int) -> int:
    if n <= 0:
        raise ValueError("n должно быть больше 0")
    if n <= 2:
        return 1

    last1 = 1
    last2 = 1
    for i in range(2, n):
        result = last1 + last2
        last2 = last1
        last1 = result
    return result


def fibo_recursive(n: int) -> int:
    if n <= 0:
        raise ValueError("n должно быть больше 0")
    if n <= 2:
        return 1

    return fibo_recursive(n - 1) + fibo_recursive(n - 2)
