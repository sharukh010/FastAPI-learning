from typing import Annotated , Literal
from fastapi import FastAPI ,Depends, Query , HTTPException, Header

app = FastAPI()

PRODUCTS = [
     {"id": 1, "name": "Laptop", "price": 900},
    {"id": 2, "name": "Mouse", "price": 20},
    {"id": 3, "name": "Keyboard", "price": 50},
    {"id": 4, "name": "Monitor", "price": 250},
    {"id": 5, "name": "Webcam", "price": 60},
]

USERS = [
    {"id":1,"name":"Alex","age":23},
    {"id":2,"name":"Bob","age":23},
    {"id":3,"name":"Charlie","age":13},
    {"id":4,"name":"Dan","age":43},
    {"id":5,"name":"Eve","age":34},
]

def get_current_user(x_token: Annotated[str | None,Header()]= None ): 
    if x_token is None: 
        raise HTTPException(400,f"Authentication failed")
    return {"x_token": x_token}

class ListParams:
    def __init__(
            self,
            skip: Annotated[int, Query(ge=0)] = 0 , 
            limit: Annotated[int, Query(ge=1,le=100)] = 10, 
            sort_by: str = "id",
            order: Literal["asc","desc"] = "asc",
    ): 
        self.skip, self.limit = skip , limit 
        self.sort_by, self.order = sort_by , order 

    def apply(self,items: list[dict]) -> list[dict]: 
        if items and self.sort_by not in items[0]: 
            raise HTTPException(400,f"Cannot sort by '{self.sort_by}'")
        items = sorted(items,key=lambda x: x[self.sort_by],reverse=self.order == "desc")
        return items[self.skip: self.skip+self.limit]

class ListParamsWithSearch(ListParams): 
    def __init__(
            self,
            search: Annotated[str | None, Query(min_length=1,max_length=30)] = None , 
            skip: Annotated[int, Query(ge=0)] = 0 , 
            limit: Annotated[int, Query(ge=1,le=100)] = 10 , 
            sort_by: str = "id",
            order: Literal["asc","desc"] = "asc",
    ): 
        super().__init__(skip,limit,sort_by,order)
        self.search = search 

    def apply(self,items: list[dict]) -> list[dict]: 
        if items and self.sort_by not in items[0]: 
            raise HTTPException(400, f"Cannot sort by '{self.sort_by}'")
        if self.search is not None: 
            items = [i for i in items if i["name"].lower() == self.search.lower()]
        items = sorted(
            items,
            key=lambda x: x[self.sort_by],
            reverse = self.order == "desc"
        )
        return items[self.skip: self.skip+self.limit]
SortAndPaginationDep = Annotated[ListParams, Depends()]
SearchListDep = Annotated[ListParamsWithSearch,Depends()]

@app.get("/products")
def list_products(p: SortAndPaginationDep): 
    return p.apply(PRODUCTS)

@app.get("/users")
def list_users(p: SearchListDep): 
    return p.apply(USERS)

@app.get("/current_user")
def current_user(user: Annotated[dict,Depends(get_current_user)]): 
    return user["x_token"]