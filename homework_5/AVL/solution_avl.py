class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    def __init__(self):
        self.root = None

    def _height(self, node):
        if node is None:
            return 0
        return node.height

    def _update_height(self, node):
        node.height = (
            max(self._height(node.left), self._height(node.right)) + 1
        )

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, node):
        new_root = node.left
        middle = new_root.right

        new_root.right = node
        node.left = middle

        # Сначала обновляем бывший корень, затем новый.
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_left(self, node):
        new_root = node.right
        middle = new_root.left

        new_root.left = node
        node.right = middle

        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rebalance(self, node):
        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return Node(value)

        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node

        return self._rebalance(node)

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Минимальный узел справа заменяет удаляемое значение.
            successor = node.right
            while successor.left is not None:
                successor = successor.left

            node.value = successor.value
            node.right = self._delete(node.right, successor.value)

        return self._rebalance(node)

    def search(self, value):
        current = self.root

        while current is not None:
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return True

        return False

    def inorder(self):
        result = []

        def traverse(node):
            if node is None:
                return

            traverse(node.left)
            result.append(node.value)
            traverse(node.right)

        traverse(self.root)
        return result
