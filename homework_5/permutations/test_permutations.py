from itertools import permutations as reference_permutations
from math import factorial

from solution_permutations import permutations


def test_examples_and_empty_list():
    for nums, expected in [
        ([1, 2, 3], [
            [1, 2, 3], [1, 3, 2], [2, 1, 3],
            [2, 3, 1], [3, 1, 2], [3, 2, 1],
        ]),
        ([0, 1], [[0, 1], [1, 0]]),
        ([1], [[1]]),
        ([], [[]]),
    ]:
        assert permutations(nums, trace=False) == expected


# Порядок выбора соответствует первому появлению значений во входном списке
def test_unsorted_input():
    assert permutations([2, 1, 3], trace=False) == [
        [2, 1, 3], [2, 3, 1], [1, 2, 3],
        [1, 3, 2], [3, 2, 1], [3, 1, 2],
    ]


def test_matches_standard_library():
    for nums in [
        [-2, 0, 3], [4, 3, 2, 1], [0, 1, 2, 3, 4],
        [1, 1, 2], [2, 1, 2, 1], [0, 0, 0], [3, 1, 3, 2],
    ]:
        expected = set(reference_permutations(nums))
        result = permutations(nums, trace=False)

        assert {tuple(row) for row in result} == expected
        assert len(result) == len(expected)


def test_duplicate_values():
    assert permutations([1, 1, 2], trace=False) == [
        [1, 1, 2], [1, 2, 1], [2, 1, 1]
    ]


def test_all_values_equal():
    assert permutations([7] * 20, trace=False) == [[7] * 20]


def test_six_distinct_values():
    nums = list(range(6))
    result = permutations(nums, trace=False)

    assert len(result) == factorial(6)
    assert len({tuple(row) for row in result}) == factorial(6)
    assert all(sorted(row) == nums for row in result)


def test_preserves_input(capsys):
    for trace in [True, False]:
        nums = [3, 1, 3, 2]
        original = nums.copy()

        permutations(nums, trace=trace)

        assert nums == original


# Каждая перестановка хранится в отдельном списке
def test_result_lists_are_independent():
    nums = [1, 2, 3]
    result = permutations(nums, trace=False)
    result[0][0] = 100

    assert result[1] == [1, 3, 2]
    assert nums == [1, 2, 3]
    assert len({id(row) for row in result}) == 6


def test_repeated_calls_are_independent():
    first = permutations([1, 2], trace=False)
    assert permutations([], trace=False) == [[]]
    assert permutations([3], trace=False) == [[3]]
    second = permutations([1, 2], trace=False)

    assert first == second
    assert first is not second
    assert first[0] is not second[0]


# По умолчанию используется tracer: видны пути, глубина и возвраты
def test_trace_is_enabled_by_default(capsys):
    assert permutations([1, 2]) == [[1, 2], [2, 1]]
    assert capsys.readouterr().out.splitlines() == [
        "-> backtrack([])",
        "  -> backtrack([1])",
        "    -> backtrack([1, 2])",
        "    <- backtrack = None",
        "  <- backtrack = None",
        "  -> backtrack([2])",
        "    -> backtrack([2, 1])",
        "    <- backtrack = None",
        "  <- backtrack = None",
        "<- backtrack = None",
    ]


def test_empty_input_trace(capsys):
    assert permutations([]) == [[]]
    assert capsys.readouterr().out == (
        "-> backtrack([])\n<- backtrack = None\n"
    )


def test_trace_can_be_disabled(capsys):
    assert permutations([0, 1], trace=False) == [[0, 1], [1, 0]]
    assert capsys.readouterr().out == ""


def test_trace_does_not_change_result(capsys):
    nums = [1, 1, 2]
    assert permutations(nums) == permutations(nums, trace=False)
    assert capsys.readouterr().out.count("-> backtrack([])") == 1
