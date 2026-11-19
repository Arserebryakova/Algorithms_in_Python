from functools import wraps
from time import perf_counter


def timer(func):
    """Измеряет весь вызов, печатает время и сохраняет исходный результат."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        started = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_elapsed = perf_counter() - started
            print(f"{func.__name__}: {wrapper.last_elapsed:.6f} s")

    wrapper.last_elapsed = None
    return wrapper


def merge_sort(nums):
    """Рекурсивная сортировка слиянием. Возвращает новый список."""
    result = list(nums)
    buffer = [None] * len(result)

    def sort(left, right):
        # Сортируем полуинтервал [left, right).
        if right - left <= 1:
            return
        middle = (left + right) // 2
        sort(left, middle)
        sort(middle, right)

        i, j = left, middle
        for position in range(left, right):
            if i < middle and (j == right or result[i] <= result[j]):
                buffer[position] = result[i]
                i += 1
            else:
                buffer[position] = result[j]
                j += 1
        for position in range(left, right):
            result[position] = buffer[position]

    sort(0, len(result))
    return result


def _partition(values, left, right):
    """Разбивает [left, right] на части < pivot, == pivot, > pivot."""
    pivot = values[right]
    less = current = left
    greater = right
    while current <= greater:
        if values[current] < pivot:
            values[less], values[current] = values[current], values[less]
            less += 1
            current += 1
        elif values[current] > pivot:
            values[current], values[greater] = values[greater], values[current]
            greater -= 1
            # Перенесённый справа элемент ещё не проверен.
        else:
            current += 1
    return less, greater


def quick_sort(nums):
    """Рекурсивный quicksort с устранением хвостовой рекурсии."""
    result = list(nums)

    def sort(left, right):
        while left < right:
            less, greater = _partition(result, left, right)
            # Рекурсивно сортируем меньшую часть, большую — в этом вызове.
            # Даже при неудачных опорных стек занимает O(log n).
            if less - left < right - greater:
                sort(left, less - 1)
                left = greater + 1
            else:
                sort(greater + 1, right)
                right = less - 1

    sort(0, len(result) - 1)
    return result


if __name__ == "__main__":
    nums = [7, 2, 5, 2, 9, 1, 4]
    print("mergesort:", timer(merge_sort)(nums))
    print("quicksort:", timer(quick_sort)(nums))
