from pydantic import BaseModel, ConfigDict 


class CommentOut(BaseModel): 
    model_config = ConfigDict(from_attributes=True)
    id: int 
    text: str 


class TagOut(BaseModel): 
    model_config = ConfigDict(from_attributes=True)
    id: int 
    name: str 

class PostOut(BaseModel): 
    model_config = ConfigDict(from_attributes=True)
    id: int 
    title: str 
    body: str 
    tags: list[TagOut] = [] 

class PostDetail(PostOut): 
    comments: list[CommentOut] = [] 

class UserOut(BaseModel): 
    model_config = ConfigDict(from_attributes=True)
    id: int 
    username: str 

class UserWithPosts(UserOut):
    posts: list[PostOut] = [] 

class PostCreate(BaseModel): 
    title: str 
    body: str 
    tag_names: list[str] = [] 

class CommentCreate(BaseModel): 
    text: str 
    user_id: int 