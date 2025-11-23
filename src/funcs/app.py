import typer
from src.funcs import funcs

app = typer.Typer()


@app.command()
def factorial(n: int):
    result = funcs.factorial(n)
    print(result)


@app.command()
def factorial_recursive(n: int):
    result = funcs.factorial_recursive(n)
    print(result)


@app.command()
def fibo(n: int):
    result = funcs.fibo(n)
    print(result)


@app.command()
def fibo_recursive(n: int):
    result = funcs.fibo_recursive(n)
    print(result)
