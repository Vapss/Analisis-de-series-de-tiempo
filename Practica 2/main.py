from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str 
    price: float
    tax: float


app = FastAPI()

    
@app.post("/items/")
async def create_item(item: Item):
    return item