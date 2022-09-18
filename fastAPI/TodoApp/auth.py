from fastapi import FastAPI, Depends, HTTPException
import models
from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import Sessionlocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt

app = FastAPI()

bcrypt_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = Sessionlocal()
        yield db
    finally:
        db.close()


def hashing_password(password: str):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user: models.Users = db.query(models.Users) \
        .filter(models.Users.username == username) \
        .first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


SECRET_KEY = "ahmed-mohamed_abdul-monem"
ALGORITHM = "HS256"


def create_access_token(username: str, userid: int, expires_delta: Optional[timedelta] = None):
    encode = {
        "sub": username,
        "id": userid
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({
        "exp": expire
    })
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


class CreateUser(BaseModel):
    email: Optional[str]
    username: str
    first_name: str
    last_name: str
    password: str
    is_active: bool


@app.post('/create/user')
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user_model = models.Users()

    user_model.email = user.email
    user_model.username = user.username
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    hashed = hashing_password(user.password)
    user_model.hashed_password = hashed
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    return {
        'msg': 'success',
        'data': user_model.username
    }


@app.post('/token')
async def login_user_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    token_expire = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, token_expire)
    return {
        "token": token
    }


oauth2_token = OAuth2PasswordBearer(tokenUrl='token')
