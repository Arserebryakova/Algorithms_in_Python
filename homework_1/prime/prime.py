def count_primes_before_n(n: int) -> int:  # sieve of eratosthenes
    if n <= 2:
        return 0

    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False

    p = 2

    while p * p < n:
        if is_prime[p]:
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False

        p += 1

    return sum(is_prime)


if __name__ == "__main__":
    n = int(input())
    print(count_primes_before_n(n))
