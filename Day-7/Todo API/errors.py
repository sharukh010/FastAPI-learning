class TodoNotFound(Exception): 
    def __init__(self,todo_id): 
        self.id = todo_id 
class DuplicateTitle(Exception): 
    def __init__(self,title): 
        self.title = title 