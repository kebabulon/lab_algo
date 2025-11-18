import pytest

from src.stack.stack import Stack


@pytest.fixture
def stack():
    return Stack()


def test_push(stack):
    stack.push(1)
    assert [*stack] == [1]
    assert stack.tail.value == stack.head.value
    stack.push(2)
    assert [*stack] == [1, 2]
    assert stack.tail.value == 1
    assert stack.head.value == 2


def test_pop(stack):
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.pop() == 1
    # pop from empty stack
    with pytest.raises(IndexError):
        stack.pop()


def test_peek(stack):
    stack.push(1)
    assert stack.peek() == 1
    stack.push(2)
    assert stack.peek() == 2
    stack.pop()
    assert stack.peek() == 1
    stack.pop()
    # peek from empty stack
    with pytest.raises(IndexError):
        stack.peek()


def test_is_empty(stack):
    assert stack.is_empty()
    stack.push(1)
    assert not stack.is_empty()
    stack.pop()
    assert stack.is_empty()


def test_len(stack):
    assert len(stack) == 0
    stack.push(1)
    assert len(stack) == 1
    stack.push(2)
    assert len(stack) == 2
    stack.pop()
    assert len(stack) == 1
    stack.pop()
    assert len(stack) == 0


def test_min(stack):
    stack.push(1)
    assert stack.min() == 1
    stack.push(2)
    assert stack.min() == 1
    stack.push(-999)
    assert stack.min() == -999
    stack.pop()
    assert stack.min() == 1
    stack.clear()
    # min from empty stack
    with pytest.raises(IndexError):
        stack.min()


def test_clear(stack):
    stack.clear()
    assert stack.is_empty()
    stack.push(1)
    stack.push(2)
    stack.clear()
    assert stack.is_empty()


def test_iter(stack):
    stack.push(1)
    stack.push(2)
    stack.push(3)
    m = [*stack]
    assert m == [1, 2, 3]
