from sqlalchemy import ForeignKey, String, Text, Table , Column 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column , relationship 

class Base(DeclarativeBase): 
    pass 


post_tags = Table(
    "post_tags",Base.metadata,
    Column("post_id",ForeignKey("posts.id"),primary_key=True),
    Column("tag_id",ForeignKey("tags.id"),primary_key=True),
)

class User(Base): 
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50),unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="author",cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")

class Post(Base): 
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="post")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post",cascade="all, delete-orphan")
    tags: Mapped[list["Tag"]]  = relationship(secondary=post_tags,back_populates="posts")

class Comment(Base): 
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")

class Tag(Base): 
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30),unique=True)
    posts: Mapped[list["Post"]] = relationship(secondary=post_tags,back_populates="tags")
    