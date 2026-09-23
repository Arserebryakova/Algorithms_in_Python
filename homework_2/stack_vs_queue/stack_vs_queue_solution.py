from __future__ import annotations


class Node:
    def __init__(self, value: int, next: Node | None = None):
        self.value = value
        self.next = next


class Stack:
    def __init__(self):
        self.top: Node | None = None

    def push(self, value: int) -> None:
        new_node = Node(value, self.top)
        self.top = new_node

    def pop(self) -> int:
        if self.top is None:
            raise IndexError("Stack is empty")

        value = self.top.value
        self.top = self.top.next

        return value


class Queue:
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None

    def enqueue(self, value: int) -> None:
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self) -> int:
        if self.head is None:
            raise IndexError("Queue is empty")

        value = self.head.value
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        return value


if __name__ == "__main__":
    numbers = list(map(int, input().split()))

    stack = Stack()
    queue = Queue()

    for number in numbers:
        stack.push(number)
        queue.enqueue(number)

    stack_result = []
    while stack.top is not None:
        stack_result.append(stack.pop())

    queue_result = []
    while queue.head is not None:
        queue_result.append(queue.dequeue())

    print("Стек:", *stack_result)
    print("Очередь:", *queue_result)
