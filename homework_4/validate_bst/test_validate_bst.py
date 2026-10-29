from solution_validate_bst import Node, is_valid_bst


# Пустое дерево является корректным BST
def test_empty_tree():
    assert is_valid_bst(None) is True


# Один узел без детей
def test_single_node():
    assert is_valid_bst(Node(5)) is True


# Корректное дерево с несколькими уровнями
def test_valid_tree():
    root = Node(8)
    root.left = Node(3)
    root.right = Node(10)
    root.left.left = Node(1)
    root.left.right = Node(6)
    root.left.right.left = Node(4)
    root.left.right.right = Node(7)
    root.right.right = Node(14)
    root.right.right.left = Node(13)

    assert is_valid_bst(root) is True


# У корня только левый ребёнок
def test_only_left_child():
    root = Node(5)
    root.left = Node(3)

    assert is_valid_bst(root) is True


# У корня только правый ребёнок
def test_only_right_child():
    root = Node(5)
    root.right = Node(7)

    assert is_valid_bst(root) is True


# Левый ребёнок больше родителя
def test_invalid_left_child():
    root = Node(5)
    root.left = Node(7)

    assert is_valid_bst(root) is False


# Правый ребёнок меньше родителя
def test_invalid_right_child():
    root = Node(5)
    root.right = Node(3)

    assert is_valid_bst(root) is False


# Повтор значения слева
def test_duplicate_on_left():
    root = Node(5)
    root.left = Node(5)

    assert is_valid_bst(root) is False


# Повтор значения справа
def test_duplicate_on_right():
    root = Node(5)
    root.right = Node(5)

    assert is_valid_bst(root) is False


# Повтор значения предка, а не непосредственного родителя
def test_duplicate_ancestor():
    root = Node(10)
    root.right = Node(15)
    root.right.left = Node(10)

    assert is_valid_bst(root) is False


# Узел 6 меньше родителя 15, но нарушает нижнюю границу 10
def test_invalid_value_in_right_subtree():
    root = Node(10)
    root.left = Node(5)
    root.right = Node(15)
    root.right.left = Node(6)
    root.right.right = Node(20)

    assert is_valid_bst(root) is False


# Узел 12 больше родителя 5, но нарушает верхнюю границу 10
def test_invalid_value_in_left_subtree():
    root = Node(10)
    root.left = Node(5)
    root.right = Node(15)
    root.left.right = Node(12)

    assert is_valid_bst(root) is False


# Ограничение корня сохраняется через несколько уровней
def test_deep_violation():
    root = Node(20)
    root.left = Node(10)
    root.left.right = Node(15)
    root.left.right.right = Node(25)

    assert is_valid_bst(root) is False


# Отрицательные значения и ноль
def test_negative_values_and_zero():
    root = Node(0)
    root.left = Node(-5)
    root.right = Node(7)
    root.left.left = Node(-8)
    root.left.right = Node(-2)
    root.right.left = Node(3)

    assert is_valid_bst(root) is True


# Ноль тоже должен учитываться как граница
def test_zero_boundary():
    root = Node(0)
    root.right = Node(5)
    root.right.left = Node(-1)

    assert is_valid_bst(root) is False


# Для значений не задаём искусственное ограничение на размер
def test_large_integer_values():
    value = 10 ** 400
    root = Node(value)
    root.left = Node(-value)
    root.right = Node(value + 1)

    assert is_valid_bst(root) is True


# Корректная цепочка правых детей
def test_increasing_chain():
    root = Node(0)
    current = root
    for value in range(1, 200):
        current.right = Node(value)
        current = current.right

    assert is_valid_bst(root) is True


# Корректная цепочка левых детей
def test_decreasing_chain():
    root = Node(200)
    current = root
    for value in range(199, 0, -1):
        current.left = Node(value)
        current = current.left

    assert is_valid_bst(root) is True


# Результат предыдущей проверки не влияет на следующую
def test_repeated_calls():
    valid_root = Node(5)
    valid_root.left = Node(3)
    invalid_root = Node(5)
    invalid_root.right = Node(3)

    assert is_valid_bst(valid_root) is True
    assert is_valid_bst(invalid_root) is False
    assert is_valid_bst(valid_root) is True
    assert is_valid_bst(None) is True


# Проверка сохраняет значения и связи даже при обнаружении ошибки
def test_preserves_tree():
    root = Node(10)
    root.left = Node(5)
    root.right = Node(15)
    root.right.left = Node(6)
    nodes = [root, root.left, root.right, root.right.left]
    original_state = [(node.value, node.left, node.right) for node in nodes]

    assert is_valid_bst(root) is False
    for node, (value, left, right) in zip(nodes, original_state):
        assert node.value == value
        assert node.left is left
        assert node.right is right
