"""
Funciones de cifrado y descifrado de datos. Cryptography

"""
from cryptography.fernet import Fernet
import os

# Obtener ruta absoluta a la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_LLAVE = os.path.join(BASE_DIR, "clave.key")

def generar_llave_maestra():
    """Genera una llave maestra y la guarda en un archivo solo si no existe."""
    if not os.path.exists(RUTA_LLAVE):
        key = Fernet.generate_key()
        with open(RUTA_LLAVE, "wb") as f:
            f.write(key)
        print("🔑 Llave maestra generada y guardada.")
    else:
        print("🔑 Llave maestra ya existe.")

def cargar_llave_maestra():
    """Carga la llave maestra desde el archivo y devuelve un objeto Fernet."""
    if not os.path.exists(RUTA_LLAVE):
        raise FileNotFoundError("No se encontró la llave maestra. Ejecuta generar_llave_maestra primero.")
    with open(RUTA_LLAVE, "rb") as f:
        key = f.read()
    return Fernet(key)