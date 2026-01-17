"""
Conexion y operaciones con la base de datos. SQLite

"""
import sqlite3
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Accede a las variables
db_folder = os.getenv("DB_FOLDER", "data")
db_name = os.getenv("DB_NAME", "password.db")

# ruta donde se creara la base de datos
"""DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    db_folder,
    db_name
)"""

def get_db_path():
    """
    Devuelve la ruta absoluta de la base de datos según si estamos
    ejecutando desde un .exe o desde Python normal.
    """
    if getattr(sys, "frozen", False):
        # Estamos ejecutando desde un .exe
        base_dir = os.path.dirname(sys.executable)
    else:
        # Ejecutando como script Python
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Carpeta donde se guardará la base de datos
    data_dir = os.path.join(base_dir, db_folder)
    os.makedirs(data_dir, exist_ok=True)  # crea la carpeta si no existe

    return os.path.join(data_dir, db_name)

# Ruta final de la base de datos
DB_PATH = get_db_path()

def init_db():
    """
    Inicializa la base de datos y crea la tabla de contraseñas si no existe.
    
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL )
        """)
    conn.commit()
    conn.close()

def save_password(site, username, password):
    """
    Guarda una contraseña en la base de datos.
    
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO passwords (site, username, password)
        VALUES (:site, :username, :password)
    """, {"site": site, "username": username, "password": password})
    conn.commit()
    conn.close()

       


def getAllPasswords():
    """
    Recupera todas las contraseñas de la base de datos.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT site, username, password FROM passwords")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_password(site, user):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE site=? AND username=?", (site, user))
    conn.commit()
    conn.close()

