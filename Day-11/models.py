from sqlalchemy import String, Boolean 
from sqlalchemy.orm import Mapped, mapped_column 
from database import Base 


class Todo(Base): 
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500),default=None)
    done: Mapped[bool] = mapped_column(Boolean,default=False)