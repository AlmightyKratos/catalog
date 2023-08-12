from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from catalog.Product import Product, generate_products

URL = "https://www.woolworths.com.au/shop"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
}


class WoolworthsCrawler:
    @classmethod
    async def _get_half_price_html(cls) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_extra_http_headers(HEADERS)
            await page.goto(f"{URL}/browse/specials/half-price")
            await page.wait_for_selector(".product-title-link")
            page_html = await page.content()
            await browser.close()
        return page_html

    @classmethod
    async def _get_search_html(cls, search_term: str) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_extra_http_headers(HEADERS)
            await page.goto(f"{URL}/search/products?searchTerm={search_term}")
            await page.wait_for_selector(".product-tile-price")
            page_html = await page.content()
            await browser.close()
        return page_html

    @classmethod
    def _process_half_price_html(cls, page_html: str) -> list[Product]:
        soup = BeautifulSoup(page_html, "html.parser")
        names = [el.text for el in soup.find_all("a", class_="product-title-link")]

        prices_container = soup.find_all("div", class_="product-tile-price")
        prices = [el.find("div", class_="primary").text[1:] for el in prices_container]
        return generate_products(names, prices)

    @classmethod
    def _process_search_html(cls, page_html: str) -> list[Product]:
        soup = BeautifulSoup(page_html, "html.parser")
        name_containers = soup.find_all("div", class_="product-tile-title")
        names = [
            name_containers.find("a", class_="product-title-link").text
            for name_containers in name_containers
        ]

        price_containers = soup.find_all("div", class_="product-tile-price")
        prices = [
            price_container.find("div", class_="primary").text[1:]
            for price_container in price_containers
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
