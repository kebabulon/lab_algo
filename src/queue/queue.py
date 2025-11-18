from src.stack.stack import Stack


class Queue():
    def __init__(self, has_min: bool = True):
        self.stack: Stack = Stack(has_min=False)

    def enqueue(self, x: int) -> None:
        temp_stack = Stack(has_min=False)

        while self.stack:
            temp_stack.push(self.stack.pop())
            print(self.stack)

        self.stack.push(x)

        while temp_stack:
            self.stack.push(temp_stack.pop())
            print(self.stack)

    def dequeue(self) -> int:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.stack.pop()

    def front(self) -> int:
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self.stack.peek()

    def is_empty(self) -> bool:
        return self.stack.is_empty()

    def __len__(self) -> int:
        return len(self.stack)

    def clear(self) -> None:
        self.stack.clear()

    def __iter__(self):
        return iter(self.stack)

    def __str__(self):
        return f"[{", ".join([str(v) for v in self])}]"

    def __repr__(self):
        return f"Queue({str(self)})"
