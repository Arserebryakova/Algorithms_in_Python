from itertools import product
from random import Random

import pytest

import solution_compare as solution
from benchmark import benchmark


def check_sorts(nums):
    original = nums.copy()
    for algorithm in (solution.merge_sort, solution.quick_sort):
        result = algorithm(nums)
        assert result == sorted(original)
        assert nums == original
        assert result is not nums


def test_examples_and_boundaries():
    for nums in [
        [], [4], [1, 2], [2, 1], [1, 1],
        [7, 2, 5, 2, 9, 1, 4], [-5, 0, -2, 8, -5],
        [2, 1, 2, 1, 2, 0], [10**50, -10**50, 0],
        list(range(31)), list(range(30, -1, -1)), [7] * 100,
    ]:
        check_sorts(nums)


def test_exhaustive_small_arrays():
    for size in range(7):
        for values in product((-1, 0, 1), repeat=size):
            check_sorts(list(values))


def test_random_arrays():
    random = Random(42)
    for _ in range(80):
        nums = [random.randint(-100, 100)
                for _ in range(random.randrange(301))]
        check_sorts(nums)


# Неудачные опорные не приводят к переполнению стека рекурсии.
def test_long_sorted_arrays():
    check_sorts(list(range(1800)))
    check_sorts(list(range(1799, -1, -1)))


def test_many_equal_values():
    check_sorts([3] * 10000)


def test_merge_sort_is_stable():
    class Item:
        def __init__(self, key, label):
            self.key, self.label = key, label

        def __le__(self, other):
            return self.key <= other.key

    nums = [Item(2, "a"), Item(1, "b"), Item(2, "c"), Item(1, "d")]
    assert [item.label for item in solution.merge_sort(nums)] == [
        "b", "d", "a", "c"
    ]


def test_timer_arguments_result_and_time(monkeypatch, capsys):
    @solution.timer
    def combine(first, second=0, *, scale=1):
        return (first + second) * scale

    assert combine.last_elapsed is None
    moments = iter([10.0, 10.25])
    monkeypatch.setattr(solution, "perf_counter", lambda: next(moments))

    assert combine(2, second=3, scale=4) == 20
    assert combine.last_elapsed == 0.25
    assert capsys.readouterr().out == "combine: 0.250000 s\n"


def test_timer_preserves_metadata():
    def original(value):
        """Возвращает переданное значение."""
        return value

    decorated = solution.timer(original)
    assert decorated.__name__ == original.__name__
    assert decorated.__doc__ == original.__doc__
    assert decorated.__wrapped__ is original


def test_timer_preserves_exception(monkeypatch, capsys):
    error = ValueError("stop")

    @solution.timer
    def fail():
        raise error

    moments = iter([1.0, 1.5])
    monkeypatch.setattr(solution, "perf_counter", lambda: next(moments))
    with pytest.raises(ValueError) as caught:
        fail()

    assert caught.value is error
    assert fail.last_elapsed == 0.5
    assert capsys.readouterr().out == "fail: 0.500000 s\n"


def test_timer_repeated_calls(monkeypatch, capsys):
    first = solution.timer(lambda: None)
    second = solution.timer(lambda: "ok")
    moments = iter([0, 1, 2, 4, 5, 8])
    monkeypatch.setattr(solution, "perf_counter", lambda: next(moments))

    assert first() is None
    assert second() == "ok"
    assert first() is None
    assert first.last_elapsed == 3
    assert second.last_elapsed == 2
    assert len(capsys.readouterr().out.splitlines()) == 3


# Время зависит от окружения, поэтому проверяем запуск, а не соотношение времён.
def test_benchmark():
    rows = benchmark(size=20, repeats=2)
    assert len(rows) == 5
    for row in rows:
        assert row["merge_seconds"] >= 0
        assert row["quick_seconds"] >= 0
