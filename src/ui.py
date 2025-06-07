"""
Interfaz de usuario para GoliSafe. Tkinter

"""
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk  # necesario para usar tk.END
from database import init_db, save_password
import os

def start_app():
    init_db()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("GoliSafe")
    app.geometry("300x200")
    app.resizable(False, False)
    

# Establecer icono de la aplicación
    base_dir = os.path.dirname(os.path.abspath(__file__))  # ruta carpeta src
    icon_path = os.path.join(base_dir, "..", "assets", "icon", "golisopod.ico")
    icon_path = os.path.normpath(icon_path)  # para normalizar ruta
   # app.iconbitmap(icon_path)



    # Pantallas (menu principal, guardar contraseñas y ver contraseñas))
    frame_principal = ctk.CTkFrame(app)
    frame_guardar = ctk.CTkFrame(app)
    frame_ver = ctk.CTkFrame(app)
    
    def mostrar_frame(frame):
        """Oculta todos los frames y muestra solo el seleccionado"""
        for f in (frame_guardar, frame_ver, frame_principal):
            f.pack_forget()

        frame.pack(fill="both", expand=True)
        app.update_idletasks()  # Actualiza el layout antes de obtener tamaño

        if frame == frame_principal:
            app.geometry("300x200")
        else:
            # Ajustar tamaño automáticamente al nuevo contenido
            frame_width = frame.winfo_reqwidth() + 20 
            frame_height = frame.winfo_reqheight() + 20 
            app.geometry(f"{frame_width}x{frame_height}")

    def crear_campo(root, texto_label, ocultar=False):
        label = ctk.CTkLabel(root, text=texto_label)
        label.pack(pady=(10, 2))
        campo = ctk.CTkEntry(root, width=300, show="*" if ocultar else "")
        campo.pack()
        return campo
    

    def crear_boton(frame, texto, comando):
        return ctk.CTkButton(
            frame,
            text=texto,
            command=comando,
            width=200,
            height=40,
            font=("Segoe UI", 16)
        )
    
    # Pantalla: Guardar Contraseña (construimos de alguna forma el frame_guardar)
    campo_siteWeb = crear_campo(frame_guardar, "Sitio web:")
    campo_user = crear_campo(frame_guardar, "Usuario:")
    campo_pass = crear_campo(frame_guardar, "Contraseña:", ocultar=False)
    
    def guardar():
        site = campo_siteWeb.get()
        user = campo_user.get()
        passwd = campo_pass.get()

        if site and user and passwd:
            save_password(site, user, passwd)
            messagebox.showinfo("Éxito", "Contraseña guardada")
            campo_siteWeb.delete(0, tk.END)
            campo_user.delete(0, tk.END)
            campo_pass.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Completa todos los campos")

    def volverMenu():
        mostrar_frame(frame_principal)




    boton_guardar = crear_boton(frame_guardar, "Guardar Contraseña", guardar)
    boton_volverMenu = crear_boton(frame_guardar, "Volver al Menú", volverMenu)

    boton_guardar.pack(pady=10)
    boton_volverMenu.pack(pady=10)

    # Pantalla: Ver Contraseñas (a completar en el futuro)
    label_ver = ctk.CTkLabel(frame_ver, text="Aquí se mostrarán las contraseñas (estamos trabajando en ello)")
    label_ver.pack(pady=20)
    boton_volverMenu = crear_boton(frame_ver, "Volver al Menú", volverMenu)
    boton_volverMenu.pack(pady=10)


    # Menú principal
    frame_principal.pack(fill="both", expand=True)





    boton_guardarPass = crear_boton(frame_principal, "Guardar Contraseña", lambda: mostrar_frame(frame_guardar))
    boton_verPass = crear_boton(frame_principal, "Ver contraseña", lambda: mostrar_frame(frame_ver))

    boton_guardarPass.pack(pady=10, padx=10)
    boton_verPass.pack(pady=10, padx=10)      


    # Mostrar pantalla por defecto (de esta forma al inicial la app se muestra la pantalla de guardar contraseñas de forma automatica)
    #mostrar_frame(frame_guardar)

    app.mainloop()
   

    