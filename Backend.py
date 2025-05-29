import sqlite3  

# Nombre del archivo de nuestra base de datos
DB_NAME = "usuarios.db"

def inicializar_db():
    """
    Crea la base de datos y la tabla de usuarios si no existen.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # tabla usuarios 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                username TEXT PRIMARY KEY,    -- Nombre de usuario (unico, no se puede repetir)
                password TEXT NOT NULL,       -- Contrasena (obligatoria)
                email TEXT NOT NULL,          -- Correo electronico (obligatorio)
                role TEXT NOT NULL            -- Tipo de usuario: "user", "admin", etc. (obligatorio)
            )
        ''')
        # tabla productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,   -- ID unico para cada producto (se incrementa automaticamente)
                categoria TEXT,                        -- Categoria del producto (opcional)
                nombre TEXT NOT NULL,                  -- Nombre del producto (obligatorio)
                precio REAL NOT NULL                   -- Precio del producto (obligatorio)
            )
        ''')

        # Tabla de pedidos de usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,    -- ID unico del pedido (se incrementa automaticamente)
            usuario TEXT NOT NULL,                   -- Nombre del usuario que hizo el pedido
            producto_id INTEGER NOT NULL,            -- ID del producto pedido (referencia a tabla productos)
            cantidad INTEGER NOT NULL,               -- Cantidad de productos pedidos
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,    -- Fecha y hora del pedido (se pone automaticamente)
            FOREIGN KEY (producto_id) REFERENCES productos(id)  -- Relacion con tabla productos)
        )
    """)
        
        # Guardamos todos los cambios en la base de datos
        conn.commit()

def registrar_usuario(usuario, contrasena, correo,tipo_usuario="user"):
    """
    Esta funcion registra un nuevo usuario en la base de datos.
    Por defecto, el tipo_usuario sera "user".

    Retorna:
    bool: True si el registro fue exitoso,False si el usuario ya existe.
    """
    # Primero nos aseguramos de que la base de datos y tabla existan
    inicializar_db()
    
    # Abrimos conexion a la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        try:
            # INSERT INTO = insertar datos en la tabla
            # Los signos ? son "placeholders" para los valores que vamos a insertar
            # SQLite los reemplaza con los valores que pasamos en la tupla
            # Evita ataques de "SQL injection"
            cursor.execute("INSERT INTO usuarios (username, password, email, role) VALUES (?, ?, ?, ?)",
                           (usuario, contrasena, correo, tipo_usuario))
            
            # Guardamos los cambios
            conn.commit()
            
            # Si todo salio bien, devolvemos True
            return True
            
        except sqlite3.IntegrityError:
            # Esta excepcion ocurre cuando intentamos insertar un username que ya existe
            # (porque username es PRIMARY KEY, debe ser unico)
            return False

def validar_usuario_db(usuario, contrasena, correo, tipo_usuario):
    """
    verifica si un usuario existe con todos los datos proporcionados.  
    Retorna:
    tuple: Una tupla con los datos del usuario si existe
    None: Si no se encuentra ningun usuario con todos los datos especificados
    """
    # Nos aseguramos de que la base de datos existe
    inicializar_db()
    
    # Abrimos conexion
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # SELECT = seleccionar/buscar datos
        # * significa "todos los campos" (username, password, email, role)
        # FROM = de que tabla queremos buscar
        # WHERE = condiciones para filtrar
        cursor.execute('''
            SELECT * FROM usuarios
            WHERE username = ? AND password = ? AND email = ? AND role = ?
        ''', (usuario, contrasena, correo, tipo_usuario))
        
        # fetchone() devuelve el primer resultado encontrado
        # Si no encuentra nada, devuelve None
        # Si encuentra algo, devuelve una tupla con todos los datos del usuario
        return cursor.fetchone()
    

def agregar_producto_db(nombre, categoria, precio):
    """
    Agrega un nuevo producto a la base de datos.
    Parametros:
    - nombre: Nombre del producto
    - categoria: Categoria del producto
    - precio: Precio del producto
    """
    # Conectamos a la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        conn = conn  # Esta linea es redundante, pero se mantiene
        cur = conn.cursor()
        # Insertamos el nuevo producto en la tabla productos
        cur.execute("INSERT INTO productos (nombre, categoria, precio) VALUES (?, ?, ?)", (nombre, categoria, precio))
        # Guardamos los cambios
        conn.commit()

def obtener_productos_db():
    """
    Obtiene todos los productos de la base de datos.
    Retorna:
    list: Lista de tuplas con (id, nombre, categoria, precio) de todos los productos
    """
    # Conectamos a la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # Seleccionamos todos los productos con sus datos principales
        cur.execute("SELECT id, nombre, categoria, precio FROM productos")
        # fetchall() devuelve todos los resultados encontrados
        productos = cur.fetchall()
        return productos

def buscar_producto_db(nombre):
    """
    Busca productos por nombre (busqueda parcial).
    Parametros:
    - nombre: Parte del nombre del producto a buscar
    Retorna:
    list: Lista de productos que coinciden con la busqueda
    """
    # Conectamos a la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # LIKE permite busqueda parcial, % significa "cualquier texto antes o despues"
        cur.execute("SELECT id, nombre, categoria, precio FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
        resultado = cur.fetchall()
        return resultado

def hacer_pedido_db(usuario, producto_id, cantidad):
    """
    Permite a un usuario realizar un pedido y lo registra en la base de datos.
    Parametros:
    - usuario: Nombre del usuario que hace el pedido
    - producto_id: ID del producto que se quiere pedir
    - cantidad: Cantidad de productos que se quieren pedir
    """
    # Conectamos a la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # Insertamos el pedido en la tabla pedidos
        # La fecha se pone automaticamente gracias a CURRENT_TIMESTAMP
        cur.execute("INSERT INTO pedidos (usuario, producto_id, cantidad) VALUES (?, ?, ?)", (usuario, producto_id, cantidad))
        # Guardamos los cambios
        conn.commit()

def obtener_pedidos_usuario(usuario):
    """
    Obtiene todos los pedidos de un usuario especifico.
    Parametros:
    - usuario: Nombre del usuario del que queremos ver los pedidos
    Retorna:
    list: Lista de pedidos con informacion del producto
    """
    # Conectamos a la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # JOIN une las tablas pedidos y productos para obtener informacion completa
        # p = alias para tabla pedidos, pr = alias para tabla productos
        cur.execute("""
            SELECT p.id, pr.nombre, p.cantidad, p.fecha 
            FROM pedidos p
            JOIN productos pr ON p.producto_id = pr.id
            WHERE p.usuario = ?
            ORDER BY p.fecha DESC
        """, (usuario,))
        pedidos = cur.fetchall()
        return pedidos
   
def obtener_usuarios():
    """
    Obtiene todos los usernames de usuarios registrados.
    Esta funcion se usa para mostrar la lista de usuarios en el dropdown del admin.
    Retorna:
    list: Lista con todos los nombres de usuario registrados
    """
    # Conectamos a la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # Seleccionamos solo los nombres de usuario
        cur.execute("SELECT username FROM usuarios")
        usuarios = cur.fetchall()
        # Convertimos las tuplas en una lista simple de strings
        # usuarios viene como [('usuario1',), ('usuario2',)] y lo convertimos a ['usuario1', 'usuario2']
        return [usuario[0] for usuario in usuarios]

def obtener_estadisticas_ventas():
    """
    Obtiene estadisticas de ventas por producto.
    Calcula cuanto se ha vendido de cada producto y cuanto dinero ha generado.
    Retorna:
    list: Lista con estadisticas de ventas (nombre, cantidad vendida, precio, ingresos totales)
    """
    # Conectamos a la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        # Query complejo que calcula estadisticas de ventas
        cur.execute("""
            SELECT 
                pr.nombre as producto,                          -- Nombre del producto
                SUM(p.cantidad) as total_vendido,               -- Suma total de cantidad vendida
                pr.precio as precio_unitario,                   -- Precio por unidad
                SUM(p.cantidad * pr.precio) as total_ingresos   -- Ingresos totales (cantidad * precio)
            FROM pedidos p
            JOIN productos pr ON p.producto_id = pr.id          -- Unimos tablas pedidos y productos
            GROUP BY p.producto_id, pr.nombre, pr.precio        -- Agrupamos por producto
            ORDER BY total_vendido DESC                         -- Ordenamos por mas vendidos primero
        """)
        estadisticas = cur.fetchall()
        return estadisticas
