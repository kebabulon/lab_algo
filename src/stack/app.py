from typer import Typer, Context

import os
from array import array

from src.stack.stack import Stack
from src.constants import STACK_FILE

app = Typer()


class StackContainer:
    """
    Контейнер стака
    Вспомогательный класс, который имеет методы для загрузки и сохранения стака в файл
    """

    def __init__(self):
        self.stack = Stack()
        self.array = array('q', [])

        self.load()

    def load(self):
        if not os.path.exists(STACK_FILE):
            return

        self.array.clear()

        with open(STACK_FILE, 'rb') as f:
            self.array.frombytes(f.read())

        for i in self.array:
            self.stack.push(i)

    def save(self):
        self.array.clear()

        for i in self.stack:
            self.array.append(i)

        with open(STACK_FILE, 'wb') as f:
            self.array.tofile(f)


def get_container(ctx: Context) -> StackContainer:
    stack = ctx.obj
    if not isinstance(stack, StackContainer):
        raise RuntimeError("StackContainer is not initialized")
    return stack


@app.callback()
def main(ctx: Context):
    ctx.obj = StackContainer()


@app.command(
    context_settings={"ignore_unknown_options": True}  # this allows negative numbers
)
def push(ctx: Context, num: int):
    container = get_container(ctx)

    container.stack.push(num)

    container.save()


@app.command(
    context_settings={"ignore_unknown_options": True}
)
def pop(ctx: Context):
    container = get_container(ctx)

    try:
        value = container.stack.pop()
        print(value)
    except IndexError as e:
        print("IndexError:", e)

    container.save()


@app.command()
def peek(ctx: Context):
    container = get_container(ctx)

    try:
        value = container.stack.peek()
        print(value)
    except IndexError as e:
        print("IndexError:", e)


@app.command()
def is_empty(ctx: Context):
    container = get_container(ctx)

    print(container.stack.is_empty())


@app.command(name="len")
def len_command(ctx: Context):
    container = get_container(ctx)

    print(len(container.stack))


@app.command()
def min(ctx: Context):
    container = get_container(ctx)

    try:
        value = container.stack.min()
        print(value)
    except IndexError as e:
        print("IndexError:", e)


@app.command()
def clear(ctx: Context):
    container = get_container(ctx)

    container.stack.clear()

    container.save()


@app.command(name="print")
def print_command(ctx: Context):
    container = get_container(ctx)

    print(*container.stack)
