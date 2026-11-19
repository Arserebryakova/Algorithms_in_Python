from itertools import product
from random import Random

import pytest

import solution_kth as solution


def check_all_k(nums):
    original = nums.copy()
    for k, value in enumerate(sorted(nums, reverse=True), start=1):
        assert solution.find_kth_largest(nums, k) == value
        assert nums == original


def test_examples():
    assert solution.find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert solution.find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4


def test_boundaries_duplicates_and_negative_numbers():
    for nums in [
        [8], [2, 1], [1, 2], [4, 4, 4, 4],
        [-5, -1, -3, -1, 0], [3, 1, 3, 2, 2, 5],
        [10**50, 0, -10**50], list(range(30)), list(range(29, -1, -1)),
    ]:
        check_all_k(nums)


def test_exhaustive_small_arrays():
    for size in range(1, 6):
        for values in product((-1, 0, 1), repeat=size):
            check_all_k(list(values))


def test_random_arrays_and_all_ranks():
    random = Random(42)
    for _ in range(50):
        nums = [random.randint(-20, 20)
                for _ in range(random.randint(1, 60))]
        check_all_k(nums)


# Фиксируем индексы опорных, чтобы повторить пример из README.
def test_pivots_from_visualization(monkeypatch):
    indices = iter([2, 5, 5])
    monkeypatch.setattr(solution, "randrange", lambda left, stop: next(indices))
    assert solution.find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4


def test_extreme_pivots(monkeypatch):
    for choose in (lambda left, stop: left, lambda left, stop: stop - 1):
        monkeypatch.setattr(solution, "randrange", choose)
        for nums in (list(range(80)), list(range(79, -1, -1)), [1, 3, 2] * 20):
            check_all_k(nums)


def test_many_equal_values():
    assert solution.find_kth_largest([7] * 10000, 5000) == 7


def test_invalid_k_and_empty_input():
    for nums, k in (([], 1), ([], 0), ([1], 0), ([1], 2), ([1, 2], -1)):
        with pytest.raises(ValueError):
            solution.find_kth_largest(nums, k)


def test_k_must_be_an_integer():
    for k in (1.0, "1", None, True, False):
        with pytest.raises(TypeError):
            solution.find_kth_largest([1, 2, 3], k)
