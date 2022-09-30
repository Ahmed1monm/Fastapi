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

