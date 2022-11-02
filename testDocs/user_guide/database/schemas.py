#! Here is Pydantic Models

from typing import Union

from pydantic import BaseModel

#* Create Pydantic models / schemas for reading / returning
class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True #! Without orm_mode, if you returned a SQLAlchemy model from your path operation, it wouldn't include the relationship data.


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
