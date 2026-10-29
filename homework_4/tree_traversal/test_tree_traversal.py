from solution_tree_traversal import BST


# Все шесть обходов на дереве с несколькими уровнями
def test_all_traversals():
    tree = BST()
    for value in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        tree.insert(value)

    assert tree.preorder() == [8, 3, 1, 6, 4, 7, 10, 14, 13]
    assert tree.inorder() == [1, 3, 4, 6, 7, 8, 10, 13, 14]
    assert tree.postorder() == [1, 4, 7, 6, 3, 13, 14, 10, 8]
    assert tree.reverse_preorder() == [8, 10, 14, 13, 3, 6, 7, 4, 1]
    assert tree.reverse_inorder() == [14, 13, 10, 8, 7, 6, 4, 3, 1]
    assert tree.reverse_postorder() == [13, 14, 10, 7, 4, 6, 1, 3, 8]


# Пустое дерево
def test_empty_tree():
    tree = BST()

    assert tree.root is None
    assert tree.preorder() == []
    assert tree.inorder() == []
    assert tree.postorder() == []
    assert tree.reverse_preorder() == []
    assert tree.reverse_inorder() == []
    assert tree.reverse_postorder() == []


# Дерево из одного узла
def test_single_node():
    tree = BST()
    tree.insert(5)

    assert tree.preorder() == [5]
    assert tree.inorder() == [5]
    assert tree.postorder() == [5]
    assert tree.reverse_preorder() == [5]
    assert tree.reverse_inorder() == [5]
    assert tree.reverse_postorder() == [5]


# У корня есть только левый ребёнок
def test_only_left_child():
    tree = BST()
    tree.insert(5)
    tree.insert(3)

    assert tree.preorder() == [5, 3]
    assert tree.inorder() == [3, 5]
    assert tree.postorder() == [3, 5]
    assert tree.reverse_preorder() == [5, 3]
    assert tree.reverse_inorder() == [5, 3]
    assert tree.reverse_postorder() == [3, 5]


# У корня есть только правый ребёнок
def test_only_right_child():
    tree = BST()
    tree.insert(5)
    tree.insert(7)

    assert tree.preorder() == [5, 7]
    assert tree.inorder() == [5, 7]
    assert tree.postorder() == [7, 5]
    assert tree.reverse_preorder() == [5, 7]
    assert tree.reverse_inorder() == [7, 5]
    assert tree.reverse_postorder() == [7, 5]


# Первая вставка создаёт корень без детей
def test_insert_root():
    tree = BST()
    tree.insert(8)

    assert tree.root.value == 8
    assert tree.root.left is None
    assert tree.root.right is None


# Меньшие значения попадают влево, большие — вправо
def test_insert_structure():
    tree = BST()
    for value in [8, 3, 10, 1, 6, 9, 14]:
        tree.insert(value)

    assert tree.root.value == 8
    assert tree.root.left.value == 3
    assert tree.root.right.value == 10
    assert tree.root.left.left.value == 1
    assert tree.root.left.right.value == 6
    assert tree.root.right.left.value == 9
    assert tree.root.right.right.value == 14

    for node in [
        tree.root.left.left,
        tree.root.left.right,
        tree.root.right.left,
        tree.root.right.right,
    ]:
        assert node.left is None
        assert node.right is None


# При вставке сравниваем значение с узлами на всём пути
def test_insert_deeper_nodes():
    tree = BST()
    for value in [8, 3, 10, 6, 14, 4, 7, 13]:
        tree.insert(value)

    assert tree.root.left.right.left.value == 4
    assert tree.root.left.right.right.value == 7
    assert tree.root.right.right.left.value == 13
    assert tree.inorder() == [3, 4, 6, 7, 8, 10, 13, 14]


# Повторы корня, внутреннего узла и листа не добавляются
def test_duplicates():
    tree = BST()
    for value in [8, 3, 10, 1, 6, 8, 3, 1, 6, 10]:
        tree.insert(value)

    assert tree.preorder() == [8, 3, 1, 6, 10]
    assert tree.inorder() == [1, 3, 6, 8, 10]
    assert tree.postorder() == [1, 6, 3, 10, 8]
    assert tree.reverse_preorder() == [8, 10, 3, 6, 1]
    assert tree.reverse_inorder() == [10, 8, 6, 3, 1]
    assert tree.reverse_postorder() == [10, 6, 1, 3, 8]


# Если все значения одинаковые, остаётся один узел
def test_all_values_equal():
    tree = BST()
    for value in [5, 5, 5, 5]:
        tree.insert(value)

    assert tree.root.left is None
    assert tree.root.right is None
    assert tree.preorder() == [5]
    assert tree.inorder() == [5]
    assert tree.postorder() == [5]
    assert tree.reverse_preorder() == [5]
    assert tree.reverse_inorder() == [5]
    assert tree.reverse_postorder() == [5]


# Вставка по возрастанию: цепочка правых детей
def test_increasing_values():
    tree = BST()
    for value in [1, 2, 3, 4, 5]:
        tree.insert(value)

    current = tree.root
    for value in [1, 2, 3, 4, 5]:
        assert current.value == value
        assert current.left is None
        current = current.right
    assert current is None

    assert tree.preorder() == [1, 2, 3, 4, 5]
    assert tree.inorder() == [1, 2, 3, 4, 5]
    assert tree.postorder() == [5, 4, 3, 2, 1]
    assert tree.reverse_preorder() == [1, 2, 3, 4, 5]
    assert tree.reverse_inorder() == [5, 4, 3, 2, 1]
    assert tree.reverse_postorder() == [5, 4, 3, 2, 1]


# Вставка по убыванию: цепочка левых детей
def test_decreasing_values():
    tree = BST()
    for value in [5, 4, 3, 2, 1]:
        tree.insert(value)

    current = tree.root
    for value in [5, 4, 3, 2, 1]:
        assert current.value == value
        assert current.right is None
        current = current.left
    assert current is None

    assert tree.preorder() == [5, 4, 3, 2, 1]
    assert tree.inorder() == [1, 2, 3, 4, 5]
    assert tree.postorder() == [1, 2, 3, 4, 5]
    assert tree.reverse_preorder() == [5, 4, 3, 2, 1]
    assert tree.reverse_inorder() == [5, 4, 3, 2, 1]
    assert tree.reverse_postorder() == [1, 2, 3, 4, 5]


# Отрицательные числа, положительные числа и ноль
def test_negative_values_and_zero():
    tree = BST()
    for value in [0, -5, 4, -8, -2, 2, 7]:
        tree.insert(value)

    assert tree.preorder() == [0, -5, -8, -2, 4, 2, 7]
    assert tree.inorder() == [-8, -5, -2, 0, 2, 4, 7]
    assert tree.postorder() == [-8, -2, -5, 2, 7, 4, 0]
    assert tree.reverse_preorder() == [0, 4, 7, 2, -5, -2, -8]
    assert tree.reverse_inorder() == [7, 4, 2, 0, -2, -5, -8]
    assert tree.reverse_postorder() == [7, 2, 4, -2, -8, -5, 0]


# После обхода можно продолжать вставку
def test_insert_after_traversal():
    tree = BST()
    for value in [8, 3, 10]:
        tree.insert(value)

    previous_result = tree.inorder()
    tree.insert(6)
    tree.insert(9)

    assert previous_result == [3, 8, 10]
    assert tree.inorder() == [3, 6, 8, 9, 10]
    assert tree.root.left.right.value == 6
    assert tree.root.right.left.value == 9


# Каждый вызов возвращает новый список без накопления значений
def test_repeated_traversal_calls():
    tree = BST()
    for value in [8, 3, 10, 1, 6]:
        tree.insert(value)

    for traversal in [
        tree.preorder,
        tree.inorder,
        tree.postorder,
        tree.reverse_preorder,
        tree.reverse_inorder,
        tree.reverse_postorder,
    ]:
        first_result = traversal()
        second_result = traversal()

        assert first_result == second_result
        assert first_result is not second_result

        first_result.append(100)
        assert traversal() == second_result


# Обходы не меняют значения узлов и связи между ними
def test_traversals_preserve_tree():
    tree = BST()
    for value in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        tree.insert(value)

    root = tree.root
    nodes = [root]
    for node in nodes:
        if node.left is not None:
            nodes.append(node.left)
        if node.right is not None:
            nodes.append(node.right)

    original_state = [(node.value, node.left, node.right) for node in nodes]

    for traversal in [
        tree.preorder,
        tree.inorder,
        tree.postorder,
        tree.reverse_preorder,
        tree.reverse_inorder,
        tree.reverse_postorder,
    ]:
        traversal()

        assert tree.root is root
        for node, (value, left, right) in zip(nodes, original_state):
            assert node.value == value
            assert node.left is left
            assert node.right is right
