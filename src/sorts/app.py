import typer

from src.sorts import sorts

app = typer.Typer()


@app.command(
    context_settings={"ignore_unknown_options": True}  # this allows negative numbers
)
def bubble_sort(a: list[int], reverse: bool = False):
    result = sorts.bubble_sort(a, reverse=reverse)
    print(f"bubble_sort({a}) = {result}")


@app.command(
    context_settings={"ignore_unknown_options": True}
)
def quick_sort(a: list[int], reverse: bool = False):
    result = sorts.quick_sort(a, reverse=reverse)
    print(f"quick_sort({a}) = {result}")


@app.command(
    context_settings={"ignore_unknown_options": True}
)
def counting_sort(a: list[int], reverse: bool = False):
    result = sorts.counting_sort(a, reverse=reverse)
    print(f"counting_sort({a}) = {result}")


@app.command(
    context_settings={"ignore_unknown_options": True}
)
def radix_sort(a: list[int], base: int = 10, reverse: bool = False):
    result = sorts.radix_sort(a, base=base, reverse=reverse)
    print(f"radix_sort({a}, base={base}) = {result}")
