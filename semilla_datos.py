import sys
import os

# Aseguramos que Python encuentre tus módulos
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_raiz)

from database.conexion import obtener_conexion
from logic.auth import Auth
from models.usuario import Usuario

def generar_datos_prueba():
    print(" Iniciando carga de datos de prueba...")
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # 1. GENERAR USUARIOS
        usuarios_test = [
            ("admin_central", "admin123", "Administrador"),
            ("operador_1", "operador123", "Operador Administrativo"),
            ("agente_007", "agente123", "Agente de Tránsito"),
            ("supervisor_general", "super123", "Supervisor")
        ]
        for nom, pwd, rol in usuarios_test:
            
            u = Usuario(nombre_usuario=nom, password=pwd, rol=rol, id_usuario_registro=1)
            Auth.registrar_usuario(u)
        print("✅ Usuarios con roles creados.")

        # 2. GENERAR AGENTES DE TRÁNSITO
        agentes = [
            ("AG-101", "Oficial Ricardo Milos", "Patrullero", "Activo", 1), # <-- El 1 final es el ID del Admin
            ("AG-102", "Oficial Sarah Connor", "Vialidad", "Activo", 1)
        ]
        
        cursor.executemany('''INSERT OR IGNORE INTO agentes 
            (numero_placa, nombre_completo, cargo, estado, id_usuario_registro) 
            VALUES (?,?,?,?,?)''', agentes)

        # 3. GENERAR PROPIETARIOS
        propietarios = [
            ("Juan Pérez López", "PELJ800101HDFRRN01", "Calle 60 #123, Mérida", "9991234567", "juan@mail.com", "Vigente", 1),
            ("María García Sosa", "GASM900505MDFRRN02", "Av. Itzaes #456, Mérida", "9997654321", "maria@mail.com", "Vigente", 1)
        ]
        
        cursor.executemany('''INSERT OR IGNORE INTO propietarios 
            (nombre_completo, curp, direccion, telefono, correo_electronico, estado_licencia, id_usuario_registro) 
            VALUES (?,?,?,?,?,?,?)''', propietarios)

        # 4. GENERAR VEHÍCULOS
        vehiculos = [
            ("1A2B3C4D5E6F7G8H9", "YUC-1234", "Toyota", "Corolla", 2022, "Gris", "Sedán", "Nacional", 1, 1),
            ("9H8G7F6E5D4C3B2A1", "YUC-9999", "Nissan", "Versa", 2021, "Blanco", "Sedán", "Nacional", 2, 1)
        ]
        
        cursor.executemany('''INSERT OR IGNORE INTO vehiculos 
            (vin, placa, marca, modelo, anio, color, clase, procedencia, id_propietario, id_usuario_registro) 
            VALUES (?,?,?,?,?,?,?,?,?,?)''', vehiculos)

        # 5. GENERAR UNA INFRACCIÓN PENDIENTE
        
        cursor.execute('''INSERT OR IGNORE INTO infracciones 
            (folio, vin_infractor, id_agente, fecha, hora, lugar, tipo_infraccion, motivo, monto, estado, id_usuario_registro) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', 
            ("FOL-00001", "1A2B3C4D5E6F7G8H9", 1, "2026-02-20", "10:30", "Centro Histórico", "Exceso de velocidad", "Art. 45", 1500.0, "Pendiente", 1))

        conexion.commit()
        print(" Datos de prueba cargados exitosamente.")
        print("\nPrueba de bloqueo lista: El vehículo Toyota (YUC-1234) tiene una multa pendiente.")
        print("No se podrá transferir ni reemplacar hasta que se pague. ")

    except Exception as e:
        print(f" Error al cargar semilla: {e}")
    finally:
        conexion.close()

if __name__ == "__main__":
    generar_datos_prueba()