from fastapi import FastAPI, Query, Path
from typing import List, Union
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Use Query to take query items
# Query can be list, Link will be  /hello/Ahmed?q=Monem&q=Mostafa&q=Hager
# if you want to take list as query parameter you must use Query from fast api 
# you can set default values for query parameters Query(default= ["Ahmed", "Hagar", "Mostafa"])

@app.get("/hello/{name}")
async def say_hello(name: str, q: Union[List[str], None] = Query(default=None)):
    query_items = q

    return {"message": f"Hello {name}", "Query": query_items}


@app.get("/welcome")
async def say_welcome(name: Union[str, None] = Path(default=None)):
    if name:
        return {
            'Message': name}
    else:
        return {'Message': 'Ahmed Monem'}


# response model 
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list[str] = []

# Notice that response_model is a parameter of the "decorator" 
# method (get, post, etc). Not of your path operation function, like all the parameters and body.
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item