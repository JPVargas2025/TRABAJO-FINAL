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
                username TEXT PRIMARY KEY,    -- Nombre de usuario (único, no se puede repetir)
                password TEXT NOT NULL,       -- Contraseña (obligatoria)
                email TEXT NOT NULL,          -- Correo electrónico (obligatorio)
                role TEXT NOT NULL            -- Tipo de usuario: "user", "admin", etc. (obligatorio)
            )
        ''')
        # tabla productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,   -- ID único para cada producto (se incrementa automáticamente)
                categoria TEXT,                        -- Categoría del producto (opcional)
                nombre TEXT NOT NULL,                  -- Nombre del producto (obligatorio)
                precio REAL NOT NULL                   -- Precio del producto (obligatorio)
            )
        ''')

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)
        
        conn.commit()

def registrar_usuario(usuario, contraseña, correo,tipo_usuario="user"):
    """
    Esta función registra un nuevo usuario en la base de datos.
    Por defecto, el tipo_usuario será "user".

    Retorna:
    bool: True si el registro fue exitoso,False si el usuario ya existe.
    """
    # Primero nos aseguramos de que la base de datos y tabla existan
    inicializar_db()
    
    # Abrimos conexión a la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        try:
            # INSERT INTO = insertar datos en la tabla
            # Los signos ? son "placeholders" para los valores que vamos a insertar
            # SQLite los reemplaza con los valores que pasamos en la tupla
            # Evita ataques de "SQL injection"
            cursor.execute("INSERT INTO usuarios (username, password, email, role) VALUES (?, ?, ?, ?)",
                           (usuario, contraseña, correo, tipo_usuario))
            
            # Guardamos los cambios
            conn.commit()
            
            # Si todo salió bien, devolvemos True
            return True
            
        except sqlite3.IntegrityError:
            # Esta excepción ocurre cuando intentamos insertar un username que ya existe
            # (porque username es PRIMARY KEY, debe ser único)
            return False

def validar_usuario_db(usuario, contraseña, correo, tipo_usuario):
    """
    verifica si un usuario existe con todos los datos proporcionados.  
    Retorna:
    tuple: Una tupla con los datos del usuario si existe
    None: Si no se encuentra ningún usuario con todos los datos especificados
    """
    # Nos aseguramos de que la base de datos existe
    inicializar_db()
    
    # Abrimos conexión
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # SELECT = seleccionar/buscar datos
        # * significa "todos los campos" (username, password, email, role)
        # FROM = de qué tabla queremos buscar
        # WHERE = condiciones para filtrar
        cursor.execute('''
            SELECT * FROM usuarios
            WHERE username = ? AND password = ? AND email = ? AND role = ?
        ''', (usuario, contraseña, correo, tipo_usuario))
        
        # fetchone() devuelve el primer resultado encontrado
        # Si no encuentra nada, devuelve None
        # Si encuentra algo, devuelve una tupla con todos los datos del usuario
        return cursor.fetchone()
    


def agregar_producto_db(nombre, categoria, precio):
   with sqlite3.connect(DB_NAME) as conn:
    conn = conn
    cur = conn.cursor()
    cur.execute("INSERT INTO productos (nombre,categoria, precio) VALUES (?, ?, ?)", ( nombre, categoria, precio))
    conn.commit()

def obtener_productos_db():
   with sqlite3.connect(DB_NAME) as conn:
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, categoria, precio FROM productos")
    productos = cur.fetchall()
    return productos

def buscar_producto_db(nombre):
   with sqlite3.connect(DB_NAME) as conn:
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, categoria, precio FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
    resultado = cur.fetchall()
    return resultado

def hacer_pedido_db(usuario, producto_id, cantidad):
   """ Permite a un usuario realizar un pedido y lo registra en la base de datos.
   Solicita el nombre del usuario, el ID del producto y la cantidad."""

   with sqlite3.connect(DB_NAME) as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO pedidos (usuario, producto_id, cantidad) VALUES (?, ?, ?)", (usuario, producto_id, cantidad))
    conn.commit()

def obtener_pedidos_usuario(usuario):
   with sqlite3.connect(DB_NAME) as conn:
    cur = conn.cursor()
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
    """Obtiene todos los usernames de usuarios registrados"""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM usuarios")
        usuarios = cur.fetchall()
        return [usuario[0] for usuario in usuarios]

def obtener_estadisticas_ventas():
    """Obtiene estadísticas de ventas por producto"""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                pr.nombre as producto,
                SUM(p.cantidad) as total_vendido,
                pr.precio as precio_unitario,
                SUM(p.cantidad * pr.precio) as total_ingresos
            FROM pedidos p
            JOIN productos pr ON p.producto_id = pr.id
            GROUP BY p.producto_id, pr.nombre, pr.precio
            ORDER BY total_vendido DESC
        """)
        estadisticas = cur.fetchall()
        return estadisticas
