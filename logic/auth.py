import sqlite3
import hashlib
from database.conexion import obtener_conexion
from models.usuario import Usuario
import logic.catalogos as cat

class Auth:
    
    @staticmethod
    def _hashear_password(password: str) -> str:
        """
        Método privado para encriptar la contraseña usando SHA-256.
        Garantiza que las contraseñas no se guarden en texto plano.
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def registrar_usuario(usuario):
        """
        Registra un nuevo usuario en el sistema.
        Según las especificaciones, esta acción solo debería estar disponible 
        para un usuario con rol 'Administrador'.
        """
        # 1. Validar reglas básicas
        if not usuario.nombre_usuario or len(usuario.nombre_usuario.strip()) < 4:
            return False, "Error: El nombre de usuario debe tener al menos 4 caracteres."
            
        if not usuario.password or len(usuario.password) < 6:
            return False, "Error: La contraseña debe tener al menos 6 caracteres."

        if usuario.rol not in cat.ROLES_USUARIO:
            return False, "Error: El rol seleccionado no es válido."

        # 2. Encriptar la contraseña antes de guardarla
        password_hash = Auth._hashear_password(usuario.password)

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO usuarios (nombre_usuario, password, rol, estado)
                VALUES (?, ?, ?, ?)
            ''', (usuario.nombre_usuario, password_hash, usuario.rol, usuario.estado))
            
            conexion.commit()
            return True, "Usuario registrado exitosamente."
            
        except sqlite3.IntegrityError:
            return False, "Error: El nombre de usuario ya está en uso. Elija uno diferente."
        except Exception as e:
            return False, f"Error inesperado al registrar usuario: {str(e)}"
        finally:
            conexion.close()

    @staticmethod
    def autenticar_usuario(nombre_usuario, password_plana):
        """
        Verifica las credenciales de inicio de sesión.
        Retorna una tupla: (es_valido: bool, objeto_usuario: Usuario o None, mensaje: str)
        """
        if not nombre_usuario or not password_plana:
            return False, None, "Error: Debe ingresar usuario y contraseña."

        password_hash = Auth._hashear_password(password_plana)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            # Buscamos al usuario por nombre y contraseña encriptada
            cursor.execute('''
                SELECT id_usuario, nombre_usuario, rol, estado 
                FROM usuarios 
                WHERE nombre_usuario = ? AND password = ?
            ''', (nombre_usuario, password_hash))
            
            resultado = cursor.fetchone()

            if not resultado:
                return False, None, "Error: Credenciales incorrectas."

            id_usuario, nombre_db, rol_db, estado_db = resultado

            # Regla de negocio: No permitir el acceso a usuarios inactivos
            if estado_db != "Activo":
                return False, None, "Error: Su cuenta de usuario está inactiva. Contacte al administrador."

            # Si todo está correcto, reconstruimos el modelo Usuario para enviarlo a la interfaz
            usuario_autenticado = Usuario(
                id_usuario=id_usuario,
                nombre_usuario=nombre_db,
                password="***", # Por seguridad, no devolvemos el hash a la memoria de la interfaz
                rol=rol_db,
                estado=estado_db
            )

            return True, usuario_autenticado, f"Bienvenido, {nombre_db}. Su rol es {rol_db}."

        except Exception as e:
            return False, None, f"Error inesperado al intentar iniciar sesión: {str(e)}"
        finally:
            conexion.close()