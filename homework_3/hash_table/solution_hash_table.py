class HashTable:
    """Хеш-таблица на списках с разрешением коллизий методом цепочек."""

    def __init__(self, capacity=8):
        if capacity <= 0:
            raise ValueError("Размер таблицы должен быть положительным")

        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def get_index(self, key):
        return hash(key) % len(self.buckets)

    def get(self, key):
        index = self.get_index(key)
        bucket = self.buckets[index]

        for stored_key, stored_value in bucket:
            # Проверка идентичности позволяет найти даже ключ NaN.
            if stored_key is key or stored_key == key:
                return stored_value

        raise KeyError(key)

    def insert(self, key, value):
        index = self.get_index(key)
        bucket = self.buckets[index]

        # Если ключ уже существует, обновляем его значение
        for pair in bucket:
            if pair[0] is key or pair[0] == key:
                pair[1] = value
                return

        # Если ключ не найден, добавляем новую пару
        bucket.append([key, value])
        self.size += 1

        # При превышении порога увеличиваем таблицу
        if self.size / len(self.buckets) > 0.75:
            self._resize()

    def delete(self, key):
        index = self.get_index(key)
        bucket = self.buckets[index]

        # Ищем пару с нужным ключом внутри ячейки
        for pair_index, pair in enumerate(bucket):
            if pair[0] is key or pair[0] == key:
                del bucket[pair_index]
                self.size -= 1
                return

        # Все пары проверены, но ключ не найден
        raise KeyError(key)

    def _resize(self):
        old_buckets = self.buckets
        new_capacity = len(old_buckets) * 2
        self.buckets = [[] for _ in range(new_capacity)]

        # При новой ёмкости индексы пересчитываются для всех пар.
        for bucket in old_buckets:
            for pair in bucket:
                index = self.get_index(pair[0])
                self.buckets[index].append(pair)
