from database import Base 
from sqlalchemy import String, Boolean , DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime,date , timezone 

class Todo(Base): 
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100),index=True)
    description: Mapped[str | None] = mapped_column(String(500),default=None)
    done: Mapped[bool] = mapped_column(Boolean,default=False)
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