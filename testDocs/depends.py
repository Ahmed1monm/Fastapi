from fastapi import Depends, HTTPException, Header, FastAPI

app = FastAPI()


async def verify_token(x_token: str = Header(default= None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(default= None)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

# Know that if those dependencies returns a value, it will not be used
# In this case you should use normal dependencies
@app.get("/items/deps", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

#* We can add dependencies for the whole FastAPI application that way:
#*app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

#* Depends with yield
async def get_db():
    db = '' #DBSession()
    try:
        yield db
    finally:
        db.close()


