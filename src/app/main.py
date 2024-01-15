from typing import Union

from fastapi import FastAPI, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from . import models

from .database import  engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post('/posts')
def createPost(post: Post):
    print(post)
    return {'message':'Successfully added the comment'}


# @app.get("/sqlalchemy")
# def testPost(db:Session = Depends(get_db)):
#     return {"status": "Success"}
