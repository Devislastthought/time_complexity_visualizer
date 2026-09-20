

import random

def linear_search(arr, target=None):
 
    if target is None:
        target = -1 

    steps = 0
    for item in arr:
        steps += 1
        if item == target:
            break
    return steps


def binary_search(arr, target=None):
   
    arr = sorted(arr)
    if target is None:
        target = -1 

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
    
    steps = 0
    for i in arr:
        for j in arr:
            steps += 1
    return steps


def selection_sort(arr):
   
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

# Every algorithm this server supports lives here. 

ALGORITHMS = {
    "linear_search": linear_search,
    "binary_search": binary_search,
    "bubble_sort": bubble_sort,
    "nested_loops": nested_loops,
    "selection_sort": selection_sort,
}

def make_random_list(n):
   
    return [random.randint(0, n * 10) for _ in range(n)]
