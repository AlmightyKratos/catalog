import pytest

from catalog.Product import Product
from catalog.ProductQuantity import ProductQuantity, UnitEnum, get_quantity

product_titles: list[tuple[str, ProductQuantity]] = [
    (
        "Bonds Womens Socks Low Cut Size 3-8 Assorted 3 Pack",
        ProductQuantity(quantity=3, unit=UnitEnum.unit),
    ),
    (
        "Gippsland Dairy Cookies & Cream Yoghurt 140g",
        ProductQuantity(quantity=140, unit=UnitEnum.g),
    ),
    (
        "Golden Gaytime Streets Ice Cream Original Original 100ml X 4 Pack",
        ProductQuantity(quantity=4, unit=UnitEnum.unit),
    ),
    (
        "Latina Fresh Spinach & Ricotta Agnolotti 375g",
        ProductQuantity(quantity=375, unit=UnitEnum.g),
    ),
    (
        "Oral-b Pro 800 Electric Toothbrush Each",
        ProductQuantity(quantity=1, unit=UnitEnum.unit),
    ),
    (
        "Pringles Original Salted Potato Chips 134g",
        ProductQuantity(quantity=134, unit=UnitEnum.g),
    ),
    (
        "Drink 1 600mL",
        ProductQuantity(quantity=600, unit=UnitEnum.mL),
    ),
    (
        "Drink 1 600ml",
        ProductQuantity(quantity=600, unit=UnitEnum.mL),
    ),
    (
        "Drink 2 600L",
        ProductQuantity(quantity=600, unit=UnitEnum.L),
    ),
    (
        "Drink 2 600l",
        ProductQuantity(quantity=600, unit=UnitEnum.L),
    ),
    (
        "Unknown Product 134h",
        ProductQuantity(quantity=0, unit=UnitEnum.unknown),
    ),
    (
        "Solo Zero Sugar 10x375ml",
        ProductQuantity(quantity=0, unit=UnitEnum.unknown),
    ),
    (
        "Solo Zero Sugar 10x375mL",
        ProductQuantity(quantity=0, unit=UnitEnum.unknown),
    ),
    (
        "  a ",
        ProductQuantity(quantity=0, unit=UnitEnum.unknown),
    ),
    (
        "",
        ProductQuantity(quantity=0, unit=UnitEnum.unknown),
    ),
    (
        "a b c asdf sdfg wert 1234 sdfg 3456asdf",
        ProductQuantity(quantity=0, unit=UnitEnum.unknown),
    ),
    (
        "Caterers Choice Banana Chips 1Kg",
        ProductQuantity(quantity=1, unit=UnitEnum.kg),
    ),
]


@pytest.mark.parametrize("test_input, expected", product_titles)
def test_quantity(test_input, expected):
    assert get_quantity(test_input) == expected


product_titles2 = [
    ("Radiant Laundry Liquid Plus Softener | 1.8L", 1.8, UnitEnum.L),
    ("Sunkist Zero Sugar Cans 375ml X10 Pack", 10, UnitEnum.unit),
    ("Pop! Vinyl Figurine Hey Arnold Arnold Banana", 0, UnitEnum.unknown),
]


@pytest.mark.parametrize(
    "test_input_name, expected_quantity, expected_unit", product_titles2
)
def test_quantity2(test_input_name, expected_quantity, expected_unit):
    product = Product(name=test_input_name, price=1)
    product.get_quantity()
    assert product.quantity == ProductQuantity(
        quantity=expected_quantity, unit=expected_unit
    )
