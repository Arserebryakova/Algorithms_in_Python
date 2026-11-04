from functools import wraps


def _format_call(func, args, kwargs):
    arguments = [repr(value) for value in args]
    arguments.extend(f"{key}={value!r}" for key, value in kwargs.items())
    return f"{func.__name__}({', '.join(arguments)})"


def tracer(func):
    depth = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal depth

        print(f"{'  ' * depth}-> {_format_call(func, args, kwargs)}")
        depth += 1

        try:
            result = func(*args, **kwargs)
        except Exception as error:
            print(f"{'  ' * (depth - 1)}<! {func.__name__} raises {error!r}")
            raise
        else:
            print(f"{'  ' * (depth - 1)}<- {func.__name__} = {result!r}")
            return result
        finally:
            # Восстанавливаем глубину и при возврате, и при исключении.
            depth -= 1

    return wrapper



def permutations(nums, trace=True):
    result = []
    counts = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path.copy())
            return

        for value in counts:
            if counts[value] == 0:
                continue

            path.append(value)
            counts[value] -= 1
            backtrack(path)
            # Возвращаем состояние перед выбором следующего значения.
            counts[value] += 1
            path.pop()

    if trace:
        backtrack = tracer(backtrack)

    backtrack([])
    return result


if __name__ == "__main__":
    print(permutations([1, 2, 3]))
