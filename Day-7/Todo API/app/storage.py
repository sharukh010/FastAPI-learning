from datetime import date, datetime
from zoneinfo import ZoneInfo
from app.schemas import Todo, Priority
import app.exceptions as exceptions 

def isTitleUnique(title: str): 
    if not any(title.lower().replace(" ","") == t.title.lower().replace(" ","") for t in todos.values()): 
        return True 
    return False 

def process_and_check_title(title: str): 
    title = title.strip()
    if not isTitleUnique(title): 
        raise exceptions.DuplicateTitle(title)
    if title == "": 
        raise exceptions.EmptyTitle()
    return title 

zone = ZoneInfo("Asia/Kolkata")

todos: dict[int, Todo] = {
    1: Todo(id=1, title="Finish FastAPI Day 7 project", description="Build the todo API with filtering and search",
            completed=False, priority=Priority.high, due_date=date(2026, 11, 20),
            created_at=datetime(2026, 11, 17, 9, 0, tzinfo=zone), updated_at=datetime(2026, 11, 17, 9, 0, tzinfo=zone)),
    2: Todo(id=2, title="Prepare Python lesson for UK student", description="Loops and functions practice worksheet",
            completed=False, priority=Priority.high, due_date=date(2026, 11, 19),
            created_at=datetime(2026, 11, 17, 9, 15, tzinfo=zone), updated_at=datetime(2026, 11, 17, 9, 15, tzinfo=zone)),
    3: Todo(id=3, title="Review Bebras past paper", description="Go through logic and pattern questions",
            completed=True, priority=Priority.medium, due_date=date(2026, 11, 15),
            created_at=datetime(2026, 11, 12, 8, 30, tzinfo=zone), updated_at=datetime(2026, 11, 15, 19, 45, tzinfo=zone)),
    4: Todo(id=4, title="Pay credit card bill", description=None,
            completed=False, priority=Priority.high, due_date=date(2026, 11, 16),
            created_at=datetime(2026, 11, 13, 10, 0, tzinfo=zone), updated_at=datetime(2026, 11, 13, 10, 0, tzinfo=zone)),
    5: Todo(id=5, title="Practice Linux commands", description="30 minutes: ls, cd, grep, chmod",
            completed=False, priority=Priority.medium, due_date=date(2026, 11, 25),
            created_at=datetime(2026, 11, 14, 7, 45, tzinfo=zone), updated_at=datetime(2026, 11, 14, 7, 45, tzinfo=zone)),
    6: Todo(id=6, title="Read Pydantic validation tutorial", description="Field, validators and nested models",
            completed=True, priority=Priority.low, due_date=None,
            created_at=datetime(2026, 11, 11, 18, 20, tzinfo=zone), updated_at=datetime(2026, 11, 12, 21, 10, tzinfo=zone)),
    7: Todo(id=7, title="Buy groceries", description="Rice, vegetables, milk, eggs",
            completed=False, priority=Priority.low, due_date=date(2026, 11, 18),
            created_at=datetime(2026, 11, 17, 20, 0, tzinfo=zone), updated_at=datetime(2026, 11, 17, 20, 0, tzinfo=zone)),
    8: Todo(id=8, title="Push Day 6 code to GitHub", description="Library API with error handling",
            completed=True, priority=Priority.medium, due_date=date(2026, 11, 14),
            created_at=datetime(2026, 11, 13, 16, 0, tzinfo=zone), updated_at=datetime(2026, 11, 14, 12, 30, tzinfo=zone)),
    9: Todo(id=9, title="Plan UK AIO session for student", description="Cover machine learning basics and past questions",
            completed=False, priority=Priority.medium, due_date=date(2026, 11, 28),
            created_at=datetime(2026, 11, 15, 11, 0, tzinfo=zone), updated_at=datetime(2026, 11, 16, 9, 30, tzinfo=zone)),
    10: Todo(id=10, title="Improve spoken English", description="Record a 5 minute explanation and review it",
             completed=False, priority=Priority.low, due_date=None,
             created_at=datetime(2026, 11, 16, 7, 0, tzinfo=zone), updated_at=datetime(2026, 11, 16, 7, 0, tzinfo=zone)),
    11: Todo(id=11, title="Start deep learning with Keras", description="Install TensorFlow and run the first model",
             completed=False, priority=Priority.medium, due_date=date(2026, 12, 5),
             created_at=datetime(2026, 11, 16, 21, 0, tzinfo=zone), updated_at=datetime(2026, 11, 16, 21, 0, tzinfo=zone)),
    12: Todo(id=12, title="Review Day 6 error handlers", description="Revisit the 404, 409 and 422 handling",
             completed=False, priority=Priority.low, due_date=date(2026, 11, 22),
             created_at=datetime(2026, 11, 17, 22, 0, tzinfo=zone), updated_at=datetime(2026, 11, 17, 22, 0, tzinfo=zone)),
}

next_id = 13