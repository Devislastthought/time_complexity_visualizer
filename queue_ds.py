"""
A Queue is "First In, First Out" (FIFO) — think of a line at a shop.
The first person to join the line is the first one served.

We use collections.deque instead of a plain list because removing
from the front of a list is slow (O(n)), while deque does it in O(1).
"""

from collections import deque


class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        """Add an item to the back of the queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove and return the item at the front of the queue."""
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._items.popleft()

    def peek(self):
        """Look at the item at the front without removing it."""
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self._items[0]

    def is_empty(self):
        """True if the queue has no items."""
        return len(self._items) == 0

    def size(self):
        """How many items are currently in the queue."""
        return len(self._items)

    def __repr__(self):
        return f"Queue({list(self._items)})"
