from fastapi import FastAPI, Query, Path, File, UploadFile
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

#*----------------------------------------------------------------------
#*FastAPI will use this response_model to:
# Convert the output data to its type declaration.
# Validate the data.
# Add a JSON Schema for the response, in the OpenAPI path operation.
# Will be used by the automatic documentation systems.
# But most importantly:
# Will limit the output data to that of the model

@app.post("/items/", response_model=Item)  
async def create_item(item: Item):
    return item

#---------------------------------------------------------------------
class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: Union[str, None] = None


@app.post("/user/", response_model=UserOut) #* Will cast UserIn to be UserOut 
async def create_user(user: UserIn):
    return user


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


# sometimes you have default values for some fields in your model
# you not want to send default and optional fields that have null values 
# make response_model_exclude_unset=True 
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]

# @app.post("/files/")
# async def create_file(file:Union [bytes , None] = File(default=None)):
#     if not file:
#         return {"message": "No file sent"}
#     else:
#         return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file( file:Union[ UploadFile , None]  = None ):
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         return {"filename": file.filename}

