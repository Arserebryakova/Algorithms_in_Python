def palindrome_check(n: int) -> bool:
    initial_n = n
    reversed_n = 0

    while n > 0:
        reversed_n = reversed_n * 10 + n % 10
        n //= 10

    return initial_n == reversed_n


if __name__ == "__main__":
    n = int(input())
    print(palindrome_check(n))
