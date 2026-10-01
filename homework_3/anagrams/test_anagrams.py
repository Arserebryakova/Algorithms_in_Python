from solution_anagrams import anagrams


def test_anagrams_unicode_and_case():
    # Кириллица поддерживается, а регистр букв имеет значение.
    strs = ["кот", "ток", "Кот", "abc", "bca", "Abc"]
    expected = [["кот", "ток"], ["Кот"], ["abc", "bca"], ["Abc"]]

    assert sorted(map(sorted, anagrams(strs))) == sorted(map(sorted, expected))


def test_anagrams_preserves_input():
    strs = ["tea", "eat", "bat", "tea"]
    original = strs.copy()

    anagrams(strs)

    assert strs == original


def test_anagrams_example():
    # Пример из условия: несколько групп разного размера
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    expected = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]

    assert sorted(map(sorted, anagrams(strs))) == sorted(map(sorted, expected))


def test_anagrams_single_letters():
    # Одинаковые однобуквенные слова объединяются в группы
    strs = ["a", "b", "a", "c", "b"]
    expected = [["a", "a"], ["b", "b"], ["c"]]

    assert sorted(map(sorted, anagrams(strs))) == sorted(map(sorted, expected))


def test_anagrams_groups_differ_by_one_letter():
    # Замена одной буквы создаёт отдельную группу
    strs = ["eat", "tea", "ear", "are"]
    expected = [["eat", "tea"], ["ear", "are"]]

    assert sorted(map(sorted, anagrams(strs))) == sorted(map(sorted, expected))


def test_anagrams_empty_list():
    # В пустом списке нет групп
    strs = []

    assert anagrams(strs) == []


def test_anagrams_one_word():
    # Единственное слово образует одну группу
    strs = ["hello"]

    assert anagrams(strs) == [["hello"]]


def test_anagrams_all_in_one_group():
    # Все слова являются анаграммами друг друга
    strs = ["abc", "bca", "cab", "acb"]
    expected = [["abc", "bca", "cab", "acb"]]

    assert sorted(map(sorted, anagrams(strs))) == sorted(map(sorted, expected))


def test_anagrams_no_matches():
    # У каждого слова своя группа
    strs = ["cat", "dog", "sun"]
    expected = [["cat"], ["dog"], ["sun"]]

    assert sorted(map(sorted, anagrams(strs))) == sorted(map(sorted, expected))


def test_anagrams_duplicate_words():
    # Повторяющиеся слова сохраняются в результате
    strs = ["eat", "eat", "tea", "bat", "bat"]
    expected = [["eat", "eat", "tea"], ["bat", "bat"]]

    assert sorted(map(sorted, anagrams(strs))) == sorted(map(sorted, expected))


def test_anagrams_different_letter_counts():
    # Важны не только сами буквы, но и количество каждой буквы
    strs = ["ab", "aab", "aba", "abb", "bab"]
    expected = [["ab"], ["aab", "aba"], ["abb", "bab"]]

    assert sorted(map(sorted, anagrams(strs))) == sorted(map(sorted, expected))


def test_anagrams_empty_strings():
    # Пустые строки объединяются в одну группу и не теряются
    strs = ["", "", "a"]
    expected = [["", ""], ["a"]]

    assert sorted(map(sorted, anagrams(strs))) == sorted(map(sorted, expected))
