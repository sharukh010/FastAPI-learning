from sqlalchemy import String, Boolean, Date , Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base 
from app.schemas import Priority
from datetime import date,datetime, timezone

class Todo(Base): 
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    title: Mapped[str] = mapped_column(String(100),index=True)
    description: Mapped[str] = mapped_column(String(500),default=None)
    completed: Mapped[bool] = mapped_column(Boolean,default=False)
    priority: Mapped[Priority] = mapped_column(Enum(Priority),default=Priority.medium)
    due_date: Mapped[date] = mapped_column(Date,default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )