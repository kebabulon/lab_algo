import typer

from src.generators import generators

app = typer.Typer()


@app.command(
    context_settings={"ignore_unknown_options": True}  # this allows negative numbers
)
def rand_int_array(n: int, lo: int, hi: int, distinct: bool = False, seed: int | None = None):
    result = generators.rand_int_array(n, lo, hi, distinct=distinct, seed=seed)
    print(f"rand_int_array({n}, {lo}, {hi}, distinct={distinct}, seed={seed}) = {result}")


@app.command(
    context_settings={"ignore_unknown_options": True}
)
def many_duplicates(n: int, lo: int, hi: int, k_unique: int = 5, seed: int | None = None):
    result = generators.many_duplicates(n, lo, hi, k_unique=k_unique, seed=seed)
    print(f"many_duplicates({n}, {lo}, {hi}, k_unique={k_unique}, seed={seed}) = {result}")


@app.command()
def reverse_sorted(n: int):
    result = generators.reverse_sorted(n)
    print(f"reverse_sorted({n}) = {result}")


@app.command(
    context_settings={"ignore_unknown_options": True}
)
def rand_float_array(n: int, lo: float = 0.0, hi: float = 1.0, seed: int | None = None):
    result = generators.rand_float_array(n, lo, hi, seed=seed)
    print(f"rand_float_array({n}, {lo}, {hi}, seed={seed}) = {result}")
