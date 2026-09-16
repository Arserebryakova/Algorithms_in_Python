from palindrome import palindrome_check


def test_palindrome():
    assert palindrome_check(121) is True  # odd number of digits
    assert palindrome_check(1221) is True  # even number of digits
    assert palindrome_check(1001) is True  # contains zeros even
    assert palindrome_check(20002) is True  # contains zeros odd
    assert palindrome_check(777777777777777777777777777777) is True  # large number
    assert palindrome_check(7) is True  # single digit
    assert palindrome_check(11) is True  # smallest two-digit palindrome


def test_not_palindrome():
    assert palindrome_check(31) is False  # even number of digits
    assert palindrome_check(123) is False  # odd number of digits
    assert palindrome_check(20032002) is False  # contains zeros
    assert palindrome_check(777777777777765437777777777777) is False  # large number
    assert palindrome_check(10) is False  # trailing zero
