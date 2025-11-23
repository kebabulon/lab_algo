import typer

from src.funcs.app import app as funcs_app
from src.sorts.app import app as sorts_app
from src.generators.app import app as generators_app
from src.stack.app import app as stack_app
from src.queue.app import app as queue_app

from src.benchmark import run_benchmarks

app = typer.Typer()

app.add_typer(funcs_app)
app.add_typer(sorts_app)
app.add_typer(generators_app)
app.add_typer(stack_app, name="stack")
app.add_typer(queue_app, name="queue")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    Запуск программы без агрументов. Запускает бенчмарк
    :return: Данная функция ничего не возвращает
    """
    if not ctx.invoked_subcommand:
        run_benchmarks()


if __name__ == "__main__":
    app()
