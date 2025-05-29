import sqlite3  
     

# Nombre del archivo de nuestra base de datos
DB_NAME = "usuarios.db"

def inicializar_db():
    """
    Crea la base de datos y la tabla de usuarios si no existen.
    """
    # sqlite3.connect() abre una conexión a la base de datos
    # Si el archivo no existe, se crea automáticamente
    # 'with' al igual que en el ejemplo de open, asegura que la conexión a la base de datos se cierre automáticamente
    with sqlite3.connect(DB_NAME) as conn:
        
        # El "puntero" que nos permite ejecutar comandos SQL
        cursor = conn.cursor()
        
        # Ejecutamos un comando SQL para crear la tabla
        # CREATE TABLE IF NOT EXISTS = "crear la tabla solo si no existe"
        # Los comentarios en SQL empiezan con -- 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                username TEXT PRIMARY KEY,    -- Nombre de usuario (único, no se puede repetir)
                password TEXT NOT NULL,       -- Contraseña (obligatoria)
                email TEXT NOT NULL,          -- Correo electrónico (obligatorio)
                role TEXT NOT NULL            -- Tipo de usuario: "user", "admin", etc. (obligatorio)
            )
        ''')
        
        # conn.commit() guarda los cambios
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

def validar_usuario(usuario, contraseña, correo, tipo_usuario):
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

