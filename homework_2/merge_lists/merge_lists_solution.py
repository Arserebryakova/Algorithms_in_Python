from stack_vs_queue.stack_vs_queue_solution import Node


def merge_with_dummy(list1: Node | None, list2: Node | None) -> Node | None:
    dummy = Node(0)
    tail = dummy

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next

        tail = tail.next

    if list1 is not None:
        tail.next = list1
    else:
        tail.next = list2

    return dummy.next


def merge_without_dummy(list1: Node | None, list2: Node | None) -> Node | None:
    if list1 is None:
        return list2
    if list2 is None:
        return list1

    if list1.value <= list2.value:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next

    tail = head

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next

        tail = tail.next

    if list1 is not None:
        tail.next = list1
    else:
        tail.next = list2

    return head


if __name__ == "__main__":
    numbers1 = list(map(int, input().split()))
    numbers2 = list(map(int, input().split()))

    for merge in (merge_with_dummy, merge_without_dummy):
        # Для каждой функции создаём новые списки, потому что слияние меняет связи
        list1 = None
        for number in reversed(numbers1):
            list1 = Node(number, list1)

        list2 = None
        for number in reversed(numbers2):
            list2 = Node(number, list2)

        head = merge(list1, list2)

        result = []
        while head is not None:
            result.append(head.value)
            head = head.next

        print(f"{merge.__name__}: {result}")
