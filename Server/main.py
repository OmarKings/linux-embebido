from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import RPi.GPIO as GPIO

app = FastAPI()
GPIO.setmode(GPIO.BCM)

# Configura los pines GPIO para relés
RELAY_PINS = [17, 27, 22, 5]
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Inicialmente apagado

# Carpeta para archivos
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Montar frontend estático
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Encender o apagar relés
@app.post("/relay/{index}/on")
def relay_on(index: int):
    if 0 <= index < len(RELAY_PINS):
        GPIO.output(RELAY_PINS[index], GPIO.HIGH)
        return {"status": "ON"}
    return {"error": "Índice fuera de rango"}

@app.post("/relay/{index}/off")
def relay_off(index: int):
    if 0 <= index < len(RELAY_PINS):
        GPIO.output(RELAY_PINS[index], GPIO.LOW)
        return {"status": "OFF"}
    return {"error": "Índice fuera de rango"}

# Subir archivo
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return {"filename": file.filename}

# Listar archivos
@app.get("/files")
def list_files():
    return os.listdir(UPLOAD_FOLDER)

# Descargar archivo
@app.get("/files/{filename}")
def get_file(filename: str):
    return FileResponse(os.path.join(UPLOAD_FOLDER, filename))

# Eliminar archivo
@app.delete("/files/{filename}")
def delete_file(filename: str):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        return {"status": "Archivo eliminado"}
    return {"error": "Archivo no encontrado"}
