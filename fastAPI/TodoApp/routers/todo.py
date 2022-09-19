from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from routers.auth import get_current_user

import models
from database import engine, Sessionlocal
from fastapi import  Depends, HTTPException, APIRouter
from routers import auth


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={
        401: {
            "Todo": "Todo not found"
        }
    }
)
models.Base.metadata.create_all(bind=engine)


class TodoPost(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=5)
    complete: bool = False
    owner_id: int


def get_db():
    try:
        db = Sessionlocal()
        yield db
    finally:
        db.close()


@router.get('/')
async def read_all_database(db: Session = Depends(get_db)):
    return {'data': db.query(models.Todo).all()}


@router.post('/add_todo')
async def add_todo(todo: TodoPost, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    todo_model = models.Todo()

    todo_model.title = todo.title
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.description = todo.description
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    return {
        'msg': 'success'
    }


@router.get('/{todo_id}')
async def get_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    todo_model = db.query(models.Todo) \
        .filter(models.Todo.id == todo_id) \
        .filter(models.Todo.owner_id == user.get("id")) \
        .first()
    if todo_model is not None:
        return {
            'data': todo_model
        }
    else:
        raise http_exception()


def http_exception():
    return HTTPException(status_code=404, detail='Todo not found')


@router.put('/edit-todo')
async def edit_todo(todo_id: int, todo: TodoPost, user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    todo_model = db.query(models.Todo)\
        .filter(models.Todo.id == todo_id)\
        .filter(models.Todo.owner_id == user.get("id"))\
        .first()

    if todo_model is None or user is None:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    # todo_model.owner_id = todo.owner_id

    db.add(todo_model)
    db.commit()

    return {
        'msg': 'Success',
        'data': todo_model
    }


@router.delete('/{todo_id}')
async def delete_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_model is None or user is None:
        raise http_exception()
    db.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.owner_id == user.get("id")).delete()
    db.commit()

    return {
        'msg': 'deleted Successfully'
    }


@router.get("/user")
async def read_all_todos_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models.Todo).filter(models.Todo.owner_id == user.get("id")).all()
