"""
Conexion y operaciones con la base de datos. SQLite

"""
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

# Accede a las variables
db_folder = os.getenv("DB_FOLDER", "data")
db_name = os.getenv("DB_NAME", "password.db")

# ruta donde se creara la base de datos
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    db_folder,
    db_name
)

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
