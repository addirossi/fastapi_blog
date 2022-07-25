from decimal import Decimal

from fastapi import FastAPI


from models import Product, ProductsList

app = FastAPI()


@app.get("/products/", response_model=ProductsList)
async def products_list():
    return {"items": [{"name": "Asus Rog", "description": "dawawdwaa", "price": "100000", "category": "tv"}]}
