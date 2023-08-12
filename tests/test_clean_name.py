import pytest

from catalog.Product import get_clean_name

product_titles = [
    ("Lifesavers Bananas       | 160g", "Lifesavers Bananas"),
]


@pytest.mark.parametrize("input_name, expected", product_titles)
def test_clean_name(input_name, expected):
    name = input_name
    clean_name = get_clean_name(name)
    assert clean_name == expected
