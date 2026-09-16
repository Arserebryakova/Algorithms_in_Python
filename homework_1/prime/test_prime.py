from prime import count_primes_before_n


def test_count_primes():
    assert count_primes_before_n(-10) == 0  # negative input
    assert count_primes_before_n(0) == 0  # no primes below 0
    assert count_primes_before_n(1) == 0  # example from the task
    assert count_primes_before_n(2) == 0  # no primes strictly less than 2
    assert count_primes_before_n(3) == 1  # only 2 is less than 3
    assert count_primes_before_n(4) == 2  # 2, 3

    assert count_primes_before_n(10) == 4  # 2, 3, 5, 7
    assert count_primes_before_n(11) == 4  # n itself is prime but must not be counted
    assert count_primes_before_n(12) == 5  # 2, 3, 5, 7, 11

    assert count_primes_before_n(26) == 9  # 25 is inside the range and must be marked composite
    assert count_primes_before_n(30) == 10  # several primes and composites
    assert count_primes_before_n(50) == 15  # checks that 49 = 7^2 is marked composite

    assert count_primes_before_n(100) == 25  # larger input
    assert count_primes_before_n(5000) == 669  # large input, checked against another C++ implementation
