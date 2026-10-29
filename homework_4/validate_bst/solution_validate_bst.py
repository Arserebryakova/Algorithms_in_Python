class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def is_valid_bst(root):
    def validate(node, lower, upper):
        if node is None:
            return True

        if lower is not None and node.value <= lower:
            return False

        if upper is not None and node.value >= upper:
            return False
        return (
            validate(node.left, lower, node.value)
            and validate(node.right, node.value, upper)
        )
    return validate(root, None, None)
