from typer import Typer, Context

import os
from array import array

from src.queue.queue import Queue
from src.stack.stack import Stack
from src.constants import QUEUE_FILE

app = Typer()


class QueueContainer:
    """
    Контейнер очереди
    Вспомогательный класс, который имеет методы для загрузки и сохранения очереди в файл
    """

    def __init__(self):
        self.queue = Queue()
        self.array = array('q', [])

        self.load()

    def load(self):
        if not os.path.exists(QUEUE_FILE):
            return

        self.array.clear()

        with open(QUEUE_FILE, 'rb') as f:
            self.array.frombytes(f.read())

        queue_stack = Stack()
        for i in self.array:
            queue_stack.push(i)

        self.queue.stack = queue_stack

    def save(self):
        self.array.clear()

        for i in self.queue:
            self.array.append(i)

        with open(QUEUE_FILE, 'wb') as f:
            self.array.tofile(f)


def get_container(ctx: Context) -> QueueContainer:
    queue = ctx.obj
    if not isinstance(queue, QueueContainer):
        raise RuntimeError("QueueContainer is not initialized")
    return queue


@app.callback()
def main(ctx: Context):
    ctx.obj = QueueContainer()


@app.command(
    context_settings={"ignore_unknown_options": True}  # this allows negative numbers
)
def enqueue(ctx: Context, num: int):
    container = get_container(ctx)

    container.queue.enqueue(num)

    container.save()


@app.command(
    context_settings={"ignore_unknown_options": True}
)
def dequeue(ctx: Context):
    container = get_container(ctx)

    try:
        value = container.queue.dequeue()
        print(value)
    except IndexError as e:
        print("IndexError:", e)

    container.save()


@app.command()
def front(ctx: Context):
    container = get_container(ctx)

    try:
        value = container.queue.front()
        print(value)
    except IndexError as e:
        print("IndexError:", e)


@app.command()
def is_empty(ctx: Context):
    container = get_container(ctx)

    print(container.queue.is_empty())


@app.command(name="len")
def len_command(ctx: Context):
    container = get_container(ctx)

    print(len(container.queue))


@app.command()
def clear(ctx: Context):
    container = get_container(ctx)

    container.queue.clear()

    container.save()


@app.command(name="print")
def print_command(ctx: Context):
    container = get_container(ctx)

    print(*container.queue)
