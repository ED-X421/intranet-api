from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reemplaza este enlace por el CSV oficial de tu Google Sheets de Precios
URL_GOOGLE_SHEETS_CSV = "https://docs.google.com/spreadsheets/d/1FccGdJ1NfN-XsIL5cQomPf-Sw6eXM0Mb/edit?gid=1307404247#gid=1307404247"

@app.get("/")
def home():
    return {"status": "ok", "message": "API de Intranet activa"}

@app.get("/api/precios")
def obtener_precios():
    try:
        response = requests.get(URL_GOOGLE_SHEETS_CSV)
        if response.status_code != 200:
            return {"status": "error", "message": "No se pudo obtener el archivo de Google Sheets"}
        
        # Leer el CSV directamente desde Google Sheets
        df = pd.read_csv(io.StringIO(response.text))
        
        # Limpiar espacios en los nombres de las columnas
        df.columns = df.columns.str.strip()
        
        # Reemplazar valores nulos
        df = df.fillna("-")
        
        datos = df.to_dict(orient="records")
        return {"status": "ok", "data": datos}
    except Exception as e:
        return {"status": "error", "message": str(e)}
