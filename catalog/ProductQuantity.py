import re
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ValidationError


class UnitEnum(str, Enum):
    g = "g"
    kg = "kg"
    unit = "unit"
    unknown = "unknown"
    initial = "initial"
    mL = "mL"
    L = "L"


class ProductQuantity(BaseModel):
    quantity: Decimal | int
    unit: UnitEnum

    @classmethod
    def unknown(cls):
        return ProductQuantity(quantity=0, unit=UnitEnum.unknown)


def get_split_words(word: str) -> list[str]:
    """splits single string by alphabetical and numerical characters"""
    return [char for char in re.split(r"(\d+\.\d+|\d+|\D+)", word) if char != ""]


def get_quantity(title: str) -> ProductQuantity:
    words = title.split()
    if len(words) < 2:
        return ProductQuantity.unknown()
    last_word = words[-1]
    if last_word in ["Each", "each"]:
        return ProductQuantity(quantity=1, unit=UnitEnum.unit)
    elif last_word in ["Pack", "pack"]:
        if words[-2][0] == "X":
            quantity = words[-2][1:]
        else:
            quantity = words[-2]
        return ProductQuantity(quantity=int(quantity), unit=UnitEnum.unit)
    else:
        last_words = get_split_words(last_word)
        if len(last_words) == 1:
            return ProductQuantity.unknown()
        match last_words[1]:
            case "ml" | "mL":
                unit = UnitEnum.mL
            case "l" | "L":
                unit = UnitEnum.L
            case "g":
                unit = UnitEnum.g
            case "kg" | "Kg":
                unit = UnitEnum.kg
            case _:
                return ProductQuantity.unknown()
        try:
            return ProductQuantity(quantity=Decimal(last_words[0]), unit=unit)
        except ValueError:
            return ProductQuantity.unknown()
        except ValidationError:
            return ProductQuantity.unknown()
