# scripts/siigo_auth.py
import json
import requests

SIIGO_AUTH_URL = "https://api.siigo.com/auth"
SIIGO_USERNAME = "sandbox@siigoapi.com"  # Usa el tuyo en producción
SIIGO_ACCESS_KEY = "NDIlMzI0MmEtNjExZC00NGM3LWE3OTQtMWUyNTNlZWU0ZTM0OkosU2MwLD4xQ08="  # Reemplaza por tu clave real

def obtener_token_siigo():
    headers = {
        "Content-Type": "application/json",
        "Partner-Id": "mi_aplicacion_django"  # Cambia por el nombre real de tu app si es necesario
    }

    data = {
        "username": SIIGO_USERNAME,
        "access_key": SIIGO_ACCESS_KEY
    }

    response = requests.post(SIIGO_AUTH_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        if token:
            return token
        else:
            raise ValueError("Token no encontrado en la respuesta.")
    else:
        raise ConnectionError(f"Error autenticando con Siigo: {response.status_code} - {response.text}")
