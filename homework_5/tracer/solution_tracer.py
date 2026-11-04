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


if __name__ == "__main__":
    @tracer
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    factorial(4)
