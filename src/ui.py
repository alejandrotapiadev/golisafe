"""
Interfaz de usuario para GoliSafe. Tkinter

"""
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedStyle
from database import init_db, save_password, getAllPasswords, delete_password
import os

def start_app():
    init_db()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("GoliSafe")
    app.geometry("300x200")
    #app.resizable(False, False)
    

    # Establecer icono de la aplicación
    base_dir = os.path.dirname(os.path.abspath(__file__))  # ruta carpeta src
    icon_path = os.path.join(base_dir, "..", "assets", "icon", "logo3.ico")
    icon_path = os.path.normpath(icon_path)  # para normalizar ruta
    app.iconbitmap(icon_path)


    #ESTILO TABLA
    style = ThemedStyle(app)
    style.set_theme("equilux")  # Cambia el tema a "arc" o cualquier otro disponible

    # Estilo general del Treeview (filas y fondo)
    style.configure("Treeview",
                    background="#2e2e2e",
                    foreground="white",
                    fieldbackground="#2e2e2e",
                    rowheight=30,
                    bordercolor="#444")

    # Estilo específico de la cabecera
    style.configure("Treeview.Heading",
                    background="#444444",
                    foreground="white",
                    font=('Segoe UI', 10, 'bold'))
    
    # Color al seleccionar una fila
    style.map("Treeview",
            background=[("selected", "#006b75")],     # Fondo cuando está seleccionada
            foreground=[("selected", "white")])       # Texto cuando está seleccionada



    # DEFINICION PANTALLAS (menu principal, guardar contraseñas y ver contraseñas))
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
    
    # PANTALLA: GUARDAR CONTRASEÑA
    
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

    # PANTALLA: VER CONTRASEÑAS
    """
    def cargar_contrasenas():
        text_box.delete("1.0", tk.END)
        filtro = campo_busqueda.get().lower()
        contrasenas = getAllPasswords()

        if not contrasenas:
            text_box.tag_config("center", justify="center", foreground="white")
            text_box.insert(tk.END, "Aun no hay contraseñas guardadas.")
            text_box.tag_add("center", "1.0", "end")
            return

        encontrados = 0
        for site, user, passwd in contrasenas:
            if filtro in site.lower() or filtro in user.lower():
                text_box.insert(tk.END, f"Sitio \u2192 {site}\nUsuario \u2192 {user}\nContraseña \u2192 {passwd}\n\n")
                encontrados += 1

        if encontrados == 0:
            text_box.insert(tk.END, f"No se encontraron coincidencias para: '{filtro}'")
        """

    def cargar_contrasenas():
        filtro = campo_busqueda.get().lower()
        for item in tree.get_children():
            tree.delete(item)

        contrasenas = getAllPasswords()

        encontrados = 0
        for site, user, passwd in contrasenas:
            if filtro in site.lower() or filtro in user.lower():
                tree.insert("", "end", values=(site, user, passwd))
                encontrados += 1

        if encontrados == 0:
            messagebox.showinfo("Información", f"No se encontraron contraseñas para: '{filtro}'")

    def eliminar_contrasena():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una contraseña para eliminar")
            return

        # Solo permitimos eliminar una seleccion a la vez:
        item = seleccion[0]
        site, user, passwd = tree.item(item, "values")

        # Confirmar eliminación
        confirmar = messagebox.askyesno("Confirmar", f"¿Quieres eliminar la contraseña para '{site}' (usuario: {user})?")
        if confirmar:
            delete_password(site, user)
            cargar_contrasenas()
            messagebox.showinfo("Éxito", "Contraseña eliminada")




    def ir_a_ver_contrasenas():
         cargar_contrasenas()
         mostrar_frame(frame_ver)


    # Entrada de búsqueda
    campo_busqueda = ctk.CTkEntry(frame_ver, width=300, placeholder_text="Buscar por sitio o usuario...")
    campo_busqueda.pack(pady=(10, 5))
    boton_buscar = ctk.CTkButton(frame_ver, text="Buscar", command=cargar_contrasenas)
    boton_buscar.pack(pady=(0, 5))


    # Caja de texto para mostrar resultados
    #text_box = ctk.CTkTextbox(frame_ver, width=400, height=300, font=("Segoe UI", 15))
    #text_box.pack(pady=5)

    # Tabla para mostrar contraseñas
    tree = ttk.Treeview(frame_ver, columns=("site", "user", "password"), show="headings", height=10)
    tree.heading("site", text="Sitio Web")
    tree.heading("user", text="Usuario")
    tree.heading("password", text="Contraseña")
    tree.column("site", width=120)
    tree.column("user", width=100)
    tree.column("password", width=120)
    tree.pack(pady=10)

    boton_eliminar = crear_boton(frame_ver, "Eliminar Contraseña", eliminar_contrasena)
    boton_eliminar.pack(pady=(5, 10))


    boton_volverMenu = crear_boton(frame_ver, "Volver al Menú", volverMenu)
    boton_volverMenu.pack(pady=10)


    # MENU PRINCIPAL (donde se accede a las diferentes pantallas)
    frame_principal.pack(fill="both", expand=True)

    boton_guardarPass = crear_boton(
        frame_principal,
        "Guardar Contraseña",
         lambda: mostrar_frame(frame_guardar)
    )

    boton_verPass = crear_boton(
        frame_principal,
        "Ver contraseña",
        ir_a_ver_contrasenas
    )
    boton_guardarPass.pack(pady=10, padx=10)
    boton_verPass.pack(pady=10, padx=10)



    # Mostrar pantalla por defecto (de esta forma al inicial la app se muestra la pantalla de guardar contraseñas de forma automatica)
    #mostrar_frame(frame_guardar)

    app.mainloop()
   

    