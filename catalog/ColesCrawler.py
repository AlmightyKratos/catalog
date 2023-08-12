from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from catalog.Product import Product, generate_products

COLES_URL = "https://www.coles.com.au"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
}


class ColesCrawler:
    @classmethod
    async def _get_half_price_html(cls) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_extra_http_headers(HEADERS)
            await page.goto(f"{COLES_URL}/half-price-specials")
            await page.wait_for_selector(
                ".coles-targeting-ProductListProductListContainer"
            )
            page_html = await page.content()
            await browser.close()
        return page_html

    @classmethod
    async def _get_search_html(cls, search_query: str) -> str:
        """NOTE: this only gets up to 24 items, although there can be a maximum of 48 on the page"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_extra_http_headers(HEADERS)
            await page.goto(f"{COLES_URL}/search?q={search_query}")
            page_html = await page.content()
            await browser.close()
        return page_html

    @classmethod
    def _process_search_html(cls, page_html: str) -> list[Product]:
        soup = BeautifulSoup(page_html, "html.parser")
        results = soup.find_all(
            "section", class_="coles-targeting-ProductTileProductTileWrapper"
        )

        names = [result.find("h2", class_="product__title").text for result in results]
        prices = [
            result.find("span", class_="price__value").text[1:] for result in results
        ]

        return generate_products(names, prices)

    @classmethod
    def _process_half_price_html(cls, page_html: str) -> list[Product]:
        soup = BeautifulSoup(page_html, "html.parser")
        elements = soup.find_all("section")

        names = [
            name.text
            for el in elements
            if (name := el.find("h2", class_="product__title")) is not None
        ]

        prices = [
            price.find("span", class_="price__value").text[1:]
            for el in elements
            if (price := el.find("div", class_="product__cta_section")) is not None
        ]

        return generate_products(names, prices)

    @classmethod
    async def get_search_products(cls, search_query: str) -> list[Product]:
        page_html = await cls._get_search_html(search_query)
        return cls._process_search_html(page_html)

    @classmethod
    async def get_half_price_products(cls) -> list[Product]:
        page_html = await cls._get_half_price_html()
        return cls._process_half_price_html(page_html)
