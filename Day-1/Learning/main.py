from fastapi import FastAPI 
from datetime import datetime
app = FastAPI(title="Day 1 API")

@app.get("/")
def root():
    return {"message":"Hello, FastAPI!"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/about")
def about(): 
    return {"app name":"Day-1 API","version":"0.0.0"}

@app.get("/time")
def time():
    return {"time": datetime.now().isoformat()}