"""
Punto de entrada a la aplicación GoliSafe.

"""

from backend.ui import start_app
from backend.crypto import generar_llave_maestra, cargar_llave_maestra

# Genera la llave solo si no existe
generar_llave_maestra()

# Carga la llave para usar en cifrado/descifrado
cipher = cargar_llave_maestra()

if __name__ == "__main__":
    start_app()
