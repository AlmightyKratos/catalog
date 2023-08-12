from typing import Protocol

from catalog.Product import Product


class Crawler(Protocol):
    @classmethod
    async def get_search_products(cls, search_query: str) -> list[Product]:
        ...

    @classmethod
    async def get_half_price_products(cls) -> list[Product]:
        ...
