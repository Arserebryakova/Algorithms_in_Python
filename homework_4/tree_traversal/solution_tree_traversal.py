class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            return

        current = self.root

        while True:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return
                current = current.left

            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    return
                current = current.right

            else:
                return

    def preorder(self):
        result = []

        def traverse(node):
            if node is None:
                return

            result.append(node.value)
            traverse(node.left)
            traverse(node.right)

        traverse(self.root)
        return result

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

    def postorder(self):
        result = []

        def traverse(node):
            if node is None:
                return

            traverse(node.left)
            traverse(node.right)
            result.append(node.value)

        traverse(self.root)
        return result

    def reverse_preorder(self):
        result = []

        def traverse(node):
            if node is None:
                return

            result.append(node.value)
            traverse(node.right)
            traverse(node.left)

        traverse(self.root)
        return result

    def reverse_inorder(self):
        result = []

        def traverse(node):
            if node is None:
                return

            traverse(node.right)
            result.append(node.value)
            traverse(node.left)

        traverse(self.root)
        return result

    def reverse_postorder(self):
        result = []

        def traverse(node):
            if node is None:
                return
            traverse(node.right)
            traverse(node.left)
            result.append(node.value)

        traverse(self.root)
        return result
