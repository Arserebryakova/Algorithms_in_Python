def max_even_arr_sum(numbers: list[int]) -> int:
    summ = 0
    min_odd = None

    for elem in numbers:
        summ += elem

        if elem % 2 != 0 and (min_odd is None or elem < min_odd):
            min_odd = elem

    if summ % 2 == 0:
        return summ

    return summ - min_odd


if __name__ == "__main__":
    numbers = list(map(int, input().split()))
    print(max_even_arr_sum(numbers))
