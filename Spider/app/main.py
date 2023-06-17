from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

app = FastAPI()
app.mount("/templates", StaticFiles(directory=os.path.join(os.path.dirname(__file__),'templates')), name="templates")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__),'static')), name="static")

@app.get("/",response_class=HTMLResponse)
async def index():
    file=open(os.path.join('templates','index.html'),'r',encoding='utf-8').read()
    return file

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)