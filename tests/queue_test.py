import pytest

from src.queue.queue import Queue


@pytest.fixture
def queue():
    return Queue()


def test_enqueue(queue):
    queue.enqueue(1)
    assert [*queue] == [1]
    queue.enqueue(2)
    assert [*queue] == [2, 1]


def test_dequeue(queue):
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    # dequeue from empty queue
    with pytest.raises(IndexError):
        queue.dequeue()


def test_front(queue):
    queue.enqueue(1)
    assert queue.front() == 1
    queue.enqueue(2)
    assert queue.front() == 1
    queue.dequeue()
    assert queue.front() == 2
    queue.dequeue()
    # front from empty queue
    with pytest.raises(IndexError):
        queue.front()


def test_is_empty(queue):
    assert queue.is_empty()
    queue.enqueue(1)
    assert not queue.is_empty()
    queue.dequeue()
    assert queue.is_empty()


def test_len(queue):
    assert len(queue) == 0
    queue.enqueue(1)
    assert len(queue) == 1
    queue.enqueue(2)
    assert len(queue) == 2
    queue.dequeue()
    assert len(queue) == 1
    queue.dequeue()
    assert len(queue) == 0


def test_clear(queue):
    queue.clear()
    assert queue.is_empty()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.clear()
    assert queue.is_empty()


def test_iter(queue):
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    m = [*queue]
    assert m == [3, 2, 1]
