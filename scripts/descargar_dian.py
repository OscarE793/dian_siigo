# scripts/descargar_dian.py
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ruta del chromedriver
CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), '..', 'chromedriver.exe')

# Carpeta donde se guardan los archivos descargados
DOWNLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'descargas_facturas'))
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def ejecutar_con_token(url_token: str, fecha_documentos):
    print("Ejecutando Selenium con token...")

    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    })
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # opcional para no abrir el navegador

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Ingresar con el token
        driver.get(url_token)
        print("Accediendo al portal con token...")
        time.sleep(5)  # Esperar a que cargue el portal

        # Ir al menú "Histórico > Documentos recibidos"
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Histórico')]/.."))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Documentos recibidos')]"))
        ).click()

        print("Entrando a Documentos recibidos...")
        time.sleep(5)

        # Seleccionar rango de fechas
        fecha_inicio = fecha_documentos.strftime("%Y/%m/%d")
        fecha_fin = fecha_documentos.strftime("%Y/%m/%d")

        # Asumimos campos de fecha por su posición. Ajusta según IDs reales si los conoces.
        campos_fecha = driver.find_elements(By.XPATH, "//input[contains(@placeholder, 'YYYY/MM/DD')]")
        if len(campos_fecha) >= 2:
            campos_fecha[0].clear()
            campos_fecha[0].send_keys(fecha_inicio)
            campos_fecha[1].clear()
            campos_fecha[1].send_keys(fecha_fin)

        # Clic en Buscar
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Buscar')]"))
        ).click()

        print("Buscando documentos...")
        time.sleep(5)

        # Descargar ZIPs de facturas
        botones_descarga = driver.find_elements(By.XPATH, "//button[contains(@title, 'Descargar elementos') or contains(@aria-label, 'Descargar')]")
        for boton in botones_descarga:
            boton.click()
            print("Descargando archivo ZIP...")
            time.sleep(4)

    except Exception as e:
        print("Error en Selenium:", str(e))
        raise

    finally:
        driver.quit()
        print("Proceso Selenium finalizado.")
