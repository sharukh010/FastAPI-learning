from typing import Annotated
from fastapi import FastAPI,Query,Path

app = FastAPI()

@app.get("/search")
def search(
    q: Annotated[str,Query(min_length=2,max_length=50)],
    limit: Annotated[int,Query(ge=1,le=100)] = 10 
): 
    return {"q":q,"limit":limit}

@app.get("/products/{pid}")
def product(pid: Annotated[int,Path(gt=0)]): 
    return {"pid":pid}