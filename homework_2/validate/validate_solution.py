from stack_vs_queue.stack_vs_queue_solution import Stack


def validate(pushed: list[int], popped: list[int]) -> bool:
    stack = Stack()
    j = 0

    for elem in pushed:
        stack.push(elem)

        while stack.top is not None and stack.top.value == popped[j]:
            stack.pop()
            j += 1

    return j == len(popped)


if __name__ == "__main__":
    pushed = list(map(int, input().split()))
    popped = list(map(int, input().split()))

    print(validate(pushed, popped))
