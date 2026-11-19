from typing import Annotated
from fastapi import Cookie, Header, FastAPI, UploadFile, HTTPException, status, Response
from pathlib import Path 
import uuid
from datetime import datetime 

app = FastAPI()
UPLOAD_DIR = Path("Day-8/Practice/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def validate_api_key(api_key: str): 
    if api_key[:3] != "sha":
        return False 
    return True 

@app.get("/chat",status_code=200)
def chat(query: str , x_api_key: Annotated[str , Header()]): 
    if not validate_api_key(x_api_key): 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid API Key")
    return {"response":f"Here is the answer for your question {query}"}

@app.get("/last_upload")
def last_upload(last_upload: Annotated[str , Cookie()]):
    return {"last_upload": last_upload} 
    
@app.post("/files")
async def upload_files(files: list[UploadFile],response: Response): 
    for file in files: 
        data = await file.read()
        file_id = f"{uuid.uuid4().hex}{Path(file.filename).suffix}"
        (UPLOAD_DIR/file_id).write_bytes(data)
    response.set_cookie(key="last_upload",value=datetime.now().isoformat())
    return {"msg": "all files uploaded successfully"}