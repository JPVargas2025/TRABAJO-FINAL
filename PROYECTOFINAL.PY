import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os
codigo_admin = "123456789"
archivo_usuarios = "usuarios.txt"

def lista_productos():
    messagebox.showinfo("Inventario", "lista_productos aún no implementada.")

def buscar_producto():
    messagebox.showinfo("Inventario", "buscar_producto aún no implementada.")

def realizar_pedido():
    messagebox.showinfo("Órdenes", "realizar_pedido aún no implementada.")

def verificar_pedido():
    messagebox.showinfo("Ventas", "verificar_pedido aún no implementada.")

# Ventana de control admin
def abrir_user_control():
    inicio.withdraw()

    def volver_menu():
        user_control.destroy()
        inicio.deiconify()

    user_control = tk.Toplevel()
    user_control.title("Menú de usuario")
    user_control.geometry("500x600")
    user_control.config(bg="lightblue")
    tk.Label(user_control, text="Menú de usuario", font=("Arial", 24), bg="pink", fg="white").pack(pady=30)

    tk.Button(user_control, text="Lista de Productos", font=("Arial", 16), command=lista_productos).pack(pady=10)
    tk.Button(user_control, text="Buscar producto", font=("Arial", 16), command=buscar_producto).pack(pady=10)
    tk.Button(user_control, text="Realizar pedido", font=("Arial", 16), command=realizar_pedido).pack(pady=10)
    tk.Button(user_control, text="Verificar orden", font=("Arial", 16), command=verificar_pedido).pack(pady=10)
    tk.Button(user_control, text="Volver", font=("Arial", 16), command=volver_menu).pack(pady=5)


def ingresar_inventario():
    messagebox.showinfo("Inventario", "Función ingresar_inventario aún no implementada.")

def verificar_inventario():
    messagebox.showinfo("Inventario", "Función verificar_inventario aún no implementada.")

def revisar_orden():
    messagebox.showinfo("Órdenes", "Función revisar_orden aún no implementada.")

def Revisar_ventas():
    messagebox.showinfo("Ventas", "Función Revisar_ventas aún no implementada.")

def abrir_admin_control():
    inicio.withdraw()

    def volver_menu():
        admin_control.destroy()
        inicio.deiconify()

    admin_control = tk.Toplevel()
    admin_control.title("Menú de Administración")
    admin_control.geometry("500x600")
    admin_control.config(bg="lightblue")
    tk.Label(admin_control, text="Menú de Administración", font=("Arial", 24), bg="pink", fg="white").pack(pady=30)

    tk.Button(admin_control, text="Ingresar Inventario", font=("Arial", 16), command=ingresar_inventario).pack(pady=10)
    tk.Button(admin_control, text="Verificar Inventario", font=("Arial", 16), command=verificar_inventario).pack(pady=10)
    tk.Button(admin_control, text="Revisar Orden de Compra", font=("Arial", 16), command=revisar_orden).pack(pady=10)
    tk.Button(admin_control, text="Revisar Ventas", font=("Arial", 16), command=Revisar_ventas).pack(pady=10)
    tk.Button(admin_control, text="Volver", font=("Arial", 16), command=volver_menu).pack(pady=5)


def abrir_registro():
    inicio.withdraw()

    def registrar_usuario():
        usuario = dato_usuario.get()
        contraseña = dato_contraseña.get()
        correo = dato_correo.get()
        tipo_usuario = opcion_tipo.get()

        if usuario == "" or contraseña == "" or correo == "" or tipo_usuario == "":
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        if not correo.endswith("@gmail.com"):
            messagebox.showerror("Error", "El correo debe terminar en @gmail.com")
            return
        if tipo_usuario == "admin":
            codigo_ingresado = tk.simpledialog.askstring("Código Admin", "Ingrese el código de administrador:", show="*")
            if codigo_ingresado != codigo_admin:
                messagebox.showerror("Error", "Código incorrecto. No se pudo registrar como administrador.")
                return
        try:
            with open(archivo_usuarios, "a") as archivo:
                archivo.write(f"{usuario},{contraseña},{correo},{tipo_usuario}\n")
            messagebox.showinfo("Registro exitoso", "Su usuario ha sido registrado exitosamente")
            registro.destroy()
            inicio.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el usuario: {e}")

    def volver_inicio():
        registro.destroy()
        inicio.deiconify()

    registro = tk.Toplevel()
    registro.title("Registro de Usuario")
    registro.geometry("500x600")
    registro.config(bg="lightblue")

    tk.Label(registro, text="Registro de Usuario", font=("Arial", 24), bg="pink", fg="white").pack(pady=30)

    tk.Label(registro, text="Correo", font=("Arial", 18)).pack(pady=5)
    dato_correo = tk.Entry(registro, font=("Arial", 16))
    dato_correo.pack()

    tk.Label(registro, text="Contraseña", font=("Arial", 18)).pack(pady=5)
    dato_contraseña = tk.Entry(registro, font=("Arial", 16), show="*")
    dato_contraseña.pack()

    tk.Label(registro, text="Usuario", font=("Arial", 18)).pack(pady=5)
    dato_usuario = tk.Entry(registro, font=("Arial", 16))
    dato_usuario.pack()

    tk.Label(registro, text="Tipo de usuario", font=("Arial", 18)).pack(pady=5)
    opcion_tipo = tk.StringVar()
    opcion_tipo.set("Seleccionar")
    opciones = tk.OptionMenu(registro, opcion_tipo, "admin", "user")
    opciones.config(font=("Arial", 14))
    opciones.pack()

    tk.Button(registro, text="Registrar", font=("Arial", 16), command=registrar_usuario).pack(pady=10)
    tk.Button(registro, text="Volver", font=("Arial", 16), command=volver_inicio).pack(pady=5)

def ingreso():
    usuario = dato_usuario.get()
    contraseña = dato_contraseña.get()
    correo = dato_correo.get()
    tipo_usuario = opcion_tipo.get()

    if usuario == "" or contraseña == "" or correo == "" or tipo_usuario == "":
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    if not os.path.exists(archivo_usuarios):
        messagebox.showerror("Error", "No hay usuarios registrados.")
        return

    with open(archivo_usuarios, "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split(",")
            if len(datos) >= 4:
                usuario_archivo, contraseña_archivo, correo_archivo, tipo_archivo = datos
                if usuario == usuario_archivo and contraseña == contraseña_archivo and correo == correo_archivo:
                    if tipo_usuario == "admin" and tipo_archivo == "admin":
                        messagebox.showinfo("Ingreso exitoso", f"Bienvenid@ a JESUS NAZARETH STORE, {usuario}")
                        abrir_admin_control()
                        dato_usuario.delete(0, tk.END)
                        dato_contraseña.delete(0, tk.END)
                        dato_correo.delete(0, tk.END)
                        opcion_tipo.set("Seleccionar")
                        return
                    elif tipo_usuario == "user" and tipo_archivo == "user":
                        messagebox.showinfo("Ingreso exitoso", f"Bienvenid@ a JESUS NAZARETH STORE, {usuario}")
                        abrir_user_control()
                        dato_usuario.delete(0, tk.END)
                        dato_contraseña.delete(0, tk.END)
                        dato_correo.delete(0, tk.END)
                        opcion_tipo.set("Seleccionar")
                        return

    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def salir():
    if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
        inicio.destroy()

inicio = tk.Tk()
inicio.title("JESUS NAZARETH STORE")
inicio.geometry("500x600")
inicio.config(bg="lightblue")

tk.Label(inicio, text="JESUS NAZARETH STORE", font=("Arial", 24), bg="pink", fg="white").pack(pady=30)
tk.Label(inicio, text="Un lugar donde los sueños se hacen realidad", font=("Arial", 16), bg="pink", fg="black").pack(pady=10)
tk.Label(inicio, text="Correo", font=("Arial", 18)).pack(pady=5)
dato_correo = tk.Entry(inicio, font=("Arial", 16))
dato_correo.pack()

tk.Label(inicio, text="Contraseña", font=("Arial", 18)).pack(pady=5)
dato_contraseña = tk.Entry(inicio, font=("Arial", 16), show="*")
dato_contraseña.pack()

tk.Label(inicio, text="Usuario", font=("Arial", 18)).pack(pady=5)
dato_usuario = tk.Entry(inicio, font=("Arial", 16))
dato_usuario.pack()

tk.Label(inicio, text="Tipo de usuario", font=("Arial", 18)).pack(pady=5)
opcion_tipo = tk.StringVar()
opcion_tipo.set("Seleccionar")
opciones = tk.OptionMenu(inicio, opcion_tipo, "admin", "user")
opciones.config(font=("Arial", 14))
opciones.pack()

tk.Button(inicio, text="Ingresar", font=("Arial", 16), command=ingreso).pack(pady=10)
tk.Button(inicio, text="Registrarse", font=("Arial", 16), command=abrir_registro).pack(pady=10)
tk.Button(inicio, text="Salir", font=("Arial", 16), command=salir).pack(pady=10)

inicio.mainloop()
