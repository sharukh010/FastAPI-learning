from sqlalchemy import String, Boolean, Date , Enum, DateTime, func , select 
from sqlalchemy.orm import Mapped, mapped_column, Session
from app.database import Base 
from app.schemas import Priority
from datetime import date,datetime, timezone
import app.exceptions as exceptions 

class Todo(Base): 
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    title: Mapped[str] = mapped_column(String(100),index=True)
    description: Mapped[str | None] = mapped_column(String(500),default=None)
    completed: Mapped[bool] = mapped_column(Boolean,default=False)
    priority: Mapped[Priority] = mapped_column(Enum(Priority),default=Priority.medium)
    due_date: Mapped[date | None] = mapped_column(Date,default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

def isTitleUnique(title: str,db: Session): 
    count = db.scalar(
        select(func.count()).select_from(
            Todo
        ).where(
            Todo.title.ilike(title)
        )
    )
    return count == 0

def process_and_check_title(title: str,db: Session): 
    title = title.strip()
    if not isTitleUnique(title,db): 
        raise exceptions.DuplicateTitle(title)
    if title == "": 
        raise exceptions.EmptyTitle()
    return title 