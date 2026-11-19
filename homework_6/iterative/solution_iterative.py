def merge_sort(nums):
    """Слияние снизу вверх без рекурсии. Возвращает новый список."""
    result = list(nums)
    size = len(result)
    buffer = [None] * size
    width = 1
    while width < size:
        for left in range(0, size, 2 * width):
            middle = min(left + width, size)
            right = min(left + 2 * width, size)
            i, j = left, middle
            for position in range(left, right):
                if i < middle and (j == right or result[i] <= result[j]):
                    buffer[position] = result[i]
                    i += 1
                else:
                    buffer[position] = result[j]
                    j += 1
        result, buffer = buffer, result
        width *= 2
    return result


def _partition(values, left, right):
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
        else:
            current += 1
    return less, greater


def quick_sort(nums):
    """Quicksort без рекурсии, с явным стеком границ отрезков."""
    result = list(nums)
    stack = [(0, len(result) - 1)] if len(result) > 1 else []
    while stack:
        left, right = stack.pop()
        while left < right:
            less, greater = _partition(result, left, right)
            # Большую часть откладываем, меньшую обрабатываем сразу.
            if less - left < right - greater:
                if greater + 1 < right:
                    stack.append((greater + 1, right))
                right = less - 1
            else:
                if left < less - 1:
                    stack.append((left, less - 1))
                left = greater + 1
    return result


if __name__ == "__main__":
    nums = [7, 2, 5, 2, 9, 1, 4]
    print("mergesort:", merge_sort(nums))
    print("quicksort:", quick_sort(nums))
