import pytest

from stack_vs_queue.stack_vs_queue_solution import Stack


def test_stack_initially_empty():
    # Новый стек пустой, извлекать из него нельзя
    stack = Stack()

    assert stack.top is None

    with pytest.raises(IndexError):
        stack.pop()


def test_stack_single_element():
    # Добавляем один элемент и проверяем вершину
    stack = Stack()
    stack.push(10)

    assert stack.top is not None
    assert stack.top.value == 10
    assert stack.top.next is None

    # Извлечение возвращает значение и опустошает стек
    result = stack.pop()

    assert result == 10
    assert stack.top is None


def test_stack_two_elements():
    # Два элемента извлекаются в обратном порядке
    stack = Stack()
    stack.push(10)
    stack.push(20)

    result = [stack.pop() for _ in range(2)]

    assert result == [20, 10]
    assert stack.top is None


def test_stack_three_elements():
    # Проверяем порядок извлечения трёх элементов
    stack = Stack()
    for value in [10, 20, 30]:
        stack.push(value)

    result = [stack.pop() for _ in range(3)]

    assert result == [30, 20, 10]
    assert stack.top is None


def test_stack_positive_and_negative():
    # Проверяем положительные и отрицательные значения
    stack = Stack()
    for value in [5, -3, 12, -8]:
        stack.push(value)

    result = [stack.pop() for _ in range(4)]

    assert result == [-8, 12, -3, 5]
    assert stack.top is None


def test_stack_equal_elements():
    # Одинаковые значения остаются отдельными элементами
    stack = Stack()
    for value in [7, 7, 7]:
        stack.push(value)

    result = [stack.pop() for _ in range(3)]

    assert result == [7, 7, 7]
    assert stack.top is None


def test_stack_with_zero():
    # Ноль сохраняется и извлекается как обычное число
    stack = Stack()
    for value in [0, 5, 0, -2]:
        stack.push(value)

    result = [stack.pop() for _ in range(4)]

    assert result == [-2, 0, 5, 0]
    assert stack.top is None


def test_stack_mixed_operations():
    # Извлекаем часть элементов, оставляя остальные в стеке
    stack = Stack()
    for value in [10, 20, 30, 40]:
        stack.push(value)

    first_result = [stack.pop() for _ in range(2)]

    assert first_result == [40, 30]

    # Новый элемент должен извлечься раньше оставшихся
    stack.push(50)
    second_result = [stack.pop() for _ in range(3)]

    assert second_result == [50, 20, 10]
    assert stack.top is None


def test_stack_pop_after_emptying():
    # После извлечения всех элементов следующий pop вызывает ошибку
    stack = Stack()
    stack.push(10)
    stack.push(20)

    result = [stack.pop(), stack.pop()]

    assert result == [20, 10]
    assert stack.top is None

    with pytest.raises(IndexError):
        stack.pop()


def test_stack_reuse_after_emptying():
    # Полностью опустошаем стек
    stack = Stack()
    stack.push(10)
    stack.push(20)

    first_result = [stack.pop(), stack.pop()]

    assert first_result == [20, 10]
    assert stack.top is None

    # Проверяем, что после опустошения можно снова добавлять элементы
    stack.push(30)
    stack.push(40)

    second_result = [stack.pop(), stack.pop()]

    assert second_result == [40, 30]
    assert stack.top is None


def test_stack_instances_are_independent():
    # Операции с одним стеком не должны менять другой
    first_stack = Stack()
    second_stack = Stack()

    first_stack.push(10)
    second_stack.push(20)
    first_stack.push(30)

    first_result = [first_stack.pop(), first_stack.pop()]
    second_result = second_stack.pop()

    assert first_result == [30, 10]
    assert second_result == 20
    assert first_stack.top is None
    assert second_stack.top is None
