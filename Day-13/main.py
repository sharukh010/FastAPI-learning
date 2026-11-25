from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select 
from sqlalchemy.orm import Session, selectinload
from database import engine, get_db
import models,schemas 


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Blog API")


@app.post("/users",response_model=schemas.UserOut,status_code=201)
def create_user(username: str,db: Session = Depends(get_db)): 
    user = models.User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 


@app.get("/users/{user_id}",response_model=schemas.UserWithPosts)
def get_user(user_id: int, db: Session = Depends(get_db)): 
    stmt = select(models.User).where(
        models.User.id == user_id
    ).options(
        selectinload(
            models.User.posts
        )
    )
    user = db.scalar(stmt)
    if user is None: 
        raise HTTPException(404,"User not found")
    return user 

@app.post("/users/{user_id}/posts",response_model=schemas.PostOut,status_code=201)
def create_post(user_id: int, data: schemas.PostCreate, db: Session = Depends(get_db)): 
    if not db.get(models.User,user_id): 
        raise HTTPException(404, "User not found")
    post = models.Post(title=data.title,body=data.body,user_id=user_id)
    for name in data.tag_names: 
        tag = db.scalar(select(models.Tag).where(models.Tag.name == name))
        post.tags.append(tag or models.Tag(name=name))
    db.add(post); db.commit(); db.refresh(post)
    return post 


@app.get("/posts/{post_id}",response_model=schemas.PostDetail)
def get_post(post_id: int, db: Session = Depends(get_db)): 
    stmt = select(models.Post).where(
        models.Post.id == post_id
    ).options(
        selectinload(
            models.Post.comments
        ),selectinload(
            models.Post.tags
        )
    )
    post = db.scalar(stmt)
    if not post: 
        raise HTTPException(404, "Post not found")
    return post 


@app.post("/posts/{post_id}/comments",response_model=schemas.CommentOut,status_code=201)
def add_comment(post_id: int, data: schemas.CommentCreate, db: Session = Depends(get_db)): 
    if not db.get(models.Post,post_id) or not db.get(models.User,data.user_id): 
        raise HTTPException(404,"Post or user not found")
    c = models.Comment(text = data.text,post_id=post_id,user_id=data.user_id)
    db.add(c); db.commit(); db.refresh(c)
    return c 

@app.get("/tags/{name}/posts",response_model=list[schemas.PostOut])
def post_by_tag(name: str, db: Session = Depends(get_db)): 
    tag = db.scalar(select(models.Tag).where(models.Tag.name == name))
    if not tag: 
        raise HTTPException(404,"Tag not found")
    return tag.posts 