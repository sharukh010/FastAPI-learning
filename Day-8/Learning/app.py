import uuid 
from pathlib import Path 
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse


app = FastAPI(title="File Upload/Download Service")

UPLOAD_DIR = Path("Day-8/Learning/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED = {"image/png","image/jpeg","application/PDF","text/plain"} #supported files 
MAX_SIZE = 5 * 1024 * 1024 # 5MB

@app.post("/files",status_code=201)
async def upload(file: UploadFile): 
    if file.content_type not in ALLOWED: 
        raise HTTPException(415,"File type not allowed")
    data = await file.read() 
    if len(data) > MAX_SIZE: 
        raise HTTPException(413,"File too large (max 5MB)")
    file_id = f"{uuid.uuid4().hex}{Path(file.filename).suffix}"
    (UPLOAD_DIR/file_id).write_bytes(data)
    return {"id": file_id, "original_name": file.filename,"size":len(data)}

@app.get("/files")
def list_files(): 
    return [{"id":p.name,"size":p.stat().st_size} for p in UPLOAD_DIR.iterdir()]

@app.get("/files/{file_id}")
def get_file(file_id: str): 
    path = UPLOAD_DIR / Path(file_id).name #Path().name picks last part of the file_id to avoid user to access files outside upload folder 
    if not path.is_file(): 
        raise HTTPException(404,"File not found")
    return FileResponse(path)


@app.delete("/files/{file_id}",status_code=204)
def delete_file(file_id: str): 
    path = UPLOAD_DIR / Path(file_id).name 
    if not path.is_file(): 
        raise HTTPException(404,"File not found")
    path.unlink()