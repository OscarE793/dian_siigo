# scripts/subir_a_siigo.py
import os
import json
import requests
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))



from siigo_auth import obtener_token_siigo
SIIGO_URL_BASE = "https://api.siigo.com/auth"
TOKEN = "NDllMzI0NmEtNjExZC00NGM3LWE3OTQtMWUyNTNlZWU0ZTM0OkosU2MwLD4xQ08="  # Reemplázalo por el real o usa variables de entorno

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

CARPETA_PROCESADAS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'facturas_procesadas'))


def cargar_facturas_procesadas():
    archivos = [f for f in os.listdir(CARPETA_PROCESADAS) if f.endswith('.xlsx')]
    for archivo in archivos:
        ruta = os.path.join(CARPETA_PROCESADAS, archivo)
        print(f"Cargando archivo: {archivo}")
        df = pd.read_excel(ruta)
        for _, fila in df.iterrows():
            data = construir_payload_siigo(fila)
            if data:
                enviar_factura_siigo(data)


def construir_payload_siigo(fila):
    try:
        return {
            "document": {
                "id": 22883  # ID del tipo de documento (ajústalo a tu caso)
            },
            "date": pd.to_datetime(fila['Fecha Emisión']).strftime("%Y-%m-%d"),
            "customer": {
                "identification": str(fila['NIT Emisor']),
                "name": fila.get("Nombre Emisor", "No identificado")
            },
            "items": [
                {
                    "code": fila.get("Prefijo", "ITEM"),
                    "description": fila.get("Tipo de documento", "Factura Electrónica"),
                    "quantity": 1,
                    "price": 1000.0  # Valor ficticio, reemplaza si tienes el valor real
                }
            ],
            "payments": [
                {
                    "value": 1000.0,
                    "due_date": pd.to_datetime(fila['Fecha Emisión']).strftime("%Y-%m-%d"),
                    "payment_method": {"id": 1}
                }
            ]
        }
    except Exception as e:
        print(f"Error construyendo payload: {e}")
        return None


def enviar_factura_siigo(payload):
    try:
        response = requests.post(f"{SIIGO_URL_BASE}/invoices", headers=HEADERS, json=payload)
        if response.status_code == 201:
            print("✅ Factura registrada exitosamente.")
        else:
            print(f"❌ Error en el envío: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error al conectar con Siigo: {e}")


if __name__ == "__main__":
    cargar_facturas_procesadas()
