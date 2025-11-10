import typer

from src.funcs.app import app as funcs_app

app = typer.Typer()

app.add_typer(funcs_app)

if __name__ == "__main__":
    app()
