"""
Interfaz de usuario para GoliSafe. Tkinter

"""
import tkinter as tk
from tkinter import messagebox
from database import init_db, save_password

def start_app():

    def guardar():
        """
        Guarda la contraseña en la base de datos.
        
        """

        #recuperar los valores de los campos de entrada
        site = entry_site.get()
        user = entry_user.get()
        passwd = entry_pass.get()
        
        if site and user and passwd:
            save_password(site, user, passwd)
            messagebox.showinfo("Éxito", "Contraseña guardada")
            entry_site.delete(0, tk.END)
            entry_user.delete(0, tk.END)
            entry_pass.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Completa todos los campos")


    def crear_campo(root, texto_label, ocultar=False):
        """
        Crea campos de Tkinter para la interfaz de usuario.
        
        """
        tk.Label(root, text=texto_label).pack()
        entry = tk.Entry(root, show="*" if ocultar else "")
        entry.pack()
        return entry
    
     #iniciar la base de datos
    init_db()


    root = tk.Tk()
    root.title("GoliSafe - Gestor de Contraseñas")
    root.geometry("400x300")

    # Crear etiquetas y campos de entrada
    
    entry_site = crear_campo(root, "Sitio web:")
    entry_site.pack()
    
    entry_user = crear_campo(root, "Usuario:")
    entry_user.pack()
    
    entry_pass = crear_campo(root, "Contraseña:")
    entry_pass.pack()

    # crear botón para guardar la contraseña
    boton_guardar = tk.Button(root, text="Guardar contraseña", command=guardar)
    boton_guardar.pack(pady=10)
    root.mainloop()

    