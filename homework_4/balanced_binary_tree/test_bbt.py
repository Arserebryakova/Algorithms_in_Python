from balanced_binary_tree.solution_bbt import Node, is_balanced


# Пустое дерево сбалансировано
def test_empty_tree():
    assert is_balanced(None) is True


# Один узел без детей
def test_single_node():
    assert is_balanced(Node(5)) is True


# Один левый ребёнок: разница высот равна 1
def test_only_left_child():
    root = Node(5)
    root.left = Node(3)

    assert is_balanced(root) is True


# Один правый ребёнок: разница высот равна 1
def test_only_right_child():
    root = Node(5)
    root.right = Node(7)

    assert is_balanced(root) is True


# Цепочка из трёх узлов влево: у корня разница высот равна 2
def test_three_nodes_on_left():
    root = Node(3)
    root.left = Node(2)
    root.left.left = Node(1)

    assert is_balanced(root) is False


# Цепочка из трёх узлов вправо
def test_three_nodes_on_right():
    root = Node(1)
    root.right = Node(2)
    root.right.right = Node(3)

    assert is_balanced(root) is False


# Полностью заполненное дерево из семи узлов
def test_perfect_tree():
    root = Node(4)
    root.left = Node(2)
    root.right = Node(6)
    root.left.left = Node(1)
    root.left.right = Node(3)
    root.right.left = Node(5)
    root.right.right = Node(7)

    assert is_balanced(root) is True


# Высоты могут отличаться на 1, симметрия не требуется
def test_balanced_tree_with_different_heights():
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.right = Node(4)

    assert is_balanced(root) is True


# У корня разница высот 1, но левое поддерево несбалансировано
def test_unbalanced_left_subtree():
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.left.left = Node(5)
    root.right.right = Node(6)

    assert is_balanced(root) is False


# Нарушение баланса внутри правого поддерева
def test_unbalanced_right_subtree():
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.right.right = Node(5)
    root.right.right.right = Node(6)

    assert is_balanced(root) is False


# Чередование левых и правых детей тоже может образовать цепочку
def test_zigzag_chain():
    root = Node(1)
    root.left = Node(2)
    root.left.right = Node(3)
    root.left.right.left = Node(4)

    assert is_balanced(root) is False


# Одинаковые значения не влияют на баланс высот
def test_duplicate_values():
    root = Node(5)
    root.left = Node(5)
    root.right = Node(5)

    assert is_balanced(root) is True


# Дерево не обязано быть BST
def test_balanced_tree_that_is_not_bst():
    root = Node(0)
    root.left = Node(10)
    root.right = Node(-10)

    assert is_balanced(root) is True


# Баланс зависит от структуры, а не от величины значений
def test_large_and_negative_values():
    root = Node(-(10 ** 400))
    root.left = Node(0)
    root.right = Node(10 ** 400)
    root.right.left = Node(-1)

    assert is_balanced(root) is True


# Длинная цепочка
def test_long_chain():
    root = Node(0)
    current = root
    for value in range(1, 200):
        current.right = Node(value)
        current = current.right

    assert is_balanced(root) is False


# Большое полностью заполненное дерево: 255 узлов
def test_large_perfect_tree():
    root = Node(0)
    level = [root]
    for _ in range(7):
        next_level = []
        for node in level:
            node.left = Node(0)
            node.right = Node(0)
            next_level.extend([node.left, node.right])
        level = next_level

    assert is_balanced(root) is True


# Повторные проверки независимы друг от друга
def test_repeated_calls():
    balanced_root = Node(1)
    balanced_root.left = Node(2)
    unbalanced_root = Node(1)
    unbalanced_root.right = Node(2)
    unbalanced_root.right.right = Node(3)

    assert is_balanced(balanced_root) is True
    assert is_balanced(unbalanced_root) is False
    assert is_balanced(balanced_root) is True
    assert is_balanced(None) is True


# Сохраняем значения и связи и для True, и для False
def test_preserves_tree():
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    nodes = [root, root.left, root.right, root.left.left]

    for expected_result in [True, False]:
        original_state = [(node.value, node.left, node.right) for node in nodes]

        assert is_balanced(root) is expected_result
        for node, (value, left, right) in zip(nodes, original_state):
            assert node.value == value
            assert node.left is left
            assert node.right is right

        if expected_result is True:
            root.left.left.left = Node(5)
            nodes.append(root.left.left.left)
