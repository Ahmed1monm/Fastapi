from fastapi import FastAPI, File, HTTPException, Header, UploadFile, Form, Depends
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

async def verify_token(x_token: str = Header(default= None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(default= None)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/deps", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]