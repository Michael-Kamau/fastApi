from typing import Union

from fastapi import FastAPI, Depends, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from . import models

from .database import  engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int,db: Session=Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    print(post)
    return {"data": post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createPost(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    print(post)
    print(new_post)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'message':'Successfully added the post', 'data':new_post}

@app.delete('/posts/{id}')
def delete_post(id:int, db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The post with an id of {id} cannot be deleted')
    
    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id:int, updated_post:Post, db:Session=Depends(get_db)):
    post_query= db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_query.update(updated_post.dict(), synchronize_session = False)

    db.commit()

    return {'data': post_query.first()}


@app.get("/sqlalchemy")
def test_post(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
