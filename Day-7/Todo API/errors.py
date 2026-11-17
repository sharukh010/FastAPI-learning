class TodoNotFound(Exception): 
    def __init__(self,todo_id): 
        self.id = todo_id 
