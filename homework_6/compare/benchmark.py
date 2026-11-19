from contextlib import redirect_stdout
from io import StringIO
from random import Random
from statistics import median

from solution_compare import merge_sort, quick_sort, timer


def make_cases(size, seed=42):
    random = Random(seed)
    shuffled = list(range(size))
    random.shuffle(shuffled)
    return {
        "random_distinct": shuffled,
        "ascending": list(range(size)),
        "descending": list(range(size - 1, -1, -1)),
        "all_equal": [7] * size,
        "few_unique": [random.randrange(5) for _ in range(size)],
    }


def benchmark(size=3000, repeats=5):
    if size < 1 or repeats < 1:
        raise ValueError("size и repeats должны быть положительными")
    algorithms = [timer(merge_sort), timer(quick_sort)]
    rows = []
    for name, nums in make_cases(size).items():
        expected = sorted(nums)  # Эталон считаем вне замера.
        samples = [[], []]
        for algorithm in algorithms:
            with redirect_stdout(StringIO()):
                result = algorithm(nums)  # Прогрев, в медиану не входит.
            assert result == expected

        for repeat in range(repeats):
            # Чередуем порядок, чтобы один алгоритм не всегда был первым.
            order = (0, 1) if repeat % 2 == 0 else (1, 0)
            for index in order:
                with redirect_stdout(StringIO()):
                    result = algorithms[index](nums)
                samples[index].append(algorithms[index].last_elapsed)
                assert result == expected

        merge_seconds, quick_seconds = map(median, samples)
        rows.append({
            "case": name,
            "n": size,
            "repeats": repeats,
            "merge_seconds": merge_seconds,
            "quick_seconds": quick_seconds,
            "quick_div_merge": quick_seconds / merge_seconds,
        })
    return rows


if __name__ == "__main__":
    rows = benchmark(size=3000, repeats=5)
    print("case                 n    merge, ms    quick, ms    quick / merge")
    for row in rows:
        print(f"{row['case']:18} {row['n']:5} "
              f"{row['merge_seconds'] * 1000:12.3f} "
              f"{row['quick_seconds'] * 1000:12.3f} "
              f"{row['quick_div_merge']:16.2f}")
