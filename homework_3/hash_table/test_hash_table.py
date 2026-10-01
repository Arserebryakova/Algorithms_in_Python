import pytest

from solution_hash_table import HashTable


def test_nan_key():
    # Один и тот же объект NaN остаётся доступен, хотя он не равен себе.
    table = HashTable()
    key = float("nan")
    table.insert(key, "initial")
    assert table.get(key) == "initial"

    for number in range(10):
        table.insert(number, number)
    assert table.get(key) == "initial"

    table.insert(key, "updated")
    assert table.get(key) == "updated"
    assert table.size == 11

    table.delete(key)
    assert table.size == 10
    with pytest.raises(KeyError):
        table.get(key)


def test_equal_keys_of_different_types():
    # Равные ключи с одинаковым хешем обозначают одну запись.
    table = HashTable()
    table.insert(1, "initial")
    table.insert(1.0, "updated")

    assert table.get(True) == "updated"
    assert table.size == 1
    table.delete(1.0)
    assert table.size == 0


@pytest.mark.parametrize("operation", ["insert", "get", "delete"])
def test_unhashable_key(operation):
    # Нехешируемый ключ отклоняется без изменения существующих данных.
    table = HashTable()
    table.insert("saved", 42)

    with pytest.raises(TypeError):
        if operation == "insert":
            table.insert([], 10)
        else:
            getattr(table, operation)([])

    assert table.size == 1
    assert table.get("saved") == 42


def test_same_hash_after_resize():
    # У -1 и -2 одинаковые хеши: расширение не устраняет эту коллизию.
    table = HashTable(capacity=1)
    table.insert(-1, "first")
    table.insert(-2, "second")
    for number in range(20):
        table.insert(number, number)

    assert table.get(-1) == "first"
    assert table.get(-2) == "second"
    table.insert(-2, "updated")
    table.delete(-1)
    assert table.get(-2) == "updated"
    assert table.size == 21


def test_initial_state():
    # Новая таблица пуста и содержит 8 ячеек
    table = HashTable()

    assert table.size == 0
    assert table.buckets == [[] for _ in range(8)]


def test_custom_capacity():
    # Начальное количество ячеек можно задать
    table = HashTable(capacity=4)

    assert len(table.buckets) == 4
    assert table.size == 0


def test_zero_capacity():
    # Нельзя создать таблицу без ячеек
    with pytest.raises(ValueError):
        HashTable(capacity=0)


def test_negative_capacity():
    # Количество ячеек не может быть отрицательным
    with pytest.raises(ValueError):
        HashTable(capacity=-3)


def test_insert_and_get():
    # Добавленное значение доступно по ключу
    table = HashTable()
    table.insert("cat", 10)

    assert table.get("cat") == 10
    assert table.size == 1


def test_independent_buckets():
    # Добавление в одну ячейку не меняет остальные ячейки
    table = HashTable()
    table.insert(0, "zero")

    assert table.buckets == [[[0, "zero"]], [], [], [], [], [], [], []]


def test_update_existing_key():
    # Повторная вставка обновляет значение без добавления новой пары
    table = HashTable()
    table.insert("cat", 10)
    table.insert("cat", 20)

    assert table.get("cat") == 20
    assert table.size == 1


def test_get_from_empty_table():
    # В пустой таблице искомого ключа нет
    table = HashTable()

    with pytest.raises(KeyError):
        table.get("missing")


def test_get_missing_key_in_occupied_bucket():
    # Совпадение индекса ячейки не означает совпадения ключей
    table = HashTable()
    table.insert(3, "cat")

    with pytest.raises(KeyError):
        table.get(11)


def test_collisions():
    # Ключи 3, 11 и 19 попадают в одну ячейку и сохраняются отдельно
    table = HashTable()
    table.insert(3, "cat")
    table.insert(11, "dog")
    table.insert(19, "fox")

    assert table.get(3) == "cat"
    assert table.get(11) == "dog"
    assert table.get(19) == "fox"
    assert table.size == 3


def test_update_with_collision():
    # Обновление одной пары не меняет соседние пары в той же ячейке
    table = HashTable()
    table.insert(3, "cat")
    table.insert(11, "dog")
    table.insert(11, "wolf")

    assert table.get(3) == "cat"
    assert table.get(11) == "wolf"
    assert table.size == 2


def test_delete_only_element():
    # После удаления единственной пары таблица становится пустой
    table = HashTable()
    table.insert("cat", 10)
    table.delete("cat")

    assert table.size == 0
    with pytest.raises(KeyError):
        table.get("cat")


def test_delete_first_in_bucket():
    # Удаление первой пары в цепочке сохраняет остальные
    table = HashTable()
    table.insert(3, "cat")
    table.insert(11, "dog")
    table.insert(19, "fox")
    table.delete(3)

    assert table.get(11) == "dog"
    assert table.get(19) == "fox"
    assert table.size == 2
    with pytest.raises(KeyError):
        table.get(3)


def test_delete_middle_in_bucket():
    # Удаление средней пары в цепочке сохраняет соседние
    table = HashTable()
    table.insert(3, "cat")
    table.insert(11, "dog")
    table.insert(19, "fox")
    table.delete(11)

    assert table.get(3) == "cat"
    assert table.get(19) == "fox"
    assert table.size == 2
    with pytest.raises(KeyError):
        table.get(11)


def test_delete_last_in_bucket():
    # Удаление последней пары в цепочке сохраняет предыдущие
    table = HashTable()
    table.insert(3, "cat")
    table.insert(11, "dog")
    table.insert(19, "fox")
    table.delete(19)

    assert table.get(3) == "cat"
    assert table.get(11) == "dog"
    assert table.size == 2
    with pytest.raises(KeyError):
        table.get(19)


def test_delete_from_empty_table():
    # Удаление из пустой таблицы вызывает ошибку и не меняет размер
    table = HashTable()

    with pytest.raises(KeyError):
        table.delete("missing")
    assert table.size == 0


def test_delete_missing_key_in_occupied_bucket():
    # При отсутствии ключа другие пары в его ячейке не удаляются
    table = HashTable()
    table.insert(3, "cat")

    with pytest.raises(KeyError):
        table.delete(11)
    assert table.get(3) == "cat"
    assert table.size == 1


def test_delete_twice():
    # Повторно удалить уже удалённый ключ нельзя
    table = HashTable()
    table.insert("cat", 10)
    table.delete("cat")

    with pytest.raises(KeyError):
        table.delete("cat")
    assert table.size == 0


def test_reinsert_deleted_key():
    # Удалённый ключ можно добавить снова с новым значением
    table = HashTable()
    table.insert("cat", 10)
    table.delete("cat")
    table.insert("cat", 20)

    assert table.get("cat") == 20
    assert table.size == 1


def test_zero_and_negative_keys():
    # Нулевые и отрицательные ключи поддерживаются
    table = HashTable()
    table.insert(0, "zero")
    table.insert(-5, "negative")

    assert table.get(0) == "zero"
    assert table.get(-5) == "negative"
    assert table.size == 2


def test_empty_string_key():
    # Пустая строка может быть ключом
    table = HashTable()
    table.insert("", "empty")

    assert table.get("") == "empty"


def test_none_value():
    # Значение None хранится как обычное значение
    table = HashTable()
    table.insert("cat", None)

    assert table.get("cat") is None
    assert table.size == 1


def test_list_value():
    # Значением может быть список
    table = HashTable()
    table.insert("numbers", [1, 2, 3])

    assert table.get("numbers") == [1, 2, 3]


def test_no_resize_at_threshold():
    # При заполнении ровно 0.75 расширение ещё не требуется
    table = HashTable()
    for key in range(6):
        table.insert(key, key * 10)

    assert len(table.buckets) == 8
    assert table.size == 6


def test_resize_above_threshold():
    # Седьмая пара увеличивает количество ячеек с 8 до 16
    table = HashTable()
    for key in range(7):
        table.insert(key, key * 10)

    assert len(table.buckets) == 16
    assert table.size == 7
    for key in range(7):
        assert table.get(key) == key * 10


def test_update_does_not_resize():
    # Обновление при заполнении 0.75 не увеличивает таблицу
    table = HashTable()
    for key in range(6):
        table.insert(key, key * 10)
    table.insert(3, "updated")

    assert table.get(3) == "updated"
    assert table.size == 6
    assert len(table.buckets) == 8


def test_redistribution_after_resize():
    # После расширения ключи получают новые индексы и остаются доступны
    table = HashTable(capacity=4)
    table.insert(0, "zero")
    table.insert(4, "four")
    table.insert(8, "eight")
    table.insert(12, "twelve")

    assert len(table.buckets) == 8
    assert table.size == 4
    assert table.get(0) == "zero"
    assert table.get(4) == "four"
    assert table.get(8) == "eight"
    assert table.get(12) == "twelve"


def test_capacity_one():
    # Таблица с одной ячейкой расширяется при первой вставке
    table = HashTable(capacity=1)
    table.insert("cat", 10)

    assert len(table.buckets) == 2
    assert table.get("cat") == 10
    assert table.size == 1


def test_multiple_resizes():
    # Несколько последовательных расширений не теряют данные
    table = HashTable(capacity=2)
    for key in range(100):
        table.insert(key, key * 10)

    assert table.size == 100
    assert table.size / len(table.buckets) <= 0.75
    for key in range(100):
        assert table.get(key) == key * 10


def test_update_and_delete_after_resize():
    # После расширения обновление и удаление используют новые индексы
    table = HashTable(capacity=4)
    for key in [0, 4, 8, 12]:
        table.insert(key, key * 10)
    table.insert(4, "updated")
    table.delete(12)

    assert table.get(4) == "updated"
    assert table.get(0) == 0
    assert table.get(8) == 80
    assert table.size == 3
    with pytest.raises(KeyError):
        table.get(12)
