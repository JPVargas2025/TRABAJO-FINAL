import tkinter as tk
from tkinter import messagebox    
from tkinter import simpledialog  
from tkinter import filedialog    
import pandas as pd               


from Backend import registrar_usuario as registrar_usuario_db
from Backend import validar_usuario_db,obtener_productos_db,buscar_producto_db,hacer_pedido_db
from Backend import obtener_usuarios,agregar_producto_db,obtener_pedidos_usuario

# Variables globales de configuración
codigo_admin = "123456789"    # Código secreto para registrarse como administrador
USUARIO_ACTUAL = None         # Variable para guardar el usuario que está usando el sistema

#--------------------Funciones de usuario--------------------
def lista_productos():
    """
    Muestra todos los productos disponibles en una ventana emergente.
    Obtiene los productos de la base de datos y los formatea para mostrar.
    """
    # Obtenemos todos los productos de la base de datos
    productos = obtener_productos_db()
    # Creamos un texto formateado con la información de cada producto
    # p[1]=nombre, p[2]=categoria, p[3]=precio
    texto = "\n".join([f" Nombre: {p[1]} Categoria: {p[2]} Precio: ${p[3]}" for p in productos])
    # Mostramos la información en una ventana emergente
    messagebox.showinfo("Lista de Productos", texto or "No hay productos registrados.")

def buscar_producto():
    """
    Permite al usuario buscar un producto por nombre.
    Muestra los resultados en una ventana emergente.
    """
    # Pedimos al usuario que ingrese el nombre del producto
    nombre = simpledialog.askstring("Buscar", "Nombre del producto:")
    if nombre:  # Si el usuario ingresó algo
        # Buscamos productos que contengan ese nombre
        resultados = buscar_producto_db(nombre)
        if resultados:  # Si encontramos productos
            # Formateamos los resultados: ID - Nombre: Precio
            texto = "\n".join([f"{p[0]} - {p[1]}: ${p[3]}" for p in resultados])
            messagebox.showinfo("Resultado", texto)
        else:  # Si no encontramos nada
            messagebox.showinfo("Sin resultados", "No se encontró el producto.")

def realizar_pedido():
    """
    Permite al usuario realizar un pedido.
    Pide el ID del producto y la cantidad deseada.
    """
    # Pedimos el ID del producto que quiere pedir
    producto_id = simpledialog.askinteger("Pedido", "ID del producto:")
    # Pedimos la cantidad que quiere
    cantidad = simpledialog.askinteger("Cantidad", "¿Cuántos desea?")
    
    if producto_id and cantidad:  # Si ingresó ambos datos
        try:
            # Intentamos hacer el pedido en la base de datos
            hacer_pedido_db(USUARIO_ACTUAL, producto_id, cantidad)
            messagebox.showinfo("Pedido", "Pedido realizado con éxito.")
        except Exception as e:
            # Si hay algún error (producto no existe, etc.)
            messagebox.showerror("Error", f"No se pudo realizar el pedido.\n{e}")

def verificar_pedido():
    """
    Muestra todos los pedidos que ha hecho el usuario actual.
    """
    # Obtenemos los pedidos del usuario actual
    pedidos = obtener_pedidos_usuario(USUARIO_ACTUAL)
    if pedidos:  # Si tiene pedidos
        # Formateamos la información: #ID - Producto xCantidad el Fecha
        texto = "\n".join([f"#{p[0]} - {p[1]} x{p[2]} el {p[3]}" for p in pedidos])
        messagebox.showinfo("Tus Pedidos", texto)
    else:  # Si no tiene pedidos
        messagebox.showinfo("Sin pedidos", "No tienes pedidos registrados.")

#--------------------Funciones de usuario--------------------

def abrir_user_control():
    """
    Abre la ventana del menú de usuario.
    Oculta la ventana principal y muestra las opciones disponibles para usuarios normales.
    """
    # Ocultamos la ventana principal
    inicio.withdraw()

    def volver_menu():
        """Función interna para volver al menú principal"""
        user_control.destroy()  # Cerramos la ventana de usuario
        inicio.deiconify()      # Mostramos la ventana principal

    # Creamos una nueva ventana para el menú de usuario
    user_control = tk.Toplevel()
    user_control.title("Menú de usuario")
    user_control.geometry("500x600")
    user_control.config(bg="lightblue")
    
    # Título de la ventana
    tk.Label(user_control, text="Menú de usuario", font=("Arial", 24), bg="pink", fg="white").pack(pady=30)

    # Botones con las opciones disponibles para el usuario
    tk.Button(user_control, text="Lista de Productos", font=("Arial", 16), command=lista_productos).pack(pady=10)
    tk.Button(user_control, text="Buscar producto", font=("Arial", 16), command=buscar_producto).pack(pady=10)
    tk.Button(user_control, text="Realizar pedido", font=("Arial", 16), command=realizar_pedido).pack(pady=10)
    tk.Button(user_control, text="Verificar orden", font=("Arial", 16), command=verificar_pedido).pack(pady=10)
    tk.Button(user_control, text="Volver", font=("Arial", 16), command=volver_menu).pack(pady=5)

#--------------------Funciones de administrador--------------------
def ingresar_inventario():
    """
    Permite al administrador agregar nuevos productos al inventario.
    Abre una ventana con formulario para ingresar categoría, nombre y precio.
    """
    # Lista de categorías predefinidas
    categorias = ['Ropa', 'Zapatos', 'Cremas', 'Lociones', 'Accesorios', 'Otros']
    
    # Creamos una nueva ventana para el formulario
    ventana = tk.Toplevel()
    ventana.title("Ingresar producto al inventario")
    ventana.geometry("400x300")
    ventana.config(bg="lightblue")

    # Campo para seleccionar categoría
    tk.Label(ventana, text="Categoría", font=("Arial", 14), bg="lightblue").pack(pady=5)
    categoria_var = tk.StringVar()
    categoria_var.set(categorias[0])  # Ponemos la primera categoría por defecto
    tk.OptionMenu(ventana, categoria_var, *categorias).pack()

    # Campo para ingresar nombre del producto
    tk.Label(ventana, text="Nombre del producto", font=("Arial", 14), bg="lightblue").pack(pady=5)
    nombre_entry = tk.Entry(ventana, font=("Arial", 14))
    nombre_entry.pack()

    # Campo para ingresar precio
    tk.Label(ventana, text="Precio", font=("Arial", 14), bg="lightblue").pack(pady=5)
    precio_entry = tk.Entry(ventana, font=("Arial", 14))
    precio_entry.pack()

    def guardar():
        """
        Función interna que se ejecuta cuando se presiona 'Guardar producto'.
        Valida los datos y los guarda en la base de datos.
        """
        categoria = categoria_var.get()
        nombre = nombre_entry.get()
        
        try:
            # Intentamos convertir el precio a número decimal
            precio = float(precio_entry.get())
        except ValueError:
            # Si no se puede convertir, mostramos error
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        # Validamos que el nombre no esté vacío
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return

        # Si todo está bien, guardamos el producto
        agregar_producto_db(nombre, categoria, precio)
        messagebox.showinfo("Éxito", f"Producto '{nombre}' guardado.")
        ventana.destroy()  # Cerramos la ventana

    # Botón para guardar el producto
    tk.Button(ventana, text="Guardar producto", font=("Arial", 14), command=guardar).pack(pady=10)

def verificar_inventario():
    """
    Exporta el inventario completo a un archivo Excel.
    Permite al administrador descargar todos los productos en formato Excel.
    """
    try:
        # Obtenemos todos los productos
        productos = obtener_productos_db()
        
        if not productos:
            messagebox.showinfo("Sin datos", "No hay productos en el inventario.")
            return
        
        # Creamos un DataFrame de pandas con los datos
        # DataFrame es como una tabla de Excel en Python
        df = pd.DataFrame(productos, columns=['ID', 'Nombre', 'Categoría', 'Precio'])
        
        # Abrimos un diálogo para que el usuario elija dónde guardar el archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",  # Extensión por defecto
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],  # Tipos de archivo permitidos
            title="Guardar inventario como..."
        )
        
        if archivo:  # Si el usuario eligió una ubicación
            # Guardamos los datos en Excel
            df.to_excel(archivo, index=False, sheet_name='Inventario')
            messagebox.showinfo("Éxito", f"Inventario exportado a: {archivo}")
        
    except Exception as e:
        # Si hay algún error en el proceso
        messagebox.showerror("Error", f"No se pudo exportar el inventario.\n{e}")

def revisar_orden():
    """
    Permite al administrador revisar las órdenes de un usuario específico.
    Muestra un dropdown con todos los usuarios y luego sus pedidos.
    """
    try:
        # Obtenemos la lista de todos los usuarios registrados
        usuarios = obtener_usuarios()
        
        if not usuarios:
            messagebox.showinfo("Sin usuarios", "No hay usuarios registrados.")
            return
        
        # Creamos ventana para seleccionar usuario
        ventana = tk.Toplevel()
        ventana.title("Revisar Órdenes de Usuario")
        ventana.geometry("400x200")
        ventana.config(bg="lightblue")
        
        tk.Label(ventana, text="Seleccionar Usuario", font=("Arial", 16), bg="lightblue").pack(pady=10)
        
        # Dropdown (menú desplegable) con los usuarios
        usuario_var = tk.StringVar()
        usuario_var.set("Seleccionar usuario")  # Texto por defecto
        dropdown = tk.OptionMenu(ventana, usuario_var, *usuarios)
        dropdown.config(font=("Arial", 14))
        dropdown.pack(pady=10)
        
        def mostrar_ordenes():
            """
            Función interna que muestra las órdenes del usuario seleccionado.
            """
            usuario_seleccionado = usuario_var.get()
            
            # Validamos que se haya seleccionado un usuario
            if usuario_seleccionado == "Seleccionar usuario":
                messagebox.showerror("Error", "Por favor selecciona un usuario.")
                return
            
            # Obtenemos los pedidos del usuario seleccionado
            pedidos = obtener_pedidos_usuario(usuario_seleccionado)
            
            if pedidos:  # Si el usuario tiene pedidos
                # Creamos el texto con la información de los pedidos
                texto = f"Órdenes de {usuario_seleccionado}:\n\n"
                total_pedidos = 0
                for p in pedidos:
                    texto += f"#{p[0]} - {p[1]} x{p[2]} el {p[3]}\n"
                    total_pedidos += 1
                texto += f"\nTotal de pedidos: {total_pedidos}"
                
                # Creamos una nueva ventana para mostrar los resultados
                resultado = tk.Toplevel()
                resultado.title(f"Órdenes de {usuario_seleccionado}")
                resultado.geometry("500x400")
                resultado.config(bg="white")
                
                # Usamos un widget de texto para mostrar la información
                text_widget = tk.Text(resultado, font=("Arial", 12), wrap=tk.WORD)
                text_widget.pack(expand=True, fill='both', padx=10, pady=10)
                text_widget.insert('1.0', texto)
                text_widget.config(state='disabled')  # Solo lectura
                
                ventana.destroy()  # Cerramos la ventana de selección
            else:  # Si no tiene pedidos
                messagebox.showinfo("Sin pedidos", f"El usuario {usuario_seleccionado} no tiene pedidos registrados.")
        
        # Botón para ver las órdenes
        tk.Button(ventana, text="Ver Órdenes", font=("Arial", 14), command=mostrar_ordenes).pack(pady=20)
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los usuarios.\n{e}")

def Revisar_ventas():
    """
    Exporta estadísticas de ventas a un archivo Excel.
    Muestra cuánto se ha vendido de cada producto y cuánto dinero ha generado.
    """
    try:
        # Importamos la función adicional del backend
        from Backend import obtener_estadisticas_ventas
        
        # Obtenemos las estadísticas de ventas
        estadisticas = obtener_estadisticas_ventas()
        
        if not estadisticas:
            messagebox.showinfo("Sin datos", "No hay ventas registradas.")
            return
        
        # Creamos DataFrame con las estadísticas
        df = pd.DataFrame(estadisticas, columns=[
            'Producto', 
            'Cantidad Vendida', 
            'Precio Unitario', 
            'Total Ingresos'
        ])
        
        # Calculamos totales generales
        total_cantidad = df['Cantidad Vendida'].sum()
        total_ingresos = df['Total Ingresos'].sum()
        
        # Creamos una fila con los totales
        fila_total = pd.DataFrame({
            'Producto': ['TOTAL'],
            'Cantidad Vendida': [total_cantidad],
            'Precio Unitario': [''],
            'Total Ingresos': [total_ingresos]
        })
        
        # Agregamos la fila de totales al DataFrame
        df = pd.concat([df, fila_total], ignore_index=True)
        
        # Abrimos diálogo para guardar archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar reporte de ventas como..."
        )
        
        if archivo:  # Si el usuario eligió ubicación
            # Guardamos en Excel
            df.to_excel(archivo, index=False, sheet_name='Reporte de Ventas')
            messagebox.showinfo("Éxito", f"Reporte de ventas exportado a: {archivo}")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar el reporte de ventas.\n{e}")

#--------------------Funciones de administrador--------------------

def abrir_admin_control():
    """
    Abre la ventana del menú de administrador.
    Similar al menú de usuario pero con opciones administrativas.
    """
    # Ocultamos la ventana principal
    inicio.withdraw()

    def volver_menu():
        """Función interna para volver al menú principal"""
        admin_control.destroy()  # Cerramos ventana de admin
        inicio.deiconify()       # Mostramos ventana principal

    # Creamos nueva ventana para menú de administrador
    admin_control = tk.Toplevel()
    admin_control.title("Menú de Administración")
    admin_control.geometry("500x600")
    admin_control.config(bg="lightblue")
    
    # Título
    tk.Label(admin_control, text="Menú de Administración", font=("Arial", 24), bg="pink", fg="white").pack(pady=30)

    # Botones con opciones administrativas
    tk.Button(admin_control, text="Ingresar Inventario", font=("Arial", 16), command=ingresar_inventario).pack(pady=10)
    tk.Button(admin_control, text="Verificar Inventario", font=("Arial", 16), command=verificar_inventario).pack(pady=10)
    tk.Button(admin_control, text="Revisar Orden de Compra", font=("Arial", 16), command=revisar_orden).pack(pady=10)
    tk.Button(admin_control, text="Revisar Ventas", font=("Arial", 16), command=Revisar_ventas).pack(pady=10)
    tk.Button(admin_control, text="Volver", font=("Arial", 16), command=volver_menu).pack(pady=5)

def registrar_usuario(usuario=None, contraseña=None, correo=None, tipo_usuario="user"):
    """
    Registra un nuevo usuario en la base de datos.
    Es un "wrapper" (envoltorio) de la función del backend que agrega mensajes de interfaz.
    
    Parámetros:
    - usuario: nombre de usuario
    - contraseña: contraseña del usuario
    - correo: email del usuario
    - tipo_usuario: "user" o "admin"
    
    Retorna:
    bool: True si el registro fue exitoso, False si el usuario ya existe.
    """
    # Llamamos a la función del backend para registrar
    if not registrar_usuario_db(usuario, contraseña, correo, tipo_usuario):
        # Si la función retorna False, significa que el usuario ya existe
        messagebox.showerror("Error", "El nombre de usuario ya existe. Por favor elija otro.")
        return False
    return True

def iniciar_sesion(usuario=None, contraseña=None, correo=None, tipo_usuario=None):
    """
    Valida las credenciales del usuario en la base de datos.
    Si las credenciales son correctas, guarda el usuario actual en la variable global.
    
    Retorna:
    tuple: (nombre_usuario, rol) si las credenciales son correctas
    (None, None) si son incorrectas
    """
    # Validamos las credenciales usando el backend
    user_data = validar_usuario_db(usuario, contraseña, correo, tipo_usuario)
    
    if user_data:  # Si encontró el usuario
        global USUARIO_ACTUAL
        USUARIO_ACTUAL = user_data[0]  # Guardamos el nombre de usuario
        return user_data[0], user_data[3]  # Retornamos usuario y rol
    return None, None  # Si no encontró el usuario

def abrir_registro():
    """
    Abre la ventana de registro de nuevos usuarios.
    Permite registrar usuarios normales y administradores.
    """
    # Ocultamos la ventana principal
    inicio.withdraw()

    def registrar_usuario_gui():
        """
        Función interna que maneja el registro desde la interfaz gráfica.
        Valida los datos ingresados y llama a la función de registro.
        """
        # Obtenemos los datos ingresados por el usuario
        usuario = dato_usuario.get()
        contraseña = dato_contraseña.get()
        correo = dato_correo.get()
        tipo_usuario = opcion_tipo.get()

        # Validamos que todos los campos estén llenos
        if usuario == "" or contraseña == "" or correo == "" or tipo_usuario == "":
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        # Validamos que el correo termine en @gmail.com
        if not correo.endswith("@gmail.com"):
            messagebox.showerror("Error", "El correo debe terminar en @gmail.com")
            return
        
        # Si quiere registrarse como admin, pedimos el código secreto
        if tipo_usuario == "admin":
            codigo_ingresado = simpledialog.askstring("Código Admin", "Ingrese el código de administrador:", show="*")
            if codigo_ingresado != codigo_admin:
                messagebox.showerror("Error", "Código incorrecto. No se pudo registrar como administrador.")
                return

        # Si todo está bien, intentamos registrar al usuario
        if registrar_usuario(usuario, contraseña, correo, tipo_usuario):
            messagebox.showinfo("Registro exitoso", "Su usuario ha sido registrado exitosamente")
            registro.destroy()  # Cerramos ventana de registro
            inicio.deiconify()  # Mostramos ventana principal

    def volver_inicio():
        """Función para volver a la ventana principal"""
        registro.destroy()  # Cerramos ventana de registro
        inicio.deiconify()  # Mostramos ventana principal

    # Creamos la ventana de registro
    registro = tk.Toplevel()
    registro.title("Registro de Usuario")
    registro.geometry("500x600")
    registro.config(bg="lightblue")

    # Título de la ventana
    tk.Label(registro, text="Registro de Usuario", font=("Arial", 24), bg="pink", fg="white").pack(pady=30)

    # Campo para ingresar correo
    tk.Label(registro, text="Correo", font=("Arial", 18)).pack(pady=5)
    dato_correo = tk.Entry(registro, font=("Arial", 16))
    dato_correo.pack()

    # Campo para ingresar contraseña (se oculta con asteriscos)
    tk.Label(registro, text="Contraseña", font=("Arial", 18)).pack(pady=5)
    dato_contraseña = tk.Entry(registro, font=("Arial", 16), show="*")
    dato_contraseña.pack()

    # Campo para ingresar nombre de usuario
    tk.Label(registro, text="Usuario", font=("Arial", 18)).pack(pady=5)
    dato_usuario = tk.Entry(registro, font=("Arial", 16))
    dato_usuario.pack()

    # Dropdown para seleccionar tipo de usuario
    tk.Label(registro, text="Tipo de usuario", font=("Arial", 18)).pack(pady=5)
    opcion_tipo = tk.StringVar()
    opcion_tipo.set("Seleccionar")  # Valor por defecto
    opciones = tk.OptionMenu(registro, opcion_tipo, "admin", "user")
    opciones.config(font=("Arial", 14))
    opciones.pack()

    # Botones de acción
    tk.Button(registro, text="Registrar", font=("Arial", 16), command=registrar_usuario_gui).pack(pady=10)
    tk.Button(registro, text="Volver", font=("Arial", 16), command=volver_inicio).pack(pady=5)

def ingreso():
    """
    Maneja el proceso de inicio de sesión.
    Valida las credenciales y redirige al menú correspondiente según el tipo de usuario.
    """
    # Obtenemos los datos ingresados en el formulario principal
    usuario = dato_usuario.get()
    contraseña = dato_contraseña.get()
    correo = dato_correo.get()
    tipo_usuario = opcion_tipo.get()

    # Validamos que todos los campos estén llenos
    if usuario == "" or contraseña == "" or correo == "" or tipo_usuario == "":
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    # Intentamos validar las credenciales
    usuario_validado, rol = iniciar_sesion(usuario, contraseña, correo, tipo_usuario)
    
    if usuario_validado:  # Si las credenciales son correctas
        if rol == "admin":  # Si es administrador
            messagebox.showinfo("Ingreso exitoso", f"Bienvenid@ a JESUS NAZARETH STORE, {usuario}")
            abrir_admin_control()  # Abrimos menú de administrador
           
            # Limpiamos los campos del formulario
            dato_usuario.delete(0, tk.END)
            dato_contraseña.delete(0, tk.END)
            dato_correo.delete(0, tk.END)
            opcion_tipo.set("Seleccionar")
            
        elif rol == "user":  # Si es usuario normal
            messagebox.showinfo("Ingreso exitoso", f"Bienvenid@ a JESUS NAZARETH STORE, {usuario}")
            abrir_user_control()  # Abrimos menú de usuario
            
            # Limpiamos los campos del formulario
            dato_usuario.delete(0, tk.END)
            dato_contraseña.delete(0, tk.END)
            dato_correo.delete(0, tk.END)
            opcion_tipo.set("Seleccionar")
    else:  # Si las credenciales son incorrectas
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def salir():
    """
    Maneja la salida del sistema.
    Pregunta al usuario si realmente quiere salir antes de cerrar la aplicación.
    """
    # Mostramos un cuadro de confirmación
    if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
        inicio.destroy()  # Cerramos la aplicación completamente

# ==================== VENTANA PRINCIPAL ====================
# Creamos la ventana principal de la aplicación
inicio = tk.Tk()
inicio.title("JESUS NAZARETH STORE")
inicio.geometry("500x600")
inicio.config(bg="lightblue")

# Títulos y descripción de la tienda
tk.Label(inicio, text="JESUS NAZARETH STORE", font=("Arial", 24), bg="pink", fg="white").pack(pady=30)
tk.Label(inicio, text="Un lugar donde los sueños se hacen realidad", font=("Arial", 16), bg="pink", fg="black").pack(pady=10)

# Formulario de inicio de sesión en la ventana principal
# Campo para correo electrónico
tk.Label(inicio, text="Correo", font=("Arial", 18)).pack(pady=5)
dato_correo = tk.Entry(inicio, font=("Arial", 16))
dato_correo.pack()

# Campo para contraseña (se muestra con asteriscos por seguridad)
tk.Label(inicio, text="Contraseña", font=("Arial", 18)).pack(pady=5)
dato_contraseña = tk.Entry(inicio, font=("Arial", 16), show="*")
dato_contraseña.pack()

# Campo para nombre de usuario
tk.Label(inicio, text="Usuario", font=("Arial", 18)).pack(pady=5)
dato_usuario = tk.Entry(inicio, font=("Arial", 16))
dato_usuario.pack()

# Dropdown para seleccionar tipo de usuario (admin o user)
tk.Label(inicio, text="Tipo de usuario", font=("Arial", 18)).pack(pady=5)
opcion_tipo = tk.StringVar()
opcion_tipo.set("Seleccionar")  # Valor por defecto
opciones = tk.OptionMenu(inicio, opcion_tipo, "admin", "user")
opciones.config(font=("Arial", 14))
opciones.pack()

# Botones principales de la aplicación
tk.Button(inicio, text="Ingresar", font=("Arial", 16), command=ingreso).pack(pady=10)        # Botón para iniciar sesión
tk.Button(inicio, text="Registrarse", font=("Arial", 16), command=abrir_registro).pack(pady=10)  # Botón para abrir registro
tk.Button(inicio, text="Salir", font=("Arial", 16), command=salir).pack(pady=10)           # Botón para salir del sistema

# Iniciamos el bucle principal de la interfaz gráfica
# Esta línea mantiene la ventana abierta y esperando interacciones del usuario
inicio.mainloop()