from typing import Annotated 
from fastapi import FastAPI, Depends, Query


app = FastAPI()

# Dependency in class 
class Pagination: 
    def __init__(self,skip: int = 0 , limit: int = 10): 
        self.skip = skip 
        self.limit = limit 

# Dependency in functions
def common_params(q: str | None = None, skip : int = 0 , limit : int = 10): 
    return {"q":q,"skip":skip,"limit": limit}

# Validations with dependency 
def pagination(
        skip: Annotated[int, Query(ge=0)] = 0 , 
        limit: Annotated[int,Query(ge=1,le=100)] = 10 
): 
    return {"skip": skip, "limit": limit}

PaginationDep = Annotated[dict,Depends(pagination)]

@app.get("/items")
def list_items(params: Annotated[dict,Depends(common_params)]): 
    return params 

@app.get("/users")
def list_users(params: Annotated[dict,Depends(common_params)]): 
    return params 

@app.get("/products")
def list_products(p: PaginationDep): 
    return p