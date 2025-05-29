import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import pandas as pd

from Backend import registrar_usuario as registrar_usuario_db
from Backend import validar_usuario_db,obtener_productos_db,buscar_producto_db,hacer_pedido_db
from Backend import obtener_usuarios,agregar_producto_db,obtener_pedidos_usuario





codigo_admin = "123456789"
archivo_usuarios = "usuarios.json"
USUARIO_ACTUAL = None

#--------------------Funciones de usuario--------------------
def lista_productos():
    productos = obtener_productos_db()
    texto = "\n".join([f" Nombre: {p[1]} Categoria: {p[2]} Precio: ${p[3]}" for p in productos])
    messagebox.showinfo("Lista de Productos", texto or "No hay productos registrados.")

def buscar_producto():
    nombre = simpledialog.askstring("Buscar", "Nombre del producto:")
    if nombre:
        resultados = buscar_producto_db(nombre)
        if resultados:
            texto = "\n".join([f"{p[0]} - {p[1]}: ${p[3]}" for p in resultados])
            messagebox.showinfo("Resultado", texto)
        else:
            messagebox.showinfo("Sin resultados", "No se encontró el producto.")


def realizar_pedido():
    producto_id = simpledialog.askinteger("Pedido", "ID del producto:")
    cantidad = simpledialog.askinteger("Cantidad", "¿Cuántos desea?")
    if producto_id and cantidad:
        try:
            hacer_pedido_db(USUARIO_ACTUAL, producto_id, cantidad)
            messagebox.showinfo("Pedido", "Pedido realizado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar el pedido.\n{e}")

def verificar_pedido():
    pedidos = obtener_pedidos_usuario(USUARIO_ACTUAL)
    if pedidos:
        texto = "\n".join([f"#{p[0]} - {p[1]} x{p[2]} el {p[3]}" for p in pedidos])
        messagebox.showinfo("Tus Pedidos", texto)
    else:
        messagebox.showinfo("Sin pedidos", "No tienes pedidos registrados.")

#--------------------Funciones de usuario--------------------



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

#--------------------Funciones de administrador--------------------
def ingresar_inventario():
    categorias = ['Ropa', 'Zapatos', 'Cremas', 'Lociones', 'Accesorios', 'Otros']
    
    ventana = tk.Toplevel()
    ventana.title("Ingresar producto al inventario")
    ventana.geometry("400x300")
    ventana.config(bg="lightblue")

    tk.Label(ventana, text="Categoría", font=("Arial", 14), bg="lightblue").pack(pady=5)
    categoria_var = tk.StringVar()
    categoria_var.set(categorias[0])
    tk.OptionMenu(ventana, categoria_var, *categorias).pack()

    tk.Label(ventana, text="Nombre del producto", font=("Arial", 14), bg="lightblue").pack(pady=5)
    nombre_entry = tk.Entry(ventana, font=("Arial", 14))
    nombre_entry.pack()

    tk.Label(ventana, text="Precio", font=("Arial", 14), bg="lightblue").pack(pady=5)
    precio_entry = tk.Entry(ventana, font=("Arial", 14))
    precio_entry.pack()

    def guardar():
        categoria = categoria_var.get()
        nombre = nombre_entry.get()
        try:
            precio = float(precio_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return

        agregar_producto_db(nombre,categoria, precio)
        messagebox.showinfo("Éxito", f"Producto '{nombre}' guardado.")
        ventana.destroy()

    tk.Button(ventana, text="Guardar producto", font=("Arial", 14), command=guardar).pack(pady=10)


def verificar_inventario():
    """Exporta el inventario completo a un archivo Excel"""
    try:
        productos = obtener_productos_db()
        
        if not productos:
            messagebox.showinfo("Sin datos", "No hay productos en el inventario.")
            return
        
        # Crear DataFrame con los datos
        df = pd.DataFrame(productos, columns=['ID', 'Nombre', 'Categoría', 'Precio'])
        
        # Abrir diálogo para guardar archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar inventario como..."
        )
        
        if archivo:
            # Guardar en Excel
            df.to_excel(archivo, index=False, sheet_name='Inventario')
            messagebox.showinfo("Éxito", f"Inventario exportado a: {archivo}")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar el inventario.\n{e}")

def revisar_orden():
    """Permite revisar órdenes de un usuario específico usando dropdown"""
    try:


        
        usuarios = obtener_usuarios()
        
        if not usuarios:
            messagebox.showinfo("Sin usuarios", "No hay usuarios registrados.")
            return
        
        # Crear ventana para seleccionar usuario
        ventana = tk.Toplevel()
        ventana.title("Revisar Órdenes de Usuario")
        ventana.geometry("400x200")
        ventana.config(bg="lightblue")
        
        tk.Label(ventana, text="Seleccionar Usuario", font=("Arial", 16), bg="lightblue").pack(pady=10)
        
        usuario_var = tk.StringVar()
        usuario_var.set("Seleccionar usuario")
        dropdown = tk.OptionMenu(ventana, usuario_var, *usuarios)
        dropdown.config(font=("Arial", 14))
        dropdown.pack(pady=10)
        
        def mostrar_ordenes():
            usuario_seleccionado = usuario_var.get()
            if usuario_seleccionado == "Seleccionar usuario":
                messagebox.showerror("Error", "Por favor selecciona un usuario.")
                return
            
            pedidos = obtener_pedidos_usuario(usuario_seleccionado)
            
            if pedidos:
                texto = f"Órdenes de {usuario_seleccionado}:\n\n"
                total_pedidos = 0
                for p in pedidos:
                    texto += f"#{p[0]} - {p[1]} x{p[2]} el {p[3]}\n"
                    total_pedidos += 1
                texto += f"\nTotal de pedidos: {total_pedidos}"
                
                # Crear ventana para mostrar resultados
                resultado = tk.Toplevel()
                resultado.title(f"Órdenes de {usuario_seleccionado}")
                resultado.geometry("500x400")
                resultado.config(bg="white")
                
                text_widget = tk.Text(resultado, font=("Arial", 12), wrap=tk.WORD)
                text_widget.pack(expand=True, fill='both', padx=10, pady=10)
                text_widget.insert('1.0', texto)
                text_widget.config(state='disabled')
                
                ventana.destroy()
            else:
                messagebox.showinfo("Sin pedidos", f"El usuario {usuario_seleccionado} no tiene pedidos registrados.")
        
        tk.Button(ventana, text="Ver Órdenes", font=("Arial", 14), command=mostrar_ordenes).pack(pady=20)
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los usuarios.\n{e}")

def Revisar_ventas():
    """Exporta estadísticas de ventas a un archivo Excel"""
    try:
        # Importar la función adicional del backend
        from Backend import obtener_estadisticas_ventas
        
        estadisticas = obtener_estadisticas_ventas()
        
        if not estadisticas:
            messagebox.showinfo("Sin datos", "No hay ventas registradas.")
            return
        
        # Crear DataFrame con las estadísticas
        df = pd.DataFrame(estadisticas, columns=[
            'Producto', 
            'Cantidad Vendida', 
            'Precio Unitario', 
            'Total Ingresos'
        ])
        
        # Agregar fila de totales
        total_cantidad = df['Cantidad Vendida'].sum()
        total_ingresos = df['Total Ingresos'].sum()
        
        # Crear fila de totales
        fila_total = pd.DataFrame({
            'Producto': ['TOTAL'],
            'Cantidad Vendida': [total_cantidad],
            'Precio Unitario': [''],
            'Total Ingresos': [total_ingresos]
        })
        
        df = pd.concat([df, fila_total], ignore_index=True)
        
        # Abrir diálogo para guardar archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar reporte de ventas como..."
        )
        
        if archivo:
            # Guardar en Excel
            df.to_excel(archivo, index=False, sheet_name='Reporte de Ventas')
            messagebox.showinfo("Éxito", f"Reporte de ventas exportado a: {archivo}")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar el reporte de ventas.\n{e}")

#--------------------Funciones de administrador--------------------


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

def registrar_usuario(usuario=None, contraseña=None, correo=None, tipo_usuario="user"):
    """
    Registra un nuevo usuario en la base de datos.
    Si el usuario ya existe, muestra un mensaje de error.
    Retorna:
    bool: True si el registro fue exitoso,False si el usuario ya existe.
    
    """
    if not registrar_usuario_db(usuario, contraseña, correo, tipo_usuario):
        messagebox.showerror("Error", "El nombre de usuario ya existe. Por favor elija otro.")
        return False
    return True


def iniciar_sesion(usuario=None, contraseña=None, correo=None, tipo_usuario=None):
    """
    Valida las credenciales del usuario en la base de datos.
    Retorna el nombre de usuario y el rol si las credenciales son correctas,
    o None si son incorrectas.
    """
    user_data = validar_usuario_db(usuario, contraseña, correo, tipo_usuario)
    if user_data:
        global USUARIO_ACTUAL
        USUARIO_ACTUAL = user_data[0]
        return user_data[0], user_data[3]  
    return None, None


def abrir_registro():
    inicio.withdraw()

    def registrar_usuario_gui():
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
            codigo_ingresado = simpledialog.askstring("Código Admin", "Ingrese el código de administrador:", show="*")
            if codigo_ingresado != codigo_admin:
                messagebox.showerror("Error", "Código incorrecto. No se pudo registrar como administrador.")
                return

        if registrar_usuario(usuario, contraseña, correo, tipo_usuario):
            messagebox.showinfo("Registro exitoso", "Su usuario ha sido registrado exitosamente")
            registro.destroy()
            inicio.deiconify()

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

    tk.Button(registro, text="Registrar", font=("Arial", 16), command=registrar_usuario_gui).pack(pady=10)
    tk.Button(registro, text="Volver", font=("Arial", 16), command=volver_inicio).pack(pady=5)


def ingreso():
    usuario = dato_usuario.get()
    contraseña = dato_contraseña.get()
    correo = dato_correo.get()
    tipo_usuario = opcion_tipo.get()

    if usuario == "" or contraseña == "" or correo == "" or tipo_usuario == "":
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    usuario_validado, rol = iniciar_sesion(usuario, contraseña, correo, tipo_usuario)
    
    if usuario_validado:
        if rol == "admin":
            messagebox.showinfo("Ingreso exitoso", f"Bienvenid@ a JESUS NAZARETH STORE, {usuario}")
            abrir_admin_control()
           
            dato_usuario.delete(0, tk.END)
            dato_contraseña.delete(0, tk.END)
            dato_correo.delete(0, tk.END)
            opcion_tipo.set("Seleccionar")
        elif rol == "user":
            messagebox.showinfo("Ingreso exitoso", f"Bienvenid@ a JESUS NAZARETH STORE, {usuario}")
            abrir_user_control()
            
            dato_usuario.delete(0, tk.END)
            dato_contraseña.delete(0, tk.END)
            dato_correo.delete(0, tk.END)
            opcion_tipo.set("Seleccionar")
    else:
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
