from fastapi import FastAPI 
from enum import Enum 
app = FastAPI()
class Unit(str,Enum): 
    km = "km"
    miles = "miles"

@app.get("/item/{item_id}")
def get_item(item_id: int): 
    return {"item_id": item_id}

@app.get("/unit/{unit}")
def pick(unit: Unit): 
    return {"unit": unit.value}

@app.get("/items")
def list_items(skip: int = 0 , limit: int = 10): 
    return {"skip":skip,"limit":limit}

