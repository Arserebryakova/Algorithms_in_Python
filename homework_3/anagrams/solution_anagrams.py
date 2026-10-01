def anagrams(strs: list[str]) -> list[list[str]]:
    """Группирует анаграммы с учётом регистра, сохраняя повторения слов."""
    vocab = {}
    for word in strs:
        # Сортировка даёт одинаковый ключ для всех анаграмм одного слова.
        key = "".join(sorted(word))
        if key not in vocab:
            vocab[key] = []

        vocab[key].append(word)
    return list(vocab.values())


if __name__ == "__main__":
    strs = input().split()
    print(anagrams(strs))
