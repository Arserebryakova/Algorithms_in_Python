from random import randrange


def find_kth_largest(nums, k):
    """Возвращает k-й наибольший элемент, учитывая повторы. Вход не меняет."""
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k должно быть целым числом")
    if not 1 <= k <= len(nums):
        raise ValueError("k должно лежать в диапазоне от 1 до len(nums)")

    values = list(nums)
    target = len(values) - k
    left, right = 0, len(values) - 1
    while left <= right:
        pivot = values[randrange(left, right + 1)]
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

        if target < less:
            right = less - 1
        elif target > greater:
            left = greater + 1
        else:
            return values[target]


if __name__ == "__main__":
    print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))
    print(find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))
