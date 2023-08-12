import pytest

from catalog.Product import Product, get_price_per_volume
from catalog.ProductQuantity import ProductQuantity, UnitEnum

product_titles = [
    (500, 500, UnitEnum.unit, "unit"),
    (500, 500, UnitEnum.g, "$1000.00 per kg"),
    (5, 985, UnitEnum.g, "$5.08 per kg"),
]


@pytest.mark.parametrize(
    "input_price, input_quantity, input_unit, expected", product_titles
)
def test_price_per_volume(input_price, input_quantity, input_unit, expected):
    product = Product(
        name="thing1",
        price=input_price,
        quantity=ProductQuantity(quantity=input_quantity, unit=input_unit),
    )

    assert get_price_per_volume(product) == expected
