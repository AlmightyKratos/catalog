from decimal import Decimal

from pydantic import BaseModel

from catalog.ProductQuantity import ProductQuantity, UnitEnum, get_quantity


class Product(BaseModel):
    name: str
    price: Decimal
    quantity: ProductQuantity = ProductQuantity(quantity=0, unit=UnitEnum.initial)

    def get_quantity(self) -> None:
        self.quantity = get_quantity(self.name)

    def clean_name(self) -> None:
        self.name = get_clean_name(self.name)

    def print_pretty_product(self) -> None:
        self.get_quantity()
        self.clean_name()
        print(
            f"Name: {self.name}, Price: ${self.price}, Amount: {self.quantity.quantity} {self.quantity.unit}"
        )


def get_price_per_volume(product: Product) -> str:
    match product.quantity.unit:
        case UnitEnum.g:
            return f"${product.price*1000 / product.quantity.quantity:.2f} per kg"
        case UnitEnum.kg:
            return "kg"
        case UnitEnum.unit:
            return "unit"
        case UnitEnum.unknown:
            return "unknown"
        case UnitEnum.initial:
            return "initial"
        case UnitEnum.mL:
            return "mL"
        case UnitEnum.L:
            return "L"


def print_unknown_unit_products(products: list[Product]) -> None:
    for product in products:
        product.get_quantity()
        if product.quantity.unit == UnitEnum.unknown:
            print(product)


def get_clean_name(name: str) -> str:
    names = name.split()
    if "|" in names:
        char_index = names.index("|")
        names = names[:char_index]
    clean_name = " ".join(names)
    return clean_name


def print_pretty_products(products: list[Product]) -> None:
    for product in products:
        product.print_pretty_product()
    print(len(products))


def generate_products(names: list[str], prices: list[Decimal]):
    try:
        return [
            Product(name=name, price=price)
            for name, price in zip(names, prices, strict=True)
        ]
    except ValueError as exc:
        raise Exception("error") from exc
