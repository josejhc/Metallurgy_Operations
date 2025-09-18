from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import List
import pandas as pd
from pathlib import Path
import os

# Clear console (optional)
os.system('cls')

app = FastAPI()

# Base directory
dir = Path.cwd()

# Path to the Excel file
dir_excel = dir / 'data_bases' / 'Calendario_pruebas.xlsm'
print(dir_excel)

# Path to the reports folder
dir_reportes = dir / 'reportes'

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Excel file on startup
df = pd.read_excel(str(dir_excel), sheet_name=1, keep_default_na=False, na_values=[])
col = df.columns
@app.get("/pruebas", response_model=List[str])
def obtener_pruebas():
    pruebas = df['Prueba'].dropna().unique().tolist()
    return pruebas

@app.get("/datos/{nombre_prueba}")
def obtener_datos_por_prueba(nombre_prueba: str):
    datos = df[df['Prueba'] == nombre_prueba]
    if datos.empty:
        return JSONResponse(
            content={"error": "No data found for that test"},
            status_code=404
        )
    return {
        "columnas": list(df.columns),
        "datos": datos.to_dict(orient="records")
    }

@app.get("/reporte/{nombre_prueba}")
def descargar_reporte(nombre_prueba: str):
    archivo_pdf = dir_reportes / f"{nombre_prueba}.pdf"

    if not archivo_pdf.exists():
        return JSONResponse(
            content={"error": "Report does not exist"},
            status_code=404
        )

    return FileResponse(
        path=archivo_pdf,
        filename=f"{nombre_prueba}.pdf",
        media_type='application/pdf'
    )

import sys
print(sys.version)
