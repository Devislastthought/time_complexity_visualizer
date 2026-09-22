"""
A Stack is "Last In, First Out" (LIFO) — think of a stack of plates.
The last plate you put on top is the first one you take off.
"""


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the item on top of the stack."""
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Look at the item on top without removing it."""
        if self.is_empty():
            raise IndexError("peek from an empty stack")
        return self._items[-1]

    def is_empty(self):
        """True if the stack has no items."""
        return len(self._items) == 0

    def size(self):
        """How many items are currently in the stack."""
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"
