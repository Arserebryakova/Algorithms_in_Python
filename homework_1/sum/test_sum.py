from sum import max_even_arr_sum


def test_sum():
    assert max_even_arr_sum([5, 7, 13, 2, 14]) == 36  # example from the task
    assert max_even_arr_sum([3]) == 0  # single odd number
    assert max_even_arr_sum([2]) == 2  # single even number

    assert max_even_arr_sum([2, 4, 6, 8, 10]) == 30  # only even numbers

    assert max_even_arr_sum([1, 3, 5, 7, 9]) == 24  # odd total sum, remove the smallest odd number
    assert max_even_arr_sum([1, 3, 7, 9]) == 20  # even total sum of odd numbers
    assert max_even_arr_sum([2, 3, 5]) == 10  # mixed array with already even total sum

    assert max_even_arr_sum([3, 1, 7, 9]) == 20  # element order should not affect the result
    assert max_even_arr_sum([3, 7, 9, 1]) == 20  # smallest odd number is at the end

    assert max_even_arr_sum([9, 5, 3, 8]) == 22  # smallest odd number is in the middle
    assert max_even_arr_sum([2, 3]) == 2  # mixed small array

    assert max_even_arr_sum([1, 1, 1, 1, 1]) == 4  # odd number of equal odd elements
    assert max_even_arr_sum([1, 1, 1, 1]) == 4  # even number of equal odd elements

    assert max_even_arr_sum([999999999999999999]) == 0  # large odd number
