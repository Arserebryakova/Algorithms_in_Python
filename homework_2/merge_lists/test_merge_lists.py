from merge_lists.merge_lists_solution import merge_with_dummy, merge_without_dummy
from stack_vs_queue.stack_vs_queue_solution import Node


def build_list(values):
    # Создаёт связный список и сохраняет его исходные узлы
    head = None
    nodes = []

    for value in reversed(values):
        head = Node(value, head)
        nodes.append(head)

    return head, nodes


def check_merge(merge_function, values1, values2, expected):
    # Проверяет значения, сохранение исходных узлов и отсутствие циклов
    # Для каждого запуска создаём новые цепочки
    list1, nodes1 = build_list(values1)
    list2, nodes2 = build_list(values2)

    original_nodes = nodes1 + nodes2
    original_ids = {id(node) for node in original_nodes}
    original_values = {id(node): node.value for node in original_nodes}

    head = merge_function(list1, list2)

    result = []
    visited_ids = set()
    current = head

    while current is not None:
        node_id = id(current)

        # Повторное посещение узла означает цикл
        assert node_id not in visited_ids, "В результате найден цикл"

        # Результат должен состоять только из исходных узлов
        assert node_id in original_ids, "В результат добавлен новый узел"

        # Слияние меняет ссылки, но не значения узлов
        assert current.value == original_values[node_id]

        visited_ids.add(node_id)
        result.append(current.value)
        current = current.next

    assert result == expected
    assert visited_ids == original_ids, "Часть исходных узлов потеряна"


class MergeTestCases:
    # Общие сценарии для обоих способов слияния

    def test_example(self):
        # Пример из условия
        check_merge(
            self.merge,
            [1, 2, 4],
            [1, 3, 4],
            [1, 1, 2, 3, 4, 4],
        )

    def test_first_list_empty(self):
        # При пустом первом списке возвращаем голову второго
        list2, _ = build_list([1, 3, 5])

        assert self.merge(None, list2) is list2

    def test_second_list_empty(self):
        # При пустом втором списке возвращаем голову первого
        list1, _ = build_list([2, 4, 6])

        assert self.merge(list1, None) is list1

    def test_both_lists_empty(self):
        # Слияние двух пустых списков даёт пустой список
        assert self.merge(None, None) is None

    def test_identical_values(self):
        # Значения списков одинаковые, но узлы в них разные
        check_merge(
            self.merge,
            [1, 2, 3],
            [1, 2, 3],
            [1, 1, 2, 2, 3, 3],
        )

    def test_many_duplicates(self):
        # Все повторяющиеся значения должны сохраниться
        check_merge(
            self.merge,
            [1, 1, 2, 2, 2, 4],
            [1, 2, 2, 3, 4, 4],
            [1, 1, 1, 2, 2, 2, 2, 2, 3, 4, 4, 4],
        )

    def test_all_values_equal(self):
        # Каждый узел сохраняется, даже если все значения равны
        check_merge(
            self.merge,
            [7, 7, 7],
            [7, 7],
            [7, 7, 7, 7, 7],
        )

    def test_single_nodes_first_smaller(self):
        # Первый узел результата берётся из первого списка
        check_merge(self.merge, [1], [2], [1, 2])

    def test_single_nodes_second_smaller(self):
        # Первый узел результата берётся из второго списка
        check_merge(self.merge, [2], [1], [1, 2])

    def test_single_nodes_equal(self):
        # Два отдельных узла с одинаковым значением
        check_merge(self.merge, [5], [5], [5, 5])

    def test_first_list_longer(self):
        # Первый список длиннее, короткий список заканчивается раньше
        check_merge(
            self.merge,
            [1, 3, 5, 7, 9],
            [4],
            [1, 3, 4, 5, 7, 9],
        )

    def test_second_list_longer(self):
        # Второй список длиннее, короткий список заканчивается раньше
        check_merge(
            self.merge,
            [4],
            [1, 3, 5, 7, 9],
            [1, 3, 4, 5, 7, 9],
        )

    def test_first_list_entirely_smaller(self):
        # После первого списка целиком присоединяем второй
        check_merge(
            self.merge,
            [1, 2, 3],
            [7, 8, 9],
            [1, 2, 3, 7, 8, 9],
        )

    def test_second_list_entirely_smaller(self):
        # После второго списка целиком присоединяем первый
        check_merge(
            self.merge,
            [7, 8, 9],
            [1, 2, 3],
            [1, 2, 3, 7, 8, 9],
        )

    def test_negative_numbers_and_zero(self):
        # Сравнение должно работать с отрицательными числами и нулём
        check_merge(
            self.merge,
            [-8, -3, 0, 5],
            [-6, -3, 0, 2],
            [-8, -6, -3, -3, 0, 0, 2, 5],
        )

    def test_alternating_nodes(self):
        # Узлы поочерёдно берутся из разных списков
        check_merge(
            self.merge,
            [1, 3, 5],
            [2, 4, 6],
            [1, 2, 3, 4, 5, 6],
        )

    def test_long_lists(self):
        # Проверяем слияние двух длинных цепочек
        check_merge(
            self.merge,
            list(range(0, 4000, 2)),
            list(range(1, 4000, 2)),
            list(range(4000)),
        )


class TestMergeWithDummy(MergeTestCases):
    merge = staticmethod(merge_with_dummy)


class TestMergeWithoutDummy(MergeTestCases):
    merge = staticmethod(merge_without_dummy)
