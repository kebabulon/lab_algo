import typer
from src.sorts import sorts

app = typer.Typer()


@app.command(
    context_settings={"ignore_unknown_options": True}  # this allows negative numbers
)
def bubble_sort(a: list[int]):
    result = sorts.bubble_sort(a)
    print(f"bubble_sort({a}) = {result}")
