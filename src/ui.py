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
    
    def calcular_posicion_centrada(ventana, ancho, alto):
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        pos_x = (ancho_pantalla // 2) - (ancho // 2)
        pos_y = (alto_pantalla // 2) - (alto // 2)
        return pos_x, pos_y


    # Configurar el modo de apariencia y tema
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("GoliSafe")

    # Tamaño de ventana
    ancho_ventana = 300
    alto_ventana = 200


    # Calcular coordenadas para centrar
    pos_x, pos_y = calcular_posicion_centrada(app, ancho_ventana, alto_ventana)
    # Definir geometría con posición
    app.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
    

    # Establecer icono de la aplicación
    base_dir = os.path.dirname(os.path.abspath(__file__))  # ruta carpeta src
    icon_path = os.path.join(base_dir, "..", "assets", "icon", "logo3.ico")
    icon_path = os.path.normpath(icon_path)  # para normalizar ruta
    app.iconbitmap(icon_path)

    # Fuente monoespaciada para etiquetas
    fuente_mono = ctk.CTkFont(family="Courier New", size=15, weight="bold")

    #ESTILO TABLA
    style = ThemedStyle(app)
    style.set_theme("equilux")  # Cambia el tema a "arc" o cualquier otro disponible

    # Estilo general del Treeview (filas y fondo)
    style.configure("Treeview",
                    bordercolor="#7f5af0",  # Accent purple border
                    relief="solid",
                    borderwidth=2,
                    background="#2e2e2e",
                    foreground="white",
                    fieldbackground="#2e2e2e",
                    rowheight=30,
                    font=fuente_mono)

    # Estilo específico de la cabecera
    style.configure("Treeview.Heading",
                    background="#444444",
                    foreground="white",
                font=(fuente_mono.actual('family'), fuente_mono.actual('size'), 'bold'))  # Fuente para encabezados
    
    # Color al seleccionar una fila
    style.map("Treeview",
            background=[("selected", "#7f5af0")],     # Fondo cuando está seleccionada
            foreground=[("selected", "white")])       # Texto cuando está seleccionada





    def ajustar_columnas(treeview, fuente):
        for col in treeview["columns"]:
            # Obtener el texto del encabezado
            header_text = col
            max_ancho = fuente.measure(header_text)

            # Medir el ancho del contenido de cada celda de la columna
            for item in treeview.get_children():
                valor = treeview.set(item, col)
                ancho = fuente.measure(valor)
                if ancho > max_ancho:
                    max_ancho = ancho

            # Agregar algo de espacio extra (padding)
            treeview.column(col, width=max_ancho + 20)



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
            ancho = 300
            alto = 200
        else:
            # Ajustar tamaño automáticamente al nuevo contenido
            ancho = frame.winfo_reqwidth() + 20
            alto = frame.winfo_reqheight() + 20

        # Calcular posición para centrar
        pos_x, pos_y = calcular_posicion_centrada(app, ancho, alto)
        # Definir geometría con posición

        # Cambiar geometría con posición centrada respecto al monitor
        app.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")

    def crear_label(root, texto):
        label = ctk.CTkLabel(root, text=texto, font=fuente_mono, text_color="#e0e6ed")
        label.pack(pady=(10, 2))
        return label

    def crear_entry(root, texto_inicial=""):
        entry = ctk.CTkEntry(root, width=300, font=fuente_mono, text_color="#e0e6ed", placeholder_text=texto_inicial)
        entry.pack()
        return entry


    def crear_campo(root, texto_label, ocultar=False, texto_inicial=""):
        crear_label(root, texto_label)
        campo = crear_entry(root, texto_inicial)
        return campo
    

    def crear_boton(frame, texto, comando):
        return ctk.CTkButton(
            frame,
            text=texto,
            command=comando,
            width=200,
            height=40,
            corner_radius=35,
            font=fuente_mono,
            fg_color="#23272e",         # dark background for button
            hover_color="#343b48",      # slightly lighter on hover
            text_color="#f8fafc",       # almost white text
            border_color="#7f5af0",     # accent purple border
            border_width=2,
        )


    
    # PANTALLA: GUARDAR CONTRASEÑA
    
    campo_siteWeb = crear_campo(frame_guardar, "Sitio web:")
    campo_user = crear_campo(frame_guardar, "Usuario:")
    campo_pass = crear_campo(frame_guardar, "Contraseña:")
    
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

        ajustar_columnas(tree, fuente_mono)
        

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
    boton_buscar = crear_boton(frame_ver, "Buscar", cargar_contrasenas)
    boton_buscar.pack(pady=(0, 5))



    # Tabla para mostrar contraseñas
    tree = ttk.Treeview(frame_ver, columns=("site", "user", "password"), show="headings", height=10)
    tree.heading("site", text="Sitio Web")
    tree.heading("user", text="Usuario")
    tree.heading("password", text="Contraseña")
    tree.column("site", width=120, stretch=True)
    tree.column("user", width=100, stretch=True)
    tree.column("password", width=120, stretch=True)
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
    boton_guardarPass.pack(pady=(40,10), padx=10)
    boton_verPass.pack(pady=10, padx=10)
    #boton_guardarPass.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    #boton_verPass.place(relx=0.5, rely=0.2, anchor=tk.CENTER)


    # Mostrar pantalla por defecto (de esta forma al inicial la app se muestra la pantalla de guardar contraseñas de forma automatica)
    #mostrar_frame(frame_guardar)

    app.mainloop()
   

    