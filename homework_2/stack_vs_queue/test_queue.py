import pytest

from stack_vs_queue.stack_vs_queue_solution import Queue


def test_queue_initially_empty():
    # Новая очередь пустая, извлекать из неё нельзя
    queue = Queue()

    assert queue.head is None
    assert queue.tail is None

    with pytest.raises(IndexError):
        queue.dequeue()


def test_queue_single_element():
    # Единственный узел одновременно является головой и хвостом
    queue = Queue()
    queue.enqueue(10)

    assert queue.head is not None
    assert queue.head is queue.tail
    assert queue.head.value == 10
    assert queue.tail.next is None

    # После извлечения обе ссылки должны стать None
    result = queue.dequeue()

    assert result == 10
    assert queue.head is None
    assert queue.tail is None


def test_queue_two_elements():
    # Два элемента извлекаются в порядке добавления
    queue = Queue()
    queue.enqueue(10)
    queue.enqueue(20)

    result = [queue.dequeue() for _ in range(2)]

    assert result == [10, 20]
    assert queue.head is None
    assert queue.tail is None


def test_queue_three_elements():
    # Проверяем порядок извлечения трёх элементов
    queue = Queue()
    for value in [10, 20, 30]:
        queue.enqueue(value)

    result = [queue.dequeue() for _ in range(3)]

    assert result == [10, 20, 30]
    assert queue.head is None
    assert queue.tail is None


def test_queue_positive_and_negative():
    # Проверяем положительные и отрицательные значения
    queue = Queue()
    for value in [5, -3, 12, -8]:
        queue.enqueue(value)

    result = [queue.dequeue() for _ in range(4)]

    assert result == [5, -3, 12, -8]
    assert queue.head is None
    assert queue.tail is None


def test_queue_equal_elements():
    # Одинаковые значения остаются отдельными элементами
    queue = Queue()
    for value in [7, 7, 7]:
        queue.enqueue(value)

    result = [queue.dequeue() for _ in range(3)]

    assert result == [7, 7, 7]
    assert queue.head is None
    assert queue.tail is None


def test_queue_with_zero():
    # Ноль сохраняется и извлекается как обычное число
    queue = Queue()
    for value in [0, 5, 0, -2]:
        queue.enqueue(value)

    result = [queue.dequeue() for _ in range(4)]

    assert result == [0, 5, 0, -2]
    assert queue.head is None
    assert queue.tail is None


def test_queue_mixed_operations():
    # Извлекаем часть элементов, оставляя остальные в очереди
    queue = Queue()
    for value in [10, 20, 30, 40]:
        queue.enqueue(value)

    first_result = [queue.dequeue() for _ in range(2)]

    assert first_result == [10, 20]

    # Новый элемент должен извлечься после оставшихся
    queue.enqueue(50)
    second_result = [queue.dequeue() for _ in range(3)]

    assert second_result == [30, 40, 50]
    assert queue.head is None
    assert queue.tail is None


def test_queue_dequeue_after_emptying():
    # После извлечения всех элементов следующий dequeue вызывает ошибку
    queue = Queue()
    queue.enqueue(10)
    queue.enqueue(20)

    result = [queue.dequeue(), queue.dequeue()]

    assert result == [10, 20]
    assert queue.head is None
    assert queue.tail is None

    with pytest.raises(IndexError):
        queue.dequeue()


def test_queue_reuse_after_emptying():
    # Полностью опустошаем очередь
    queue = Queue()
    queue.enqueue(10)
    queue.enqueue(20)

    first_result = [queue.dequeue(), queue.dequeue()]

    assert first_result == [10, 20]
    assert queue.head is None
    assert queue.tail is None

    # Проверяем добавление и извлечение после опустошения
    queue.enqueue(30)
    queue.enqueue(40)

    second_result = [queue.dequeue(), queue.dequeue()]

    assert second_result == [30, 40]
    assert queue.head is None
    assert queue.tail is None


def test_queue_instances_are_independent():
    # Операции с одной очередью не должны менять другую
    first_queue = Queue()
    second_queue = Queue()

    first_queue.enqueue(10)
    second_queue.enqueue(20)
    first_queue.enqueue(30)

    first_result = [first_queue.dequeue(), first_queue.dequeue()]
    second_result = second_queue.dequeue()

    assert first_result == [10, 30]
    assert second_result == 20
    assert first_queue.head is None
    assert first_queue.tail is None
    assert second_queue.head is None
    assert second_queue.tail is None


def test_queue_enqueue_after_leaving_one_element():
    # После извлечения из двух элементов остаётся один
    queue = Queue()
    queue.enqueue(10)
    queue.enqueue(20)

    assert queue.dequeue() == 10
    assert queue.head is not None
    assert queue.head is queue.tail
    assert queue.head.value == 20
    assert queue.tail.next is None

    # Добавление должно правильно продолжить цепочку
    queue.enqueue(30)

    assert queue.head.next is queue.tail
    assert queue.tail.value == 30
    assert queue.tail.next is None

    result = [queue.dequeue(), queue.dequeue()]

    assert result == [20, 30]
    assert queue.head is None
    assert queue.tail is None
