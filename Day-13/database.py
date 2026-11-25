from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine 


engine = create_engine("sqlite:///Day-13/blogs.db",connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(bind=engine,autoflush=False)

def get_db(): 
    db = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close()