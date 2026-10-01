from solution_two_sum import two_sum


def test_preserves_input():
    arr = [10, 4, 3, 1]
    original = arr.copy()

    assert two_sum(arr, 7) == (1, 2)
    assert arr == original


# Первый пример из условия
def test_example_1():
    assert two_sum([1, 3, 4, 10], 7) == (1, 2)


# Второй пример: два одинаковых числа
def test_example_2():
    assert two_sum([5, 5, 1, 4], 10) == (0, 1)


# Пара в начале массива
def test_pair_at_start():
    assert two_sum([2, 7, 20, 30], 9) == (0, 1)


# Пара в конце массива
def test_pair_at_end():
    assert two_sum([20, 30, 2, 7], 9) == (2, 3)


# Первый и последний элементы
def test_first_and_last():
    assert two_sum([2, 20, 30, 7], 9) == (0, 3)


# Пара внутри массива, элементы не рядом
def test_pair_in_middle():
    assert two_sum([20, 3, 30, 40, 8, 50], 11) == (1, 4)


# Минимальный массив из двух элементов
def test_two_elements():
    assert two_sum([2, 7], 9) == (0, 1)


# Ноль входит в пару
def test_zero_in_pair():
    assert two_sum([8, 0, 5, 20], 5) == (1, 2)


# Положительная сумма чисел разных знаков
def test_mixed_signs():
    assert two_sum([-3, 10, 2, 20], 7) == (0, 1)


# Отрицательная сумма двух отрицательных чисел
def test_negative_target():
    assert two_sum([-8, 4, -3, 20], -11) == (0, 2)


# Сумма противоположных чисел равна нулю
def test_opposite_numbers():
    assert two_sum([4, -7, 2, 7], 0) == (1, 3)


# Пара из двух нулей
def test_two_zeros():
    assert two_sum([0, 3, 0, 8], 0) == (0, 2)


# Один элемент нельзя использовать дважды
def test_cannot_reuse_element():
    assert two_sum([3, 2, 4], 6) == (1, 2)


# Повторяющиеся числа, не входящие в ответ
def test_duplicates_outside_pair():
    assert two_sum([1, 1, 1, 4, 6], 10) == (3, 4)


# Большой массив с парой в конце
def test_large_array():
    assert two_sum(list(range(10_000)), 19_997) == (9_998, 9_999)
