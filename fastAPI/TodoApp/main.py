from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import engine, Sessionlocal
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class TodoPost(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=5)
    complete: bool = False


def get_db():
    try:
        db = Sessionlocal()
        yield db
    finally:
        db.close()


@app.get('/')
async def read_all_database(db: Session = Depends(get_db)):
    return {'data': db.query(models.Todo).all()}


@app.post('/add_todo')
async def add_todo(todo: TodoPost, db: Session = Depends(get_db)):
    todo_model = models.Todo()

    todo_model.title = todo.title
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.description = todo.description

    db.add(todo_model)
    db.commit()

    return {
        'msg': 'success'
    }


@app.get('/todo/{todo_id}')
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_model is not None:
        return {
            'data': todo_model
        }
    else:
        raise http_exception()


def http_exception():
    return HTTPException(status_code=404, detail='Todo not found')
