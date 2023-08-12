from fastapi import FastAPI

from catalog.ColesCrawler import ColesCrawler

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/coles/half-price")
async def coles_half_price():
    return await ColesCrawler.get_half_price_products()


@app.get("/coles/search/{search_query}")
async def coles_search(search_query: str):
    return await ColesCrawler.get_search_products(search_query)
