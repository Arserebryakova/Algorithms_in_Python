import random

from solution_avl import AVL, Node


def assert_avl(tree, expected):
    visited = set()
    values = []

    def check(node, lower=None, upper=None):
        if node is None:
            return 0

        # Проверяем структуру, порядок BST, реальные высоты и баланс.
        assert id(node) not in visited
        visited.add(id(node))
        assert lower is None or lower < node.value
        assert upper is None or node.value < upper

        left_height = check(node.left, lower, node.value)
        values.append(node.value)
        right_height = check(node.right, node.value, upper)

        assert node.height == max(left_height, right_height) + 1
        assert abs(left_height - right_height) <= 1
        return node.height

    check(tree.root)
    assert values == sorted(expected)
    assert tree.inorder() == values


def make_tree(values):
    tree = AVL()
    expected = set()
    for value in values:
        tree.insert(value)
        expected.add(value)
        assert_avl(tree, expected)
    return tree


def test_initial_node():
    node = Node(5)
    assert node.value == 5
    assert node.left is None
    assert node.right is None
    assert node.height == 1


def test_empty_tree():
    tree = AVL()
    assert tree.root is None
    assert tree.search(5) is False
    tree.delete(5)
    assert_avl(tree, [])


def test_single_node():
    tree = make_tree([5])
    assert tree.root.value == 5
    assert tree.search(5) is True
    assert tree.search(0) is False


# Четыре вида нарушения баланса при вставке
def test_insert_rotations():
    for values in [
        [30, 20, 10],  # LL
        [10, 20, 30],  # RR
        [30, 10, 20],  # LR
        [10, 30, 20],  # RL
    ]:
        tree = make_tree(values)
        assert tree.root.value == 20
        assert tree.root.left.value == 10
        assert tree.root.right.value == 30
        assert_avl(tree, values)


def test_rotations_preserve_other_subtrees():
    for values in [
        [50, 30, 70, 20, 40, 60, 80, 10, 5],
        [50, 30, 70, 20, 40, 60, 80, 90, 95],
        [50, 30, 70, 20, 40, 60, 80, 10, 15],
        [50, 30, 70, 20, 40, 60, 80, 90, 85],
        [30, 20, 40, 10, 25, 5],
        [30, 20, 40, 35, 50, 60],
    ]:
        tree = make_tree(values)
        for value in values:
            assert tree.search(value) is True
        assert_avl(tree, values)


def test_duplicate_insertions():
    tree = make_tree([5, 3, 7, 5, 3, 7])
    assert_avl(tree, [3, 5, 7])
    tree.delete(5)
    assert tree.search(5) is False
    assert_avl(tree, [3, 7])


def test_search_all_values_and_missing_values():
    values = [8, 3, 10, 1, 6, 14, 4, 7, 13]
    tree = make_tree(values)

    for value in values:
        assert tree.search(value) is True
    for value in [-100, 0, 2, 5, 9, 11, 100]:
        assert tree.search(value) is False
    assert_avl(tree, values)


def test_delete_only_node():
    tree = make_tree([5])
    tree.delete(5)
    assert tree.root is None
    assert_avl(tree, [])


def test_delete_different_node_types():
    for values, deleted in [
        ([5, 3, 7], 3),               # Лист слева
        ([5, 3, 7], 7),               # Лист справа
        ([5, 3], 5),                  # Корень с левым ребёнком
        ([5, 7], 5),                  # Корень с правым ребёнком
        ([5, 3, 7, 2], 3),            # Внутренний узел с левым ребёнком
        ([5, 3, 7, 4], 3),            # Внутренний узел с правым ребёнком
        ([5, 3, 7], 5),               # Преемник — правый ребёнок
        ([20, 10, 30, 25, 40], 20),    # Преемник глубже в правом поддереве
        ([20, 10, 40, 5, 15, 30, 50, 35], 20),  # У преемника есть ребёнок
        ([20, 10, 30, 5, 15, 25, 35], 10),       # Два ребёнка внутри дерева
    ]:
        tree = make_tree(values)
        tree.delete(deleted)
        assert tree.search(deleted) is False
        assert_avl(tree, set(values) - {deleted})


# В том числе случаи, когда баланс тяжёлого ребёнка равен нулю
def test_delete_rotations():
    for values, deleted, root in [
        ([5, 3, 6, 2], 6, 3),
        ([2, 1, 4, 5], 1, 4),
        ([5, 2, 6, 3], 6, 3),
        ([2, 1, 5, 3], 1, 3),
        ([5, 3, 6, 2, 4], 6, 3),
        ([3, 2, 5, 4, 6], 2, 5),
    ]:
        tree = make_tree(values)
        tree.delete(deleted)
        assert tree.root.value == root
        assert_avl(tree, set(values) - {deleted})


# Одно удаление вызывает повороты на двух уровнях
def test_delete_rebalances_multiple_ancestors():
    values = [12, 6, 16, 3, 9, 14, 17, 2, 4, 8, 10, 13, 1]
    tree = make_tree(values)
    assert tree.root.value == 12

    tree.delete(17)

    assert tree.root.value == 6
    assert_avl(tree, set(values) - {17})


def test_delete_missing_value_and_delete_twice():
    tree = make_tree([5, 3, 7])
    tree.delete(100)
    assert_avl(tree, [3, 5, 7])
    tree.delete(3)
    tree.delete(3)
    assert_avl(tree, [5, 7])


def test_reinsert_deleted_value():
    tree = make_tree([5, 3, 7])
    tree.delete(5)
    tree.insert(5)
    assert tree.search(5) is True
    assert_avl(tree, [3, 5, 7])


def test_zero_negative_and_large_values():
    values = [0, -5, 10 ** 100, -(10 ** 100), 7, -1]
    tree = make_tree(values)
    for value in values:
        assert tree.search(value) is True
    tree.delete(0)
    assert_avl(tree, set(values) - {0})


def test_string_values():
    tree = make_tree(["cat", "ant", "dog", "bee"])
    assert tree.search("bee") is True
    tree.delete("cat")
    assert_avl(tree, ["ant", "bee", "dog"])


def test_sorted_insertions_and_complete_deletion():
    for reverse in [False, True]:
        values = list(range(150))
        if reverse:
            values.reverse()
        tree = make_tree(values)
        expected = set(values)

        for value in values[::2] + values[1::2]:
            tree.delete(value)
            expected.remove(value)
            assert tree.search(value) is False
            assert_avl(tree, expected)
        assert tree.root is None


# Сравниваем смешанные операции с set, после каждого шага проверяем инварианты
def test_mixed_operations():
    for seed in [0, 7, 42, 123]:
        generator = random.Random(seed)
        tree = AVL()
        expected = set()

        for _ in range(500):
            value = generator.randrange(-50, 51)
            operation = generator.choice(["insert", "delete", "search"])
            if operation == "insert":
                tree.insert(value)
                expected.add(value)
            elif operation == "delete":
                tree.delete(value)
                expected.discard(value)
            else:
                assert tree.search(value) is (value in expected)
            assert_avl(tree, expected)


def test_independent_trees():
    first = make_tree([1, 2, 3])
    second = make_tree([10, 20, 30])
    first.delete(2)
    second.insert(40)

    assert_avl(first, [1, 3])
    assert_avl(second, [10, 20, 30, 40])
