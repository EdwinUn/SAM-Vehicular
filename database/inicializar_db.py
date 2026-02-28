import sys
import os

# Agregamos la carpeta raíz del proyecto al camino de búsqueda de Python
ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_raiz)

from database.conexion import obtener_conexion
def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()


# 1. Tabla Propietarios [cite: 398, 400]
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS propietarios (
            id_propietario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT NOT NULL,
            curp TEXT UNIQUE NOT NULL,
            direccion TEXT,
            telefono TEXT,
            correo_electronico TEXT,
            estado_licencia TEXT,
            estado TEXT DEFAULT 'Activo'
        )
    ''')

# 2. Tabla Vehículos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            vin TEXT PRIMARY KEY,
            placa TEXT UNIQUE NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            anio INTEGER NOT NULL,
            color TEXT,
            clase TEXT NOT NULL,
            estado_legal TEXT DEFAULT 'Activo',
            procedencia TEXT NOT NULL,
            id_propietario INTEGER NOT NULL,
            FOREIGN KEY (id_propietario) REFERENCES propietarios (id_propietario)
        )
    ''')

# 3. Tabla Agentes de Tránsito
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agentes (
            id_agente INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_placa TEXT UNIQUE NOT NULL,
            nombre_completo TEXT NOT NULL,
            cargo TEXT,
            estado TEXT DEFAULT 'Activo'
        )
    ''')

    # 4. Tabla Infracciones (Multas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS infracciones (
            folio TEXT PRIMARY KEY,
            vin_infractor TEXT NOT NULL,
            id_agente INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            lugar TEXT NOT NULL,
            tipo_infraccion TEXT NOT NULL,
            motivo TEXT,
            monto REAL NOT NULL,
            licencia_conductor TEXT,
            estado TEXT DEFAULT 'Pendiente',
            
            -- NUEVAS COLUMNAS DE AUDITORÍA
            id_usuario_registro INTEGER NOT NULL,
            id_usuario_actualizacion INTEGER,
            
            FOREIGN KEY (vin_infractor) REFERENCES vehiculos (vin),
            FOREIGN KEY (id_agente) REFERENCES agentes (id_agente),
            FOREIGN KEY (id_usuario_registro) REFERENCES usuarios (id_usuario),
            FOREIGN KEY (id_usuario_actualizacion) REFERENCES usuarios (id_usuario)
        )
    ''')

    # 5. Tabla Usuarios (Para el Login y seguridad)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL,
            estado TEXT DEFAULT 'Activo',
            debe_cambiar_password INTEGER DEFAULT 1 
        )
    ''')

    conexion.commit()
    conexion.close()
    print("Base de datos y tablas creadas exitosamente.")

if __name__ == "__main__":
    crear_tablas()