from itertools import product
from random import Random

from solution_iterative import merge_sort, quick_sort


def check_sorts(nums):
    original = nums.copy()
    for algorithm in (merge_sort, quick_sort):
        result = algorithm(nums)
        assert result == sorted(original)
        assert nums == original
        assert result is not nums


def test_examples_and_boundaries():
    for nums in [
        [], [7], [1, 2], [2, 1], [2, 2],
        [7, 2, 5, 2, 9, 1, 4], [3, -1, 0, -1, 8],
        [10**50, -10**50, 0], [2, 1, 2, 1, 2, 0],
        list(range(31)), list(range(30, -1, -1)), [5] * 100,
    ]:
        check_sorts(nums)


def test_exhaustive_small_arrays():
    for size in range(7):
        for values in product((-1, 0, 1), repeat=size):
            check_sorts(list(values))


# Последний блок mergesort может быть короче остальных.
def test_lengths_around_powers_of_two():
    random = Random(13)
    for size in (3, 5, 7, 8, 9, 15, 16, 17, 63, 64, 65, 127, 128, 129):
        nums = list(range(size))
        random.shuffle(nums)
        check_sorts(nums)


def test_random_arrays():
    random = Random(42)
    for _ in range(80):
        nums = [random.randint(-50, 50)
                for _ in range(random.randrange(301))]
        check_sorts(nums)


def test_long_sorted_and_equal_arrays():
    check_sorts(list(range(1800)))
    check_sorts(list(range(1799, -1, -1)))
    check_sorts([4] * 10000)


def test_merge_sort_is_stable():
    class Item:
        def __init__(self, key, label):
            self.key, self.label = key, label

        def __le__(self, other):
            return self.key <= other.key

    nums = [Item(2, "a"), Item(1, "b"), Item(2, "c"), Item(1, "d")]
    assert [item.label for item in merge_sort(nums)] == ["b", "d", "a", "c"]
