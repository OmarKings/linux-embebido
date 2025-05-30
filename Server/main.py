
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Servidor DropAir",
    version="beta 0.0.1",
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/test/", status_code=200)
def test_endpoint(request: Request):
    return {"mensaje": "Todo OK ✅"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)
"""


# Airdop para programadores
import os
import shutil

from fastapi import FastAPI

from fastapi import File
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from starlette.requests import Request

UPLOADS_FOLDER = './Server/'

app = FastAPI(

    title="Servidor DropAir",
    version="beta  0.0.1",

)

@app.get('/test/',status_code=200)
def test_endpoint(request:Request):
    return "()"

@app.get('/', response_class=HTMLResponse)
def upload_file_v2():
    content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Página Bonita</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-indigo-200 via-purple-100 to-pink-200 min-h-screen flex items-center justify-center">
  <div class="bg-white/80 backdrop-blur-lg rounded-2xl shadow-2xl p-10 max-w-lg text-center">
    <h1 class="text-4xl font-bold text-indigo-600 mb-4">¡Hola, programador!</h1>
    <p class="text-lg text-gray-700 mb-6">
      Bienvenido a DropAir, tu sistema de envío fácil de archivos. 🚀
    </p>
    <form action="/upload-file/" method="post" enctype="multipart/form-data" class="inline-block">
      <input type="file" name="file" class="mb-4">
      <button type="submit" class="bg-indigo-500 hover:bg-indigo-600 text-white px-6 py-3 rounded-full font-semibold transition">
        Subir archivo
      </button>
    </form>
  </div>
</body>
</html>
"""

    return content



@app.post('/upload-file/', status_code=201)
def upload_file(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOADS_FOLDER,exist_ok=True)
        filepath = os.path.join(UPLOADS_FOLDER, file.filename)
        with open(filepath, 'w') as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail='COULD YOU UPLOAD YOUR FILE!')


    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=9090)