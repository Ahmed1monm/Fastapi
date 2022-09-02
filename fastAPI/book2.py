from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    title: str = Field(min_length=5)
    description: Optional[str] = Field(min_length=5, max_length=150)
    auther: str = Field(min_length=2, max_length=100)
    rating: int = Field(gt=-1, lt=101)
    id: UUID

    class Config:
        schema_extra = {
            "example":
                {
                    "title": "كتاب حياتي يا عين",
                    "description": "كتاب حياتي يا عين ما شوفت زيه كتاب الفرح فيه سطرين والباقي كله عذاب عذاااااااااب",
                    "auther": "الفنان حسن الأخضر هه",
                    "rating": 20,
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                },

        }


Books = []


@app.post('/')
async def add_book(book: Book):
    Books.append(book)
    return {
        "your data": book,
        'data': Books
    }
