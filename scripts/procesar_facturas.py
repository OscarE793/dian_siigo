# scripts/procesar_facturas.py
import os
import zipfile
import pandas as pd
from datetime import datetime

# Ruta donde se descargan los ZIP o Excel
BASE_DIR = os.path.dirname(__file__)
CARPETA_DESCARGAS = os.path.abspath(os.path.join(BASE_DIR, '..', 'descargas_facturas'))
CARPETA_PROCESADAS = os.path.abspath(os.path.join(BASE_DIR, '..', 'facturas_procesadas'))
os.makedirs(CARPETA_PROCESADAS, exist_ok=True)

def procesar_zip_y_extraer_datos():
    print("Procesando archivos descargados...")

    for archivo in os.listdir(CARPETA_DESCARGAS):
        ruta_archivo = os.path.join(CARPETA_DESCARGAS, archivo)

        if archivo.endswith(".zip"):
            print(f"Descomprimiendo: {archivo}")
            with zipfile.ZipFile(ruta_archivo, 'r') as zip_ref:
                zip_ref.extractall(CARPETA_PROCESADAS)

        elif archivo.endswith(".xlsx") or archivo.endswith(".xls"):
            print(f"Leyendo Excel: {archivo}")
            df = pd.read_excel(ruta_archivo)
            guardar_excel_limpio(df, archivo)

def guardar_excel_limpio(df: pd.DataFrame, nombre_origen):
    columnas_interes = [
        'Tipo de documento', 'CUFE/CUDE', 'Folio', 'Prefijo',
        'Divisa', 'Forma de Pago', 'Medio de Pago',
        'Fecha Emisión', 'Fecha Recepción',
        'NIT Emisor', 'Nombre Emisor'
    ]

    columnas_encontradas = [col for col in columnas_interes if col in df.columns]

    if not columnas_encontradas:
        print("⚠️  El archivo no tiene las columnas esperadas.")
        return

    df_filtrado = df[columnas_encontradas].copy()
    nombre_salida = f"procesado_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nombre_origen}"
    ruta_salida = os.path.join(CARPETA_PROCESADAS, nombre_salida)
    df_filtrado.to_excel(ruta_salida, index=False)
    print(f"Archivo procesado guardado en: {ruta_salida}")

if __name__ == '__main__':
    procesar_zip_y_extraer_datos()
