from catalog.Product import print_unknown_unit_products
from catalog.WoolworthsCrawler import WoolworthsCrawler


def test_woolworths_search():
    with open("tests/files/woolworths_search.html") as file:
        ret = WoolworthsCrawler._process_search_html(file)
        print_unknown_unit_products(ret)

    # assert len(ret) == 36


test_woolworths_search()
