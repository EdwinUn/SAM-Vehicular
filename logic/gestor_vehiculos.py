import sqlite3
from database.conexion import obtener_conexion
from logic.validador import Validador

class GestorVehiculos:
    
    @staticmethod
    def registrar_vehiculo(vehiculo):
        """Recibe un objeto Vehiculo, verifica sus reglas de negocio y lo guarda."""
        
        # 1. Validaciones estructurales, de formato y de catálogos
        # Estas validaciones evitan viajes innecesarios a la base de datos.
        
        valido, msj = Validador.validar_vin(vehiculo.vin)
        if not valido: return False, msj
        
        valido, msj = Validador.validar_placa(vehiculo.placa)
        if not valido: return False, msj

        valido, msj = Validador.validar_anio_vehiculo(vehiculo.anio)
        if not valido: return False, msj

        valido, msj = Validador.validar_estado_vehiculo(vehiculo.estado_legal)
        if not valido: return False, msj
        
        valido, msj = Validador.validar_procedencia_vehiculo(vehiculo.procedencia)
        if not valido: return False, msj

        valido, msj = Validador.validar_marca_modelo_clase(vehiculo.marca, vehiculo.modelo, vehiculo.clase)
        if not valido: return False, msj

        valido, msj = Validador.validar_color_vehiculo(vehiculo.color)
        if not valido: return False, msj

        valido, msj = Validador.validar_id_propietario(vehiculo.id_propietario)
        if not valido: return False, msj
        
        
        # 2. Guardar en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # Regla de negocio: Verificar que el propietario asociado exista
            cursor.execute("SELECT id_propietario FROM propietarios WHERE id_propietario = ?", (vehiculo.id_propietario,))
            if not cursor.fetchone():
                return False, "Error: El ID del propietario no existe en el sistema."

            cursor.execute('''
                INSERT INTO vehiculos (vin, placa, marca, modelo, anio, color, clase, estado_legal, procedencia, id_propietario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (vehiculo.vin, vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.anio, 
                vehiculo.color, vehiculo.clase, vehiculo.estado_legal, vehiculo.procedencia, vehiculo.id_propietario))
            
            conexion.commit()
            return True, "Vehículo registrado correctamente."
            
        except sqlite3.IntegrityError as e:
            error_str = str(e).lower()
            # Interceptamos las restricciones UNIQUE de la base de datos
            if 'vin' in error_str:
                return False, "Error: El VIN ingresado ya está registrado. Es único e inmutable."
            elif 'placa' in error_str:
                return False, "Error: La placa ingresada ya está asignada a otro vehículo activo."
            else:
                return False, "Error de integridad en la base de datos."
        except Exception as e:
            return False, f"Error inesperado al registrar vehículo: {str(e)}"
        finally:
            conexion.close()

    @staticmethod
    def buscar_vehiculo_por_vin(vin: str) -> tuple[bool, str | dict]:
        """
        Busca un vehículo por su VIN y retorna todos sus datos para mostrarlos en la interfaz.
        """
        try:
            # --- AQUÍ USAMOS TU FUNCIÓN OFICIAL ---
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Ahora traemos toda la fila
            cursor.execute('''
                SELECT placa, marca, modelo, anio, color, clase, estado_legal, procedencia, id_propietario 
                FROM vehiculos 
                WHERE vin = ?
            ''', (vin,))
            
            resultado = cursor.fetchone()
            
            if resultado:
                # Empaquetamos todo el vehículo
                datos_vehiculo = {
                    "placa": resultado[0],
                    "marca": resultado[1],
                    "modelo": resultado[2],
                    "anio": resultado[3],
                    "color": resultado[4],
                    "clase": resultado[5],
                    "estado_legal": resultado[6],
                    "procedencia": resultado[7],
                    "id_propietario": resultado[8]
                }
                return True, datos_vehiculo
            else:
                return False, "No se encontró ningún vehículo registrado con ese VIN."
                
        except Exception as e:
            return False, f"Error al buscar en la base de datos: {str(e)}"
        finally:
            if 'conexion' in locals():
                conexion.close()


    @staticmethod
    def actualizar_vehiculo(vin: str, color: str, estado_legal: str) -> tuple[bool, str]:
        """
        Actualiza únicamente los campos permitidos (color y estado_legal) de un vehículo existente.
        """
        # (Opcional) Aquí podrías llamar al Validador.validar_color_vehiculo si lo deseas, 
        # aunque el QComboBox del frontend ya nos protege bastante.
        
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            # Ejecutamos el comando UPDATE de SQL
            cursor.execute('''
                UPDATE vehiculos 
                SET color = ?, estado_legal = ? 
                WHERE vin = ?
            ''', (color, estado_legal, vin))
            
            # Verificamos si realmente se modificó alguna fila
            if cursor.rowcount == 0:
                return False, "No se pudo actualizar. El vehículo no existe o no hubo cambios."
                
            conexion.commit()
            return True, "Datos del vehículo actualizados correctamente."
            
        except Exception as e:
            return False, f"Error al actualizar en la base de datos: {str(e)}"
        finally:
            if 'conexion' in locals():
                conexion.close()
    
    
    @staticmethod
    def modificar_vehiculo(vin, nueva_placa, nuevo_color, nuevo_estado_legal):
        """
        Modifica los datos permitidos de un vehículo (Placa, Color, Estado legal).
        Bloquea el trámite si hay infracciones pendientes.
        No permite modificar atributos inmutables como VIN, Marca, Modelo, Año, Clase ni Procedencia[cite: 229, 230, 231, 232, 233, 234, 235].
        """
        # 1. Validaciones de formato y catálogos
        valido, msj = Validador.validar_placa(nueva_placa)
        if not valido: return False, msj

        valido, msj = Validador.validar_estado_vehiculo(nuevo_estado_legal)
        if not valido: return False, msj

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            # 2. Regla de negocio: Bloquear trámite administrativo si hay infracciones pendientes [cite: 180, 236]
            cursor.execute('''
                SELECT COUNT(*) FROM infracciones 
                WHERE vin_infractor = ? AND estado = 'Pendiente'
            ''', (vin,))
            
            if cursor.fetchone()[0] > 0:
                return False, "Error: El vehículo tiene infracciones pendientes. Trámite bloqueado."

            # 3. Regla de negocio: Garantizar que la nueva placa sea única [cite: 178]
            # Revisamos que no exista OTRO vehículo (diferente VIN) activo con esa misma placa [cite: 175]
            cursor.execute('''
                SELECT vin FROM vehiculos 
                WHERE placa = ? AND vin != ? AND estado_legal = 'Activo'
            ''', (nueva_placa, vin))
            
            if cursor.fetchone():
                return False, "Error: La nueva placa ya está asignada a otro vehículo activo."

            # 4. Ejecutar la actualización solo en los campos permitidos
            cursor.execute('''
                UPDATE vehiculos 
                SET placa = ?, color = ?, estado_legal = ?
                WHERE vin = ?
            ''', (nueva_placa, nuevo_color, nuevo_estado_legal, vin))

            if cursor.rowcount == 0:
                return False, "Error: No se encontró el vehículo con el VIN especificado."

            conexion.commit()
            return True, "Datos del vehículo actualizados correctamente."

        except sqlite3.IntegrityError:
            # Respaldo por si la base de datos lanza error de unicidad (UNIQUE constraint)
            return False, "Error de integridad: La placa ingresada ya existe en el sistema."
        except Exception as e:
            return False, f"Error inesperado al modificar vehículo: {str(e)}"
        finally:
            conexion.close()
            
    @staticmethod
    def tiene_multas_pendientes(vin):
        """Verifica si el vehículo tiene deudas. Regla de negocio [4.2.vii]"""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM infracciones WHERE vin_infractor = ? AND estado = 'Pendiente'", (vin,))
        resultado = cursor.fetchone()[0]
        conexion.close()
        return resultado > 0

    @staticmethod
    def realizar_reemplacamiento(vin, nueva_placa):
        """Actualiza la placa validando unicidad y multas."""
        if GestorVehiculos.tiene_multas_pendientes(vin):
            return False, "Trámite Bloqueado: El vehículo tiene infracciones pendientes de pago."
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE vehiculos SET placa = ? WHERE vin = ?", (nueva_placa, vin))
            conexion.commit()
            return True, "Reemplacamiento exitoso."
        except sqlite3.IntegrityError:
            return False, "Error: La placa ya está registrada en otro vehículo activo."
        finally:
            conexion.close()

    @staticmethod
    def transferir_propiedad(vin, id_nuevo_propietario):
        """Cambia el dueño validando existencia, estado y multas."""
        if GestorVehiculos.tiene_multas_pendientes(vin):
            return False, "Trámite Bloqueado: No se puede transferir un vehículo con multas pendientes."
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            # Validar que el nuevo propietario existe y está activo [4.3.vi]
            cursor.execute("SELECT estado FROM propietarios WHERE id_propietario = ?", (id_nuevo_propietario,))
            propietario = cursor.fetchone()
            
            if not propietario or propietario[0] != "Activo":
                return False, "Error: El propietario destino no existe o está inactivo."

            cursor.execute("UPDATE vehiculos SET id_propietario = ? WHERE vin = ?", (id_nuevo_propietario, vin))
            conexion.commit()
            return True, "Transferencia de propiedad realizada correctamente."
        finally:
            conexion.close()