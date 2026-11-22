from app.schemas import SortBy, SortOrder, Priority
from datetime import date 
from fastapi import Query 

class FilterAndPagination:
    def __init__(
        self,
        completed: bool | None  = None ,
        priority: Priority | None = None , 
        search: str | None = Query(default=None,min_length=1),
        due_before: date | None = None, 
        due_after: date | None = None ,
        sort_by: SortBy = SortBy.created_at,
        order: SortOrder = SortOrder.asc , 
        limit: int = Query(default=10,ge=1,le=100),
        offset: int = Query(default=0,ge=0)
    ): 
        self.completed = completed 
        self.priority = priority 
        self.search = search 
        self.due_before = due_before 
        self.due_after = due_after 
        self.sort_by = sort_by
        self.order = order 
        self.limit = limit 
        self.offset = offset

FilteringAndPaginationDep = FilterAndPagination