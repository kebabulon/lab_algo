import typer
import src.funcs.funcs as funcs

app = typer.Typer()


@app.command()
def factorial(n: int):
    result = funcs.factorial(n)
    print(f"factorial({n}) = {result}")


@app.command()
def factorial_recursive(n: int):
    result = funcs.factorial_recursive(n)
    print(f"factorial_recursive({n}) = {result}")


@app.command()
def fibo(n: int):
    result = funcs.fibo(n)
    print(f"fibo({n}) = {result}")


@app.command()
def fibo_recursive(n: int):
    result = funcs.fibo_recursive(n)
    print(f"fibo_recursive({n}) = {result}")
