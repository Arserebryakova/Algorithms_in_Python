class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def is_balanced(root):
    def height(node):
        if node is None:
            return 0

        left_height = height(node.left)
        if left_height == -1:
            return -1

        right_height = height(node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1
        return max(left_height, right_height) + 1
    return height(root) != -1
