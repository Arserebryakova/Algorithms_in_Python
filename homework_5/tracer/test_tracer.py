import inspect

import pytest

from solution_tracer import tracer


# Вход и возврат находятся на одной глубине, результат не меняется
def test_recursive_factorial(capsys):
    @tracer
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    assert factorial(3) == 6
    assert capsys.readouterr().out.splitlines() == [
        "-> factorial(3)",
        "  -> factorial(2)",
        "    -> factorial(1)",
        "    <- factorial = 1",
        "  <- factorial = 2",
        "<- factorial = 6",
    ]


# После возврата из одной ветки соседняя начинается на той же глубине
def test_branching_recursion(capsys):
    @tracer
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    assert fibonacci(3) == 2
    assert capsys.readouterr().out.splitlines() == [
        "-> fibonacci(3)",
        "  -> fibonacci(2)",
        "    -> fibonacci(1)",
        "    <- fibonacci = 1",
        "    -> fibonacci(0)",
        "    <- fibonacci = 0",
        "  <- fibonacci = 1",
        "  -> fibonacci(1)",
        "  <- fibonacci = 1",
        "<- fibonacci = 2",
    ]


def test_no_arguments_and_none_result(capsys):
    @tracer
    def empty():
        return None

    assert empty() is None
    assert capsys.readouterr().out == "-> empty()\n<- empty = None\n"


def test_positional_and_keyword_arguments(capsys):
    @tracer
    def combine(first, second=0, *, scale=1):
        return (first + second) * scale

    assert combine(2, second=3, scale=4) == 20
    assert capsys.readouterr().out == (
        "-> combine(2, second=3, scale=4)\n<- combine = 20\n"
    )


def test_variable_arguments(capsys):
    @tracer
    def collect(*args, **kwargs):
        return args, kwargs

    assert collect(1, 2, name="cat") == ((1, 2), {"name": "cat"})
    assert capsys.readouterr().out.splitlines()[0] == (
        "-> collect(1, 2, name='cat')"
    )


def test_different_arguments_and_results(capsys):
    for value in [None, False, 0, "", "a\nb", [1, 2], {"x": 3}]:
        @tracer
        def identity(item):
            return item

        assert identity(value) is value
        assert capsys.readouterr().out.splitlines() == [
            f"-> identity({value!r})",
            f"<- identity = {value!r}",
        ]


def test_preserves_function_metadata():
    def original(n: int, offset=1) -> int:
        """Возвращает сумму."""
        return n + offset

    decorated = tracer(original)

    assert decorated.__name__ == original.__name__
    assert decorated.__doc__ == original.__doc__
    assert decorated.__annotations__ == original.__annotations__
    assert decorated.__wrapped__ is original
    assert inspect.signature(decorated) == inspect.signature(original)


# Ошибка проходит через весь стек, следующий запуск начинается без отступа
def test_exception_propagates_and_depth_resets(capsys):
    error = ValueError("stop")

    @tracer
    def countdown(n, fail=False):
        if n == 0:
            if fail:
                raise error
            return 0
        return countdown(n - 1, fail=fail)

    with pytest.raises(ValueError) as caught:
        countdown(2, fail=True)

    assert caught.value is error
    assert capsys.readouterr().out.splitlines()[-3:] == [
        "    <! countdown raises ValueError('stop')",
        "  <! countdown raises ValueError('stop')",
        "<! countdown raises ValueError('stop')",
    ]
    assert countdown(0) == 0
    assert capsys.readouterr().out == "-> countdown(0)\n<- countdown = 0\n"


# Перехват ошибки внутри рекурсии не нарушает глубину следующей ветки
def test_caught_exception_inside_recursion(capsys):
    @tracer
    def visit(n):
        if n < 0:
            raise ValueError("negative")
        if n == 0:
            return 0
        try:
            visit(-1)
        except ValueError:
            return visit(0)

    assert visit(1) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[1] == "  -> visit(-1)"
    assert lines[3] == "  -> visit(0)"
    assert lines[-1] == "<- visit = 0"


def test_repeated_calls(capsys):
    @tracer
    def countdown(n):
        if n == 0:
            return 0
        return countdown(n - 1)

    for _ in range(3):
        assert countdown(2) == 0
        lines = capsys.readouterr().out.splitlines()
        assert lines[0] == "-> countdown(2)"
        assert lines[-1] == "<- countdown = 0"


# У разных декорированных функций собственные счётчики
def test_independent_decorators(capsys):
    @tracer
    def first(n):
        if n == 0:
            return 1
        return first(n - 1)

    @tracer
    def second():
        return 2

    assert first(2) == 1
    assert second() == 2
    assert capsys.readouterr().out.splitlines()[-2:] == [
        "-> second()", "<- second = 2"
    ]
