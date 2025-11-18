class Node():
    def __init__(self, value: int):
        self.value: int = value
        self.next: Node | None = None

    def __repr__(self):
        return f"Node({self.value})"


class Stack():
    def __init__(self, has_min: bool = True):
        self.head: Node | None = None
        self.tail: Node | None = None

        self.min_stack: Stack | None = None
        if has_min:
            self.min_stack = Stack(has_min=False)

    # methods to make mypy happy
    def get_head(self) -> Node:
        if not isinstance(self.head, Node):
            raise ValueError('head is None')
        return self.head

    def get_tail(self) -> Node:
        if not isinstance(self.tail, Node):
            raise ValueError('tail is None')
        return self.tail

    def push(self, x: int) -> None:
        new_node = Node(x)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.get_head().next = new_node
            self.head = new_node

        if isinstance(self.min_stack, Stack):
            if self.min_stack.is_empty() or x <= self.min_stack.peek():
                self.min_stack.push(x)

    def pop(self) -> int:
        if self.is_empty():
            raise IndexError("pop from empty stack")

        value = self.get_head().value

        current_node = self.get_tail()
        while current_node.next and current_node.next != self.get_head():
            current_node = current_node.next

        if current_node.next:
            self.head = current_node
            current_node.next = None
        else:
            self.tail = None
            self.head = None

        if isinstance(self.min_stack, Stack):
            if value == self.min_stack.peek():
                self.min_stack.pop()

        return value

    def peek(self) -> int:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.get_head().value

    def is_empty(self) -> bool:
        if self.head and self.tail:
            return False
        return True

    def __len__(self) -> int:
        if self.is_empty():
            return 0

        count = 0
        current_node = self.tail
        while current_node:
            count += 1
            current_node = current_node.next

        return count

    def min(self) -> int:
        if not isinstance(self.min_stack, Stack):
            raise ValueError("min is not supported for has_min=False Stack")
        if self.is_empty():
            raise IndexError("min from empty stack")
        return self.min_stack.peek()

    def clear(self) -> None:
        if self.is_empty():
            return
        self.head = None
        self.tail = None
        if isinstance(self.min_stack, Stack):
            self.min_stack.clear()

    def __iter__(self):
        if not self.is_empty():
            current_node = self.get_tail()
            while current_node:
                yield current_node.value
                current_node = current_node.next

    def __str__(self):
        return f"[{", ".join([str(v) for v in self])}]"

    def __repr__(self):
        return f"Stack({str(self)})"
