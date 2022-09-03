from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    title: str = Field(min_length=5)
    description: Optional[str] = Field(min_length=5, max_length=150)
    author: str = Field(min_length=2, max_length=100)
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


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    # if books_to_return and books_to_return < 0:
    #     raise NegativeNumberException(books_to_return=books_to_return)

    if len(Books) < 1:
        create_books_no_api()

    if books_to_return and len(Books) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(Books[i - 1])
            i += 1
        return new_books
    return Books


def create_books_no_api():
    book_1 = Book(id="71f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="21f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id="31f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)
    book_4 = Book(id="41f4c2ea-1340-41f4-89f7-2852347bb0d1",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=90)
    Books.append(book_1)
    Books.append(book_2)
    Books.append(book_3)
    Books.append(book_4)


@app.delete('/')
async def delete_book(book_id: UUID):
    count = 0
    for book in Books:
        count += 1
        if book_id == book.id:
            del Books[count - 1]
            return {
                'Msg': f'Book with id = {book_id} deleted successfully'
            }

    raise HTTPException(status_code=400, detail=f'There is No books with id = {book_id}')
