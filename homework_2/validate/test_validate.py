from validate.validate_solution import validate


def test_validate_example_valid():
    # После извлечения 5 можно последовательно извлечь 4 и 2
    pushed = [1, 2, 3, 4, 5]
    popped = [1, 3, 5, 4, 2]

    assert validate(pushed, popped) is True


def test_validate_example_invalid():
    # После извлечения 3 число 2 закрывает доступ к 1
    pushed = [1, 2, 3]
    popped = [3, 1, 2]

    assert validate(pushed, popped) is False


def test_validate_single_element():
    # Единственный элемент добавляем и сразу извлекаем
    assert validate([10], [10]) is True


def test_validate_even_length():
    # Четыре элемента: каждую пару извлекаем в обратном порядке
    pushed = [1, 2, 3, 4]
    popped = [2, 1, 4, 3]

    assert validate(pushed, popped) is True


def test_validate_odd_length():
    # Начало допустимо, но после извлечения 5 вершина — 4, а не 3
    pushed = [1, 2, 3, 4, 5]
    popped = [2, 1, 5, 3, 4]

    assert validate(pushed, popped) is False


def test_validate_reverse_order():
    # Сначала добавляем все элементы, затем извлекаем все
    pushed = [1, 2, 3, 4, 5]
    popped = [5, 4, 3, 2, 1]

    assert validate(pushed, popped) is True


def test_validate_negative_numbers():
    # Отрицательные значения обрабатываются так же, как положительные
    pushed = [-5, -1, -8, -3]
    popped = [-1, -8, -3, -5]

    assert validate(pushed, popped) is True


def test_validate_with_zero():
    # Ноль — обычный элемент последовательности
    pushed = [0, -2, 5]
    popped = [-2, 0, 5]

    assert validate(pushed, popped) is True


def test_validate_max_length():
    # Максимальная длина и максимальное заполнение стека
    pushed = list(range(100_000))
    popped = pushed[::-1]

    assert validate(pushed, popped) is True


def test_validate_same_order():
    # После каждого push сразу выполняется pop
    pushed = [4, 1, 7, 2]
    popped = [4, 1, 7, 2]

    assert validate(pushed, popped) is True


def test_validate_max_length_invalid():
    # Чтобы извлечь последний элемент первым, нужно добавить все
    # После него вершиной будет 99_998, поэтому извлечь 0 нельзя
    pushed = list(range(100_000))
    popped = [99_999] + list(range(99_999))

    assert validate(pushed, popped) is False
