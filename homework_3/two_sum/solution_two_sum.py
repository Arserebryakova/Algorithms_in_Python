def two_sum(arr: list[int], k: int) -> tuple[int, int]:
    """Возвращает индексы единственной существующей пары с суммой k."""
    seen = {}
    for index, number in enumerate(arr):
        needed = k - number
        # Проверка до вставки исключает повторное использование элемента.
        if needed in seen:
            return seen[needed], index
        seen[number] = index


if __name__ == "__main__":
    arr = list(map(int, input().split()))
    k = int(input())

    first_index, second_index = two_sum(arr, k)
    print(first_index, second_index)
