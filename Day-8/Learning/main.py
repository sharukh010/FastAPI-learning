from typing import Annotated 
from fastapi import FastAPI,Header,Response,Cookie,Form  

app = FastAPI() 

@app.get("/agent")
def agent(user_agent: Annotated[str | None,Header()] = None,
          x_token: Annotated[str | None, Header()] = None): 
    return {"user_agent": user_agent,"x_token": x_token}

@app.get("/h")
def h(response: Response): 
    response.headers["X-App"] = "demo"
    return {"ok": True}


# Cookies 
@app.get("/me")
def me(session_id: Annotated[str | None, Cookie()] = None): 
    return {"session_id": session_id}

@app.post("/login-cookie")
def set_cookie(response: Response): 
    response.set_cookie(key="session_id",value="abc123",httponly=True)
    return {"msg": "cookie set"}

@app.post("/logout-cookie")
def del_cookie(response: Response): 
    response.delete_cookie("session_id")
    return {"msg": "cookie removed"}

#Form Data 
@app.post("/login")
def login(username: Annotated[str, Form()], password: Annotated[str, Form()]): 
    return {"username": username}