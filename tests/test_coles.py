import pytest

from catalog.ColesCrawler import ColesCrawler


def test_coles_search():
    with open("tests/files/coles_search.html") as file:
        ret = ColesCrawler._process_search_html(file)

    assert len(ret) == 24


@pytest.mark.asyncio
async def test_coles_half_price():
    coles_crawler = ColesCrawler
    print(await coles_crawler.get_half_price_products())
