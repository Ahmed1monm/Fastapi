from fastapi import FastAPI, File, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime
from typing import Union

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File(description="A file read as bytes", default= None)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile",default=None),
):
    return {"filename": file.filename}



# Multi file upload 
#* Form Data
@app.post("/files/file")
async def create_file(
    file: bytes = File(default=None), fileb: UploadFile = File(default=None), token: str = Form(default=None)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data