from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import RPi.GPIO as GPIO

app = FastAPI()

# Habilitar CORS (opcional, pero evita bloqueos desde otro origen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Configuraci�n de GPIO ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
RELAY_PINS = [17, 27, 22, 5]
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# === Ruta absoluta para "uploads/" ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(CURRENT_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print("Guardando archivos en:", UPLOAD_FOLDER)

# === ENDPOINTS ANTES DE MONTAR STATIC ===

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    print("Recibiendo archivo:", file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    print("Guardado en:", file_path)
    return {"filename": file.filename}

@app.get("/files")
def list_files():
    return os.listdir(UPLOAD_FOLDER)

@app.get("/files/{filename}")
def get_file(filename: str):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "Archivo no encontrado"}

@app.delete("/files/{filename}")
def delete_file(filename: str):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        return {"status": "Archivo eliminado"}
    return {"error": "Archivo no encontrado"}

@app.post("/relay/{index}/on")
def relay_on(index: int):
    if 0 <= index < len(RELAY_PINS):
        GPIO.output(RELAY_PINS[index], GPIO.HIGH)
        return {"status": f"Relay {index} ON"}
    return {"error": "�ndice fuera de rango"}

@app.post("/relay/{index}/off")
def relay_off(index: int):
    if 0 <= index < len(RELAY_PINS):
        GPIO.output(RELAY_PINS[index], GPIO.LOW)
        return {"status": f"Relay {index} OFF"}
    return {"error": "�ndice fuera de rango"}

# === Montar frontend React compilado al final ===
STATIC_DIR = os.path.join(CURRENT_DIR, "static")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
