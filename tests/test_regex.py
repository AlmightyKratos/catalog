import pytest

from catalog.ProductQuantity import get_split_words

product_titles = [
    ("295mL", ["295", "mL"]),
    ("355mL", ["355", "mL"]),
    ("4L", ["4", "L"]),
    ("1.8L", ["1.8", "L"]),
]


@pytest.mark.parametrize("test_input, expected", product_titles)
def test_regex(test_input, expected):
    assert get_split_words(test_input) == expected
