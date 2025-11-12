import typer

from src.funcs.app import app as funcs_app
from src.sorts.app import app as sorts_app
from src.benchmark.app import app as benchmark_app

app = typer.Typer()

app.add_typer(funcs_app)
app.add_typer(sorts_app)
app.add_typer(benchmark_app)

if __name__ == "__main__":
    app()
