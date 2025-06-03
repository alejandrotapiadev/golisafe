# ![Vista previa del proyecto](assets/gifs/dflvh2b-b6b090a2-e2f1-4fe1-ac60-422c9d0de526.gif) Golisafe - Contraseñas de bolsillo

Aplicación de escritorio desarrollada en Python para gestionar contraseñas personales de forma segura. Utiliza una interfaz gráfica con Tkinter, almacenamiento local con SQLite y cifrado con la librería `cryptography`.

---

## 📦 Características

- Interfaz simple y amigable con Tkinter.
- Guarda información de:
  - Sitio web
  - Usuario
  - Contraseña (cifrada)
- Base de datos local con SQLite.
- Variables de configuración externas mediante archivo `.env`.

---

## 🛠️ Requisitos

- Python 3.8 o superior
- Entorno virtual (opcional pero recomendado)

---

## 🚀 Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/alejandrotapiadev/golisafe.git
cd golisafe
```
### 2. Crear y activar un entorno virtual

```bash
python -m venv venv 

venv\Scripts\activate # --> Activar en Windows

source venv/bin/activate # --> Activar en macOS/Linux 
```
### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python src/main.py
```
