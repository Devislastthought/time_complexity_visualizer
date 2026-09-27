"""
Each function below takes a list `arr` and returns how many
"basic operations" (comparisons/steps) it took to run.

We don't care about the actual search/sort result here — we only
care about counting steps, so we can see how the count grows as
the input size (n) grows.
"""

import random

from stack import Stack
from queue_ds import Queue


def linear_search(arr, target=None):
    """Look through the list one by one until we find the target."""
    if target is None:
        target = -1  # a value that is never in arr, so it's a worst-case run

    steps = 0
    for item in arr:
        steps += 1
        if item == target:
            break
    return steps


def binary_search(arr, target=None):
    """Repeatedly cut the (sorted) list in half looking for the target."""
    arr = sorted(arr)
    if target is None:
        target = -1  # worst case: never found, loop runs all the way

    steps = 0
    low, high = 0, len(arr) - 1
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            break
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return steps


def bubble_sort(arr):
    """Repeatedly swap neighbouring items that are in the wrong order."""
    arr = arr.copy()
    steps = 0
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            steps += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return steps


def nested_loops(arr):
    """A plain example of O(n^2): a loop inside a loop."""
    steps = 0
    for i in arr:
        for j in arr:
            steps += 1
    return steps


def selection_sort(arr):
    """Repeatedly find the smallest remaining item and move it to the front."""
    arr = arr.copy()
    steps = 0
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            steps += 1
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return steps


def stack_push_pop(arr):
    """Push every item onto a Stack, then pop everything back off."""
    steps = 0
    s = Stack()
    for item in arr:
        s.push(item)
        steps += 1
    while not s.is_empty():
        s.pop()
        steps += 1
    return steps


def queue_enqueue_dequeue(arr):
    """Enqueue every item into a Queue, then dequeue everything back out."""
    steps = 0
    q = Queue()
    for item in arr:
        q.enqueue(item)
        steps += 1
    while not q.is_empty():
        q.dequeue()
        steps += 1
    return steps


# Every algorithm this server supports lives here. To add a new one,
# write a function above and add one line here.
ALGORITHMS = {
    "linear_search": linear_search,
    "binary_search": binary_search,
    "bubble_sort": bubble_sort,
    "nested_loops": nested_loops,
    "selection_sort": selection_sort,
    "stack_push_pop": stack_push_pop,
    "queue_enqueue_dequeue": queue_enqueue_dequeue,
}



def make_random_list(n):
    """Helper: build a list of n random numbers."""
    return [random.randint(0, n * 10) for _ in range(n)]
