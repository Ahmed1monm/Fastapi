from fastapi.responses import JSONResponse 
# by default fastAPI returns the response in JSON format


from typing import Union

from fastapi import Body, FastAPI, status

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}


@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Union[str, None] = Body(default=None),
    size: Union[int, None] = Body(default=None),
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, #* write your status code 
            
             content=item #! Content will be item, handel it as you want 

             #? content = {
             #?   "data": item
             #? }
             
             )