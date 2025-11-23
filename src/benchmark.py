from rich.console import Console
from rich.table import Table

from timeit import default_timer

from src.sorts.sorts import (
    MultisortCallable,
    SORTS_DICT
)

from src.generators import generators

console = Console()

BenchmarkResult = dict[str, dict[str, float]]


def timeit_once(func: MultisortCallable, *args, **kwargs) -> float:
    """
    Засекает время работы функции сортировки на данных аргументах
    :param func: Функция сортировки
    :param *args **kwargs: Аргументы для функции сортировки
    :return: Время работы сортировки на данных аргументах
    """
    start = default_timer()

    func(*args, **kwargs)

    end = default_timer()
    return end - start


def benchmark_sorts(arrays: dict[str, list], algos: dict[str, MultisortCallable], print_status: bool = False) -> BenchmarkResult:
    """
    Запускает сортировки
    :param arrays: Словарь с массивами, которые будут сортироватся
    :param algos: Словарь с функциями сортировок
    :param print_status: Если правда, печатает текущию сортировку.
    :return: Словарь с результатами сортировок
    """
    result: BenchmarkResult = {}

    last_status_len = 0

    for array_name, array in arrays.items():
        result[array_name] = {}
        for algo_name, algo in algos.items():
            if print_status:
                status = f"Running {array_name} {algo_name}"
                padding_len = last_status_len - len(status)
                padding = ' ' * padding_len if padding_len > 0 else ''
                print(status + padding, end="\r", flush=True)
                last_status_len = len(status)
            time = timeit_once(algo, array)
            result[array_name][algo_name] = time

    if print_status:
        print(' ' * last_status_len, end='\r', flush=True)

    return result


def print_benchmark_result(result: BenchmarkResult) -> None:
    """
    Печатает таблицу результатов
    :param result: Словарь с результатами сортировок
    :return: Данная функция ничего не возвращает
    """
    table = Table(title="Benchmark")

    table.add_column("Array", style="cyan")
    table.add_column("Sort", style="magenta")
    table.add_column("Time", style="green")

    for array_name, algos in result.items():
        row_array_name = array_name
        for algo_name, time in sorted(algos.items(), key=lambda x: x[1]):
            table.add_row(row_array_name, algo_name, '{:.6f}'.format(time))
            row_array_name = ""
        table.add_section()

    console.print(table)


def run_benchmarks() -> None:
    """
    Запуск бенчмарка. Создает словарь массивов для сортировки, запускает бенчмарк и печатает таблицу результатов
    :return: Данная функция ничего не возвращает
    """
    arrays: dict[str, list] = {
        # "rand_int_array 1000": generators.rand_int_array(1000, -100, 100),
        "rand_int_array 10000": generators.rand_int_array(10000, -100, 100),
        "rand_int_array 10000 distinct": generators.rand_int_array(10000, -10000, 10000, distinct=True),

        # "many_duplicates 1000": generators.many_duplicates(1000, -100, 100),
        "many_duplicates 10000": generators.many_duplicates(10000, -100, 100),

        # "reverse_sorted 1000": generators.reverse_sorted(1000),
        "reverse_sorted 10000": generators.reverse_sorted(10000),
    }

    result: BenchmarkResult = benchmark_sorts(arrays, SORTS_DICT, print_status=True)
    print_benchmark_result(result)
