from ctypes import Union
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import false

app = FastAPI()


# tokenUrl is the end point to take token 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


class UserModel(BaseModel):
    username: str
    email: str #Union[str, None] = None
    full_name: str #Union[str, None] = None
    disabled: str# Union[bool, None] = None

# def fake_decode_token(token):
#     return UserModel(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     return user


# @app.get("/users/me")
# async def read_users_me(current_user: UserModel = Depends(get_current_user)):
#     return current_user


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class UserInDB(UserModel):
    hashed_password: str

def get_user(db, username:str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)




def fake_decode_token(token:str):
    user = get_user(fake_users_db, token)
    return user




async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}, #! Any HTTP (error) status code 401 "UNAUTHORIZED" is supposed to also return a WWW-Authenticate header.
        )
    return user




def fake_hash_password(password: str):
    return "fakehashed" + password




async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if  current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user





@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    #! The response of the token endpoint must be a JSON object.
    #* It should have a token_type. In our case, as we are using "Bearer" tokens, the token type should be "bearer".
    #* And it should have an access_token, with a string containing our access token.

    return {"access_token": user.username, "token_type": "bearer"} 







@app.get("/users/me")
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user
