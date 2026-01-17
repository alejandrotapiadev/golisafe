"""
Interfaz de usuario minimalista para GoliSafe - Mejorada
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from screeninfo import get_monitors
from backend.database import init_db, save_password, getAllPasswords, delete_password
import os
import sys

from frontend import app

def resource_path(relative_path):
    """
    Devuelve la ruta absoluta a un recurso,
    compatible con PyInstaller (.exe) y desarrollo normal.
    """
    try:
        # PyInstaller crea una carpeta temporal con los assets
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def start_app():
    init_db()

    # ==============================
    # CONFIGURACIÓN INICIAL
    # ==============================
    ctk.set_appearance_mode("dark")   # "light", "dark" o "system"
    ctk.set_default_color_theme("green")  # puedes usar "dark-blue" o crear un tema propio

    app = ctk.CTk()
    app.title("GoliSafe")
    app.geometry("700x500")
    app.minsize(600, 400)

    # Icono
    icon_path = resource_path("assets/icon/logo4.ico")
    app.iconbitmap(icon_path)

    # Tipografía base
    font_title = ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
    font_text = ctk.CTkFont(family="Segoe UI", size=15)
    accent_color = "#7f5af0"

    # ==============================
    # FUNCIONES AUXILIARES
    # ==============================
    def mostrar_frame(frame):
        for f in (frame_home, frame_guardar, frame_ver):
            f.pack_forget()
        frame.pack(fill="both", expand=True, padx=30, pady=20)

    # ==============================
    # BARRA DE NAVEGACIÓN
    # ==============================
    nav_bar = ctk.CTkFrame(app, fg_color="#1e1e1e", height=60, corner_radius=0)
    nav_bar.pack(fill="x")

    titulo = ctk.CTkLabel(nav_bar, text="GoliSafe", font=font_title, text_color=accent_color)
    titulo.pack(side="left", padx=20)

    def boton_nav(texto, comando):
        return ctk.CTkButton(
            nav_bar, text=texto, command=comando, width=120, height=35,
            fg_color="transparent", hover_color="#2b2b2b",
            text_color="#d6d6d6", corner_radius=10
        )

    boton_home = boton_nav("Inicio", lambda: mostrar_frame(frame_home))
    boton_home.pack(side="right", padx=10)
    boton_ver = boton_nav("Ver Contraseñas", lambda: [cargar_contrasenas(), mostrar_frame(frame_ver)])
    boton_ver.pack(side="right", padx=10)
    boton_guardar = boton_nav("Guardar", lambda: mostrar_frame(frame_guardar))
    boton_guardar.pack(side="right", padx=10)

    # ==============================
    # FRAME: INICIO
    # ==============================
    frame_home = ctk.CTkFrame(app, fg_color="#161616")
    label_bienvenida = ctk.CTkLabel(
        frame_home, text="Bienvenido a GoliSafe 🛡️",
        font=font_title, text_color="white"
    )
    label_bienvenida.pack(pady=(100, 10))
    label_desc = ctk.CTkLabel(
        frame_home, text="Tu gestor de contraseñas personal, seguro y minimalista.",
        font=font_text, text_color="#b3b3b3"
    )
    label_desc.pack(pady=5)

    # ==============================
    # FRAME: GUARDAR CONTRASEÑA
    # ==============================
    frame_guardar = ctk.CTkFrame(app, fg_color="#161616")

    def crear_campo(parent, texto, placeholder=""):
        lbl = ctk.CTkLabel(parent, text=texto, font=font_text, text_color="#e5e5e5")
        lbl.pack(pady=(10, 2))
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder,
            width=300, height=35,
            fg_color="#1e1e1e", border_color="#3c3c3c",
            text_color="white", corner_radius=8
        )
        entry.pack(pady=(0, 5))
        return entry

    entry_site = crear_campo(frame_guardar, "Sitio web:", "Ej. github.com")
    entry_user = crear_campo(frame_guardar, "Usuario:", "Tu nombre de usuario")
    entry_pass = crear_campo(frame_guardar, "Contraseña:", "Tu contraseña segura")

    def guardar_contrasena():
        site, user, pwd = entry_site.get(), entry_user.get(), entry_pass.get()
        if site and user and pwd:
            save_password(site, user, pwd)
            messagebox.showinfo("Éxito", "Contraseña guardada correctamente.")
            entry_site.delete(0, tk.END)
            entry_user.delete(0, tk.END)
            entry_pass.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Completa todos los campos antes de guardar.")

    boton_guardar_ok = ctk.CTkButton(
        frame_guardar, text="Guardar Contraseña", command=guardar_contrasena,
        fg_color=accent_color, hover_color="#6c47d9", text_color="white",
        width=200, height=40, corner_radius=12, font=font_text
    )
    boton_guardar_ok.pack(pady=20)

    # ==============================
    # FRAME: VER CONTRASEÑAS
    # ==============================
    frame_ver = ctk.CTkFrame(app, fg_color="#161616")

    campo_busqueda = ctk.CTkEntry(
        frame_ver, placeholder_text="Buscar por sitio o usuario...",
        width=400, height=35, fg_color="#1e1e1e", border_color="#3c3c3c",
        text_color="white", corner_radius=8
    )
    campo_busqueda.pack(pady=15)

    columnas = ("Sitio", "Usuario", "Contraseña")
    tree = ttk.Treeview(frame_ver, columns=columnas, show="headings", height=12)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#1e1e1e", foreground="white",
                    rowheight=28, fieldbackground="#1e1e1e", borderwidth=0)
    style.map("Treeview", background=[("selected", accent_color)])
    style.configure("Treeview.Heading", background="#2a2a2a", foreground="white", font=("Segoe UI", 11, "bold"))

    def cargar_contrasenas():
        filtro = campo_busqueda.get().strip().lower()
        for item in tree.get_children():
            tree.delete(item)
        contras = getAllPasswords()
        for site, user, pwd in contras:
            if filtro in site.lower() or filtro in user.lower():
                tree.insert("", "end", values=(site, user, pwd))

    def eliminar_contrasena():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona una contraseña para eliminar.")
            return
        site, user, _ = tree.item(sel[0], "values")
        if messagebox.askyesno("Confirmar", f"¿Eliminar la contraseña para {site}?"):
            delete_password(site, user)
            cargar_contrasenas()

    frame_botones = ctk.CTkFrame(frame_ver, fg_color="#161616")
    frame_botones.pack(pady=10)
    ctk.CTkButton(frame_botones, text="Eliminar", command=eliminar_contrasena,
                  fg_color="#2e2e2e", hover_color="#3b3b3b",
                  text_color="white", width=150).pack(side="left", padx=5)
    ctk.CTkButton(frame_botones, text="Actualizar", command=cargar_contrasenas,
                  fg_color=accent_color, hover_color="#6c47d9",
                  text_color="white", width=150).pack(side="left", padx=5)

    # ==============================
    # INICIO APP
    # ==============================
    mostrar_frame(frame_home)
    app.mainloop()
