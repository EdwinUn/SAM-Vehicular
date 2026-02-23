import re
from datetime import datetime
import logic.catalogos as cat

#TODO Mejora
class Validador:
    """
    Clase centralizada para validaciones de formato, longitud y catálogos.
    No interactúa con la base de datos.
    Retorna siempre una tupla: (es_valido: bool, mensaje_error: str)
    """

    # =========================
    # VALIDACIONES DE VEHÍCULOS
    # =========================
    
    @staticmethod
    def validar_vin(vin: str) -> tuple[bool, str]:
        if len(vin) != 17:
            return False, "El VIN debe tener exactamente 17 caracteres."
        return True, ""

    @staticmethod
    def validar_placa(placa: str) -> tuple[bool, str]:
        if not placa or placa.strip() == "":
            return False, "La placa no puede quedar vacía."
        # Aquí puedes agregar un Regex específico si el municipio tiene un formato exacto.
        return True, ""

    @staticmethod
    def validar_anio_vehiculo(anio: int) -> tuple[bool, str]:
        anio_actual = datetime.now().year
        if not isinstance(anio, int):
            return False, "El año del vehículo debe ser un valor numérico."
        if anio < 1900 or anio > anio_actual:
            return False, f"El año debe estar en el rango de 1900 a {anio_actual}."
        return True, ""

    @staticmethod
    def validar_clase_vehiculo(clase: str) -> tuple[bool, str]:
        if clase not in cat.CLASES_VEHICULO:
            return False, "La clase de vehículo seleccionada no es válida."
        return True, ""

    @staticmethod
    def validar_procedencia_vehiculo(clase: str) -> tuple[bool, str]:
        if clase not in cat.PROCEDENCIAS_VEHICULO:
            return False, "La procedencia de vehículo seleccionada no es válida."
        return True, ""

    @staticmethod
    def validar_estado_vehiculo(estado: str) -> tuple[bool, str]:
        if estado not in cat.ESTADOS_VEHICULO:
            return False, "El estado legal del vehículo seleccionado no es válido."
        return True, ""

    @staticmethod
    def validar_marca_modelo(marca: str, modelo: str) -> tuple[bool, str]:
        """
        Valida que la marca exista en el catálogo y que el modelo corresponda a dicha marca.
        """
        if marca not in cat.MARCAS_MODELOS_VEHICULO:
            return False, "La marca seleccionada no es válida o no está registrada en el sistema."
        
        # Si la marca es válida, verificamos que el modelo pertenezca a su lista
        modelos_permitidos = cat.MARCAS_MODELOS_VEHICULO[marca]
        if modelo not in modelos_permitidos:
            return False, f"El modelo '{modelo}' no es válido para la marca '{marca}'."
            
        return True, ""

    @staticmethod
    def validar_color_vehiculo(color: str) -> tuple[bool, str]:
        """
        Valida que el color se encuentre dentro del catálogo cerrado.
        """
        if color not in cat.COLORES_VEHICULO:
            return False, "El color ingresado no es válido. Seleccione uno de la lista."
        return True, ""
    
    @staticmethod
    def validar_id_propietario(id_propietario: int) -> tuple[bool, str]:
        """
        Valida únicamente el formato numérico del ID interno.
        La existencia real del propietario en la base de datos se verifica en el Gestor.
        """
        if not isinstance(id_propietario, int) or isinstance(id_propietario, bool):
            return False, "El ID del propietario debe ser un valor numérico entero."
        if id_propietario <= 0:
            return False, "El ID del propietario debe ser mayor a cero."
            
        return True, ""

    # =========================
    # VALIDACIONES DE PROPIETARIOS
    # =========================

    @staticmethod
    def validar_curp(curp: str) -> tuple[bool, str]:
        patron_curp = r'^[A-Z0-9]{18}$' 
        if not re.match(patron_curp, curp):
            return False, "La CURP debe contener exactamente 18 caracteres alfanuméricos."
        return True, ""

    @staticmethod
    def validar_correo(correo: str) -> tuple[bool, str]:
        patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron_correo, correo):
            return False, "El correo electrónico no cumple con el formato estándar."
        return True, ""

    @staticmethod
    def validar_telefono(telefono: str) -> tuple[bool, str]:
        if not telefono.isdigit():
            return False, "El teléfono debe contener únicamente dígitos."
        if len(telefono) != 10:  # Asumiendo estándar nacional de 10 dígitos [cite: 352]
            return False, "El teléfono debe tener una longitud válida (10 dígitos)."
        return True, ""


    @staticmethod
    def validar_nombre_completo(nombre: str) -> tuple[bool, str]:
        """
        Valida que el nombre contenga al menos 5 caracteres y solo incluya letras, 
        espacios y caracteres del español (acentos, diéresis, ñ).
        Es un atributo estructural que no podrá modificarse una vez registrado.
        """
        if not nombre or len(nombre.strip()) < 5:
            return False, "El nombre completo debe tener al menos 5 caracteres."
        
        # Expresión regular que permite letras mayúsculas, minúsculas, acentos, ñ, ü y espacios
        patron_nombre = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$'
        if not re.match(patron_nombre, nombre.strip()):
            return False, "El nombre solo debe contener letras y espacios (sin números ni símbolos especiales)."
        
        return True, ""

    @staticmethod
    def validar_direccion(direccion: str) -> tuple[bool, str]:
        """
        Valida que la dirección no esté vacía y tenga una longitud mínima para evitar campos basura.
        Este dato podrá actualizarse en caso de cambios en la información de contacto.
        """
        if not direccion or len(direccion.strip()) < 10:
            return False, "La dirección debe contener al menos 10 caracteres válidos."
        
        return True, ""

    @staticmethod
    def validar_estado_licencia(estado: str) -> tuple[bool, str]:
        """
        Valida que el estado de la licencia de conducir se restrinja a valores predefinidos[cite: 302, 373].
        """
        if estado not in cat.ESTADOS_LICENCIA:
            return False, "El estado de la licencia seleccionado no es válido."
        
        return True, ""

    @staticmethod
    def validar_estado_propietario(estado: str) -> tuple[bool, str]:
        """
        Valida que el estado del propietario cambie estrictamente según su situación administrativa.
        """
        if estado not in cat.ESTADOS_PROPIETARIO:
            return False, "El estado del propietario seleccionado no es válido."
        
        return True, ""

    # =========================
    # VALIDACIONES DE INFRACCIONES
    # =========================

    @staticmethod
    def validar_monto(monto: float) -> tuple[bool, str]:
        if not isinstance(monto, (int, float)):
            return False, "El monto de la infracción debe ser numérico."
        if monto <= 0:
            return False, "El monto de la infracción debe ser mayor a cero."
        return True, ""

    @staticmethod
    def validar_tipo_infraccion(tipo: str) -> tuple[bool, str]:
        if tipo not in cat.TIPOS_INFRACCION:
            return False, "El tipo de infracción seleccionado no es válido."
        return True, ""
    