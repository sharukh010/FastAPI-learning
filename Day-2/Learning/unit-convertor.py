from enum import Enum 
from typing import Annotated
from fastapi import FastAPI,Query 

app = FastAPI(title="Unit Convertor")

class Distance(str,Enum): 
    km = "km"
    miles = "miles"

class Temp(str,Enum): 
    c = "c"
    f = "f"

@app.get("/convert/distance/{unit}")
def convert_distance(unit: Distance,value: Annotated[float,Query(ge=0)],decimals: Annotated[int, Query(ge=0,le=6)] = 2): 
    if unit == Distance.km: 
        return {
            "input": f"{value} km",
            "result": round(value * 0.62137,decimals),
            "unit":"miles"
        }
    return {
        "input": f"{value} miles",
        "result": round(value/0.62137,decimals),
        "unit":"km"
    }

@app.get("/convert/temperature/{unit}")
def convert_temperature(unit: Temp,value: float,decimals: Annotated[int, Query(ge=0,le=6)] = 2 ): 
    if unit == Temp.c: 
        return {
            "result": round(value * 9/5+32,2),
            "unit":"f"
        }
    return {
        "result":round((value-32)*5/9,2),
        "unit": "c"
    }

@app.get("/convert/batch/{unit}")
def batch(unit: Distance,values: Annotated[list[float],Query(max_length=10)],decimals: Annotated[int, Query(ge=0,le=6)] = 2): 
    factor = 0.621371 if unit == Distance.km else 1/0.621371
    return {"results": [round(v*factor,4) for v in values]}