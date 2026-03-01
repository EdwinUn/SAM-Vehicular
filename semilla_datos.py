import sys
import os
import time

# Aseguramos que Python encuentre tus módulos
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_raiz)

from database.conexion import obtener_conexion
from logic.auth import Auth
from models.usuario import Usuario
import logic.catalogos as cat

def generar_datos_prueba():
    print("==================================================")
    print("🚀 INICIANDO CARGA Y SIMULACIÓN DE TRÁMITES")
    print("==================================================")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # 1. USUARIOS (Base para la auditoría)
        usuarios_test = [
            ("admin_central", "admin123", cat.ROLES_USUARIO[0]),
            ("operador_1", "operador123", cat.ROLES_USUARIO[1]),
            ("agente_007", "agente123", cat.ROLES_USUARIO[2]),
            ("supervisor_general", "super123", cat.ROLES_USUARIO[3])
        ]
        for nom, pwd, rol in usuarios_test:
            u = Usuario(nombre_usuario=nom, password=pwd, rol=rol, id_usuario_registro=1)
            Auth.registrar_usuario(u)

        # 2. AGENTES
        agentes = [
            ("AG-101", "Oficial Ricardo Milos", "Patrullero", cat.ESTADOS_AGENTE[0], 1), 
            ("AG-102", "Oficial Sarah Connor", "Vialidad", cat.ESTADOS_AGENTE[0], 1)
        ]
        cursor.executemany('''INSERT OR IGNORE INTO agentes 
            (numero_placa, nombre_completo, cargo, estado, id_usuario_registro) 
            VALUES (?,?,?,?,?)''', agentes)

        # 3. PROPIETARIOS
        propietarios = [
            ("Juan", "Pérez", "López", "PELJ800101HDFRRN01", "Calle 60", "123", "", "Centro", "97000", "Mérida", "Yucatán", "9991234567", "juan@mail.com", cat.ESTADOS_LICENCIA[0], 1),
            ("María", "García", "Sosa", "GASM900505MDFRRN02", "Av. Itzaes", "456", "", "García Ginerés", "97070", "Mérida", "Yucatán", "9997654321", "maria@mail.com", cat.ESTADOS_LICENCIA[0], 1),
            ("Carlos", "López", "Ruiz", "LORC750312HDFRRN03", "Calle 50", "789", "A", "Pacabtún", "97160", "Mérida", "Yucatán", "9995551122", "carlos.lopez@mail.com", cat.ESTADOS_LICENCIA[1], 1)
        ]
        cursor.executemany('''INSERT OR IGNORE INTO propietarios 
            (nombres, apellido_paterno, apellido_materno, curp, calle, numero_exterior, 
            numero_interior, colonia, codigo_postal, ciudad, estado_provincia, 
            telefono, correo_electronico, estado_licencia, id_usuario_registro) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', propietarios)
        
        # 4. VEHÍCULOS
        vehiculos = [
            ("VIN00000000000001", "YUC-1001", "Toyota", "Corolla", 2022, "Gris", "Sedán", "Nacional", 1, 1),
            ("VIN00000000000002", "YUC-2001", "Nissan", "NP300", 2023, "Blanco", "Camioneta", "Nacional", 2, 1),
            ("VIN00000000000003", "YUC-3001", "Chevrolet", "Chevy", 2010, "Negro", "Hatchback", "Importado", 3, 1)
        ]
        cursor.executemany('''INSERT OR IGNORE INTO vehiculos 
            (vin, placa, marca, modelo, anio, color, clase, procedencia, id_propietario, id_usuario_registro) 
            VALUES (?,?,?,?,?,?,?,?,?,?)''', vehiculos)

        # 5. INFRACCIONES
        infracciones = [
            ("FOL-00001", "VIN00000000000001", 1, "2026-02-20", "10:30", "Centro", "Exceso de velocidad", "Art. 64", 1500.0, cat.ESTADOS_INFRACCION[0], 1),
            ("FOL-00002", "VIN00000000000002", 2, "2026-01-15", "14:15", "Periférico", "Estacionamiento prohibido", "Art. 75", 850.0, cat.ESTADOS_INFRACCION[0], 1)
        ]
        cursor.executemany('''INSERT OR IGNORE INTO infracciones 
            (folio, vin_infractor, id_agente, fecha, hora, lugar, tipo_infraccion, motivo, monto, estado, id_usuario_registro) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', infracciones)

        conexion.commit()

        # ==========================================
        # 6. SIMULACIÓN DE TRÁMITES (AUDITORÍA DETALLADA)
        # ==========================================
        print("🕒 Simulando transacciones para la bitácora...")
        time.sleep(1) 

        # Trámite A: Reemplacamiento y Cambio de Color (Hecho por Operador 1)
        cursor.execute('''
            UPDATE vehiculos 
            SET placa = 'YUC-9999', color = 'Rojo', id_usuario_actualizacion = 2 
            WHERE vin = 'VIN00000000000001'
        ''')

        # Trámite B: Transferencia de Propiedad (Juan -> María)
        cursor.execute('''
            UPDATE vehiculos 
            SET id_propietario = 2, id_usuario_actualizacion = 2 
            WHERE vin = 'VIN00000000000001'
        ''')

        # Trámite C: Pago de Multa y Reporte de Robo (Hecho por Admin)
        cursor.execute('''
            UPDATE infracciones SET estado = ?, id_usuario_actualizacion = 1 WHERE folio = 'FOL-00002'
        ''', (cat.ESTADOS_INFRACCION[1],))
        
        cursor.execute('''
            UPDATE vehiculos SET estado_legal = ?, id_usuario_actualizacion = 1 WHERE vin = 'VIN00000000000003'
        ''', (cat.ESTADOS_VEHICULO[2],))

        # Trámite D: Actualización de datos de Propietario (Cambio de teléfono y licencia)
        cursor.execute('''
            UPDATE propietarios 
            SET telefono = '9990001122', estado_licencia = ?, id_usuario_actualizacion = 1
            WHERE curp = 'PELJ800101HDFRRN01'
        ''', (cat.ESTADOS_LICENCIA[2],))

        conexion.commit()

        print("\n✅ Simulación completada.")
        print("\n" + "="*65)
        print(" GUÍA PARA LA PRESENTACIÓN DE MAÑANA 🎓")
        print("="*65)
        print("\n1. MUESTRA EL DASHBOARD: Los números ya reflejan el auto robado y la multa pagada.")
        print("\n2. EL PLATO FUERTE (REPORTE 11):")
        print("   - Abre 'Reportes' -> '11. Historial Completo de Movimientos'.")
        print("   - Señala la columna 'Detalles del Cambio'.")
        print("   - Muestra cómo el sistema detectó que el auto VIN...01 cambió de placa 'YUC-1001' a 'YUC-9999'.")
        print("   - Muestra cómo registró que el color pasó de 'Gris' a 'Rojo'.")
        print("\n3. SEGREGACIÓN DE FUNCIONES:")
        print("   - Explica que el 'operador_1' hizo los trámites de placas, pero el 'admin' gestionó la seguridad.")
        print("\n" + "="*65)

    except Exception as e:
        print(f"\n❌ Error grave al cargar semilla: {e}")
    finally:
        conexion.close()

if __name__ == "__main__":
    generar_datos_prueba()