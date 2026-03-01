import sys
import os

# Agregamos la carpeta raíz del proyecto al camino de búsqueda de Python
ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_raiz)

from database.conexion import obtener_conexion

def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # ==========================================
    # 1. TABLAS PRINCIPALES
    # ==========================================
    
    # Tabla Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL,
            estado TEXT DEFAULT 'Activo',
            debe_cambiar_password INTEGER DEFAULT 1,
            id_usuario_registro INTEGER,
            id_usuario_actualizacion INTEGER,
            FOREIGN KEY (id_usuario_registro) REFERENCES usuarios (id_usuario),
            FOREIGN KEY (id_usuario_actualizacion) REFERENCES usuarios (id_usuario)
        )
    ''')
    
    # Tabla Agentes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agentes (
            id_agente INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_placa TEXT UNIQUE NOT NULL,
            nombre_completo TEXT NOT NULL,
            cargo TEXT,
            estado TEXT DEFAULT 'Activo',
            id_usuario_registro INTEGER NOT NULL,
            id_usuario_actualizacion INTEGER,
            FOREIGN KEY (id_usuario_registro) REFERENCES usuarios (id_usuario),
            FOREIGN KEY (id_usuario_actualizacion) REFERENCES usuarios (id_usuario)
        )
    ''')

    # Tabla Propietarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS propietarios (
            id_propietario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT NOT NULL,
            apellido_paterno TEXT NOT NULL,
            apellido_materno TEXT,
            curp TEXT UNIQUE NOT NULL,
            calle TEXT NOT NULL,
            numero_exterior TEXT NOT NULL,
            numero_interior TEXT,
            colonia TEXT NOT NULL,
            codigo_postal TEXT NOT NULL,
            ciudad TEXT NOT NULL,
            estado_provincia TEXT NOT NULL,
            telefono TEXT,
            correo_electronico TEXT,
            estado_licencia TEXT,
            estado TEXT DEFAULT 'Activo',
            id_usuario_registro INTEGER NOT NULL,
            id_usuario_actualizacion INTEGER,
            FOREIGN KEY (id_usuario_registro) REFERENCES usuarios (id_usuario),
            FOREIGN KEY (id_usuario_actualizacion) REFERENCES usuarios (id_usuario)
        )
    ''')

    # Tabla Vehículos
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
            id_usuario_registro INTEGER NOT NULL,
            id_usuario_actualizacion INTEGER,
            FOREIGN KEY (id_propietario) REFERENCES propietarios (id_propietario),
            FOREIGN KEY (id_usuario_registro) REFERENCES usuarios (id_usuario),
            FOREIGN KEY (id_usuario_actualizacion) REFERENCES usuarios (id_usuario)
        )
    ''')

    # Tabla Infracciones
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
            id_usuario_registro INTEGER NOT NULL,
            id_usuario_actualizacion INTEGER,
            FOREIGN KEY (vin_infractor) REFERENCES vehiculos (vin),
            FOREIGN KEY (id_agente) REFERENCES agentes (id_agente),
            FOREIGN KEY (id_usuario_registro) REFERENCES usuarios (id_usuario),
            FOREIGN KEY (id_usuario_actualizacion) REFERENCES usuarios (id_usuario)
        )
    ''')

    # ==========================================
    # 2. BITÁCORA (CAJA NEGRA)
    # ==========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bitacora_auditoria (
            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_hora DATETIME DEFAULT (datetime('now', 'localtime')),
            tabla_afectada TEXT NOT NULL,
            id_registro_afectado TEXT NOT NULL,
            tipo_accion TEXT NOT NULL, 
            detalles TEXT, 
            id_usuario INTEGER,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
        )
    ''')

    # ==========================================
    # 3. DISPARADORES (AUDITORÍA DETALLADA)
    # ==========================================

    # --- TRIGGERS VEHÍCULOS ---
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_vehiculos_insert AFTER INSERT ON vehiculos
        BEGIN
            INSERT INTO bitacora_auditoria (tabla_afectada, id_registro_afectado, tipo_accion, id_usuario, detalles)
            VALUES ('vehiculos', NEW.vin, 'CREACIÓN', NEW.id_usuario_registro, 'Registro inicial del vehículo');
        END;
    ''')

    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_vehiculos_update AFTER UPDATE ON vehiculos
        WHEN NEW.id_usuario_actualizacion IS NOT NULL 
        BEGIN
            INSERT INTO bitacora_auditoria (tabla_afectada, id_registro_afectado, tipo_accion, id_usuario, detalles)
            VALUES ('vehiculos', NEW.vin, 'ACTUALIZACIÓN', NEW.id_usuario_actualizacion,
                (CASE WHEN OLD.placa <> NEW.placa THEN 'Placa: ' || OLD.placa || ' -> ' || NEW.placa || ' | ' ELSE '' END) ||
                (CASE WHEN OLD.color <> NEW.color THEN 'Color: ' || OLD.color || ' -> ' || NEW.color || ' | ' ELSE '' END) ||
                (CASE WHEN OLD.estado_legal <> NEW.estado_legal THEN 'Estado: ' || OLD.estado_legal || ' -> ' || NEW.estado_legal ELSE '' END) ||
                (CASE WHEN OLD.id_propietario <> NEW.id_propietario THEN 'Cambio Dueño ID: ' || OLD.id_propietario || ' -> ' || NEW.id_propietario ELSE '' END)
            );
        END;
    ''')

    # --- TRIGGERS PROPIETARIOS ---
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_propietarios_insert AFTER INSERT ON propietarios
        BEGIN
            INSERT INTO bitacora_auditoria (tabla_afectada, id_registro_afectado, tipo_accion, id_usuario, detalles)
            VALUES ('propietarios', NEW.curp, 'CREACIÓN', NEW.id_usuario_registro, 'Alta de propietario en padrón');
        END;
    ''')

    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_propietarios_update AFTER UPDATE ON propietarios
        WHEN NEW.id_usuario_actualizacion IS NOT NULL
        BEGIN
            INSERT INTO bitacora_auditoria (tabla_afectada, id_registro_afectado, tipo_accion, id_usuario, detalles)
            VALUES ('propietarios', NEW.curp, 'ACTUALIZACIÓN', NEW.id_usuario_actualizacion,
                (CASE WHEN OLD.calle <> NEW.calle THEN 'Dirección actualizada | ' ELSE '' END) ||
                (CASE WHEN OLD.telefono <> NEW.telefono THEN 'Tel: ' || OLD.telefono || ' -> ' || NEW.telefono || ' | ' ELSE '' END) ||
                (CASE WHEN OLD.estado_licencia <> NEW.estado_licencia THEN 'Licencia: ' || OLD.estado_licencia || ' -> ' || NEW.estado_licencia || ' | ' ELSE '' END) ||
                (CASE WHEN OLD.estado <> NEW.estado THEN 'Estado: ' || OLD.estado || ' -> ' || NEW.estado ELSE '' END)
            );
        END;
    ''')

    # --- TRIGGERS INFRACCIONES ---
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_infracciones_insert AFTER INSERT ON infracciones
        BEGIN
            INSERT INTO bitacora_auditoria (tabla_afectada, id_registro_afectado, tipo_accion, id_usuario, detalles)
            VALUES ('infracciones', NEW.folio, 'CREACIÓN', NEW.id_usuario_registro, 'Emisión de boleta de infracción');
        END;
    ''')

    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_infracciones_update AFTER UPDATE ON infracciones
        WHEN NEW.id_usuario_actualizacion IS NOT NULL
        BEGIN
            INSERT INTO bitacora_auditoria (tabla_afectada, id_registro_afectado, tipo_accion, id_usuario, detalles)
            VALUES ('infracciones', NEW.folio, 'ACTUALIZACIÓN', NEW.id_usuario_actualizacion,
                'Estado multa: ' || OLD.estado || ' -> ' || NEW.estado
            );
        END;
    ''')

    # --- TRIGGERS USUARIOS ---
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_usuarios_insert AFTER INSERT ON usuarios
        WHEN NEW.id_usuario_registro IS NOT NULL
        BEGIN
            INSERT INTO bitacora_auditoria (tabla_afectada, id_registro_afectado, tipo_accion, id_usuario, detalles)
            VALUES ('usuarios', NEW.nombre_usuario, 'CREACIÓN', NEW.id_usuario_registro, 'Nuevo acceso creado');
        END;
    ''')

    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS trg_usuarios_update AFTER UPDATE ON usuarios
        WHEN NEW.id_usuario_actualizacion IS NOT NULL
        BEGIN
            INSERT INTO bitacora_auditoria (tabla_afectada, id_registro_afectado, tipo_accion, id_usuario, detalles)
            VALUES ('usuarios', NEW.nombre_usuario, 'ACTUALIZACIÓN', NEW.id_usuario_actualizacion,
                (CASE WHEN OLD.rol <> NEW.rol THEN 'Rol: ' || OLD.rol || ' -> ' || NEW.rol || ' | ' ELSE '' END) ||
                (CASE WHEN OLD.estado <> NEW.estado THEN 'Estado: ' || OLD.estado || ' -> ' || NEW.estado ELSE '' END)
            );
        END;
    ''')

    conexion.commit()
    conexion.close()
    print("Base de datos inicializada con Auditoría Nivel Detalle.")

if __name__ == "__main__":
    crear_tablas()