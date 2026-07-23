from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# Permitir solicitudes desde cualquier origen (Google Sites / iframes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ok", "message": "API de Intranet activa"}

@app.get("/api/precios")
def obtener_precios():
    archivo = "Precios_y_Cantidades.xlsx"
    
    if not os.path.exists(archivo):
        return {"status": "error", "message": f"Archivo {archivo} no encontrado"}
        
    try:
        # Leer el Excel omitiendo la primera fila de título corporativo
        df = pd.read_excel(archivo, skiprows=1)
        
        # Limpiar encabezados de espacios sobrantes
        df.columns = df.columns.str.strip()
        
        # Reemplazar valores nulos para evitar errores JSON
        df = df.fillna("-")
        
        datos = df.to_dict(orient="records")
        return {"status": "ok", "data": datos}
    except Exception as e:
        return {"status": "error", "message": str(e)}
