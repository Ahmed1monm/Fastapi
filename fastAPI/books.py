from typing import Optional

from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    'Book_1': {"title": "Book 1", "Auther": "Auther 1"},
    'Book_2': {"title": "Book 2", "Auther": "Auther 2"},
    'Book_3': {"title": "Book 3", "Auther": "Auther 3"},
    'Book_4': {"title": "Book 4", "Auther": "Auther 4"},
    'Book_5': {"title": "Book 5", "Auther": "Auther 5"},
    'Book_6': {"title": "Book 6", "Auther": "Auther 6"},

}


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):  # Query parameter
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return {
            "msg": "Success",
            "data": new_books
        }
    return {
        "msg": "Success",
        "data": BOOKS
    }


@app.get("/books/{book_title}")  # Path parameter
async def read_specefic_book(book_title: str):
    key = book_title.title()
    return BOOKS[key]


@app.post("/")  # post request
async def create_book(book_title, book_auther):
    current_index = 0
    for book in BOOKS:
        if len(BOOKS) > 0:
            x = int(book.split("_")[-1])
            if x > current_index:
                current_index = x
    BOOKS[f'book_{current_index}'] = {"title": book_auther, "Auther": book_auther}
    return {
        "Data": BOOKS
    }


@app.put("/book_name")
async def edit_book(book_name, book_title, book_auther):
    temp = {"title": book_title, "Auther": book_auther}
    BOOKS[book_name] = temp
    return {
        "your data": temp,
        "all data": BOOKS
    }


@app.delete("/{book_name}")
async def delete_book(book_name):

    del BOOKS[book_name]
    return {
        'msg': f'book {book_name} deleted successfully',
        'data': BOOKS
    }
