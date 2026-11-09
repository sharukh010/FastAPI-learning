from fastapi import FastAPI 
from datetime import datetime  
import random 
app = FastAPI(title="Personal Info API",description="Day-1 Project",version="0.1.0")
start_time = datetime.now()
quotes = [
    "Never Settle for average",
    "Comfort kills talent",
    "Simple is better than complex",
    "Greatness comes from simplicity",
    "Start from 0 build to 100"
]
skills_list = ["Teaching","Python","Machine Learning","DSA","C++","Java"]
@app.get("/",summary="API Endpoints",tags=["Info"])
def root(): 
    return {
        "message": "Welcome to my Personal Info API",
        "docs": "/docs",
        "endpoints":["/health","/about","/time","/quote","/skills","/uptime"]
    }

@app.get("/health",summary="Health Check",tags=["Utility"])
def health(): 
    return {"status":"ok"}

@app.get("/about",summary="About Me",tags=["Info"])
def about():
    return {
        "app":"Personal Info API",
        "version":"0.1.0",
        "author":"Pathan Sharukh Khan",
        "description":"Day-1 project"
    }

@app.get("/time",summary="Current Time",tags=["Utility"])
def time(): 
    return {
        "server_time":datetime.now().isoformat()
    }

@app.get("/quote",summary="Random Quote",tags=["Utility"])
def quote():
    return {
        "quote":random.choice(quotes)
    }

@app.get("/skills",summary="My Skills",tags=["Info"])
def skills():
    return {
        "count":len(skills_list),
        "skills":skills_list
    }

@app.get("/uptime",summary="Server Uptime",tags=["Utility"])
def uptime():
    now = datetime.now()
    
    return {
        "uptime_seconds": f"{(now - start_time).total_seconds():.1f}" 
    }