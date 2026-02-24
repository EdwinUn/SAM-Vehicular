"""
Catálogos oficiales del sistema.

Este módulo centraliza todos los valores predefinidos utilizados por el sistema
para garantizar consistencia entre la interfaz, la validación y la lógica de negocio.

NO contiene lógica.
NO realiza validaciones.
NO accede a base de datos.
"""

# =========================
# VEHÍCULOS
# =========================

ESTADOS_VEHICULO = [
    "Activo",
    "Baja temporal",
    "Reporte de robo",
    "Recuperado",
    "En corralón"
]

CLASES_VEHICULO = [
    "Sedán",
    "Motocicleta",
    "Camión",
    "Camioneta",
    "Autobús",
    "Hatchback"
]

PROCEDENCIAS_VEHICULO = [
    "Nacional",
    "Importado"
]

# =========================
# MARCAS, MODELOS Y SUS CLASES PERMITIDAS (Cascada Doble)
# =========================
# Diccionario donde la clave es la Marca y el valor es otro diccionario.
# Cada Modelo contiene una LISTA con las clases en las que se fabrica.

#TODO MEJORAR porque por ejemplo puedo poner un aveo hatchback que no existe realmente
MARCAS_MODELOS_VEHICULO = {
    "Nissan": {
        "Versa": ["Sedán"], "Sentra": ["Sedán"], "March": ["Hatchback"], 
        "Tsuru": ["Sedán"], "Altima": ["Sedán"], "Kicks": ["Camioneta"], 
        "Frontier": ["Camioneta"], "NP300": ["Camioneta"]
    },
    "Chevrolet": {
        "Aveo": ["Sedán", "Hatchback"], "Chevy": ["Sedán", "Hatchback"], 
        "Beat": ["Sedán", "Hatchback"], "Spark": ["Hatchback"], 
        "Onix": ["Sedán"], "Trax": ["Camioneta"], 
        "Silverado": ["Camioneta"], "Colorado": ["Camioneta"]
    },
    "Volkswagen": {
        "Jetta": ["Sedán"], "Vento": ["Sedán"], "Gol": ["Hatchback"], 
        "Polo": ["Hatchback"], "Virtus": ["Sedán"], "Tiguan": ["Camioneta"], 
        "Saveiro": ["Camioneta"], "Taos": ["Camioneta"]
    },
    "Toyota": {
        "Corolla": ["Sedán"], "Yaris": ["Sedán", "Hatchback"], "Camry": ["Sedán"], 
        "Prius": ["Sedán", "Hatchback"], "RAV4": ["Camioneta"], 
        "Hilux": ["Camioneta"], "Tacoma": ["Camioneta"], "Avanza": ["Camioneta"]
    },
    "Honda": {
        "Civic": ["Sedán", "Hatchback"], "City": ["Sedán", "Hatchback"], 
        "Accord": ["Sedán"], "CR-V": ["Camioneta"], 
        "HR-V": ["Camioneta"], "BR-V": ["Camioneta"]
    },
    "Ford": {
        "Figo": ["Sedán", "Hatchback"], "Fiesta": ["Sedán", "Hatchback"], 
        "Focus": ["Sedán", "Hatchback"], "Mustang": ["Sedán"], 
        "Escape": ["Camioneta"], "Ranger": ["Camioneta"], 
        "F-150": ["Camioneta"], "Explorer": ["Camioneta"]
    },
    "Mazda": {
        "Mazda 2": ["Sedán", "Hatchback"], "Mazda 3": ["Sedán", "Hatchback"], 
        "Mazda 6": ["Sedán"], "CX-3": ["Camioneta"], 
        "CX-5": ["Camioneta"], "CX-30": ["Camioneta"]
    },
    "Kia": {
        "Rio": ["Sedán", "Hatchback"], "Forte": ["Sedán", "Hatchback"], 
        "Soul": ["Camioneta"], "Seltos": ["Camioneta"], 
        "Sportage": ["Camioneta"], "Sorento": ["Camioneta"]
    },
    "Hyundai": {
        "Grand i10": ["Sedán", "Hatchback"], "Accent": ["Sedán", "Hatchback"], 
        "Elantra": ["Sedán"], "Tucson": ["Camioneta"], "Creta": ["Camioneta"]
    },
    "Yamaha": {
        "FZ25": ["Motocicleta"], "MT-07": ["Motocicleta"], 
        "R6": ["Motocicleta"], "Crypton": ["Motocicleta"]
    },
    "Mercedes-Benz": {
        "Sprinter": ["Camioneta"], "Clase C": ["Sedán"], 
        "Actros": ["Camión"], "Marcopolo": ["Autobús"]
    }
}
# =========================
# COLORES DE VEHÍCULO
# =========================
# Catálogo cerrado para evitar discrepancias ortográficas o descriptivas en la base de datos.
#PENDIENTE A MEJORAR
COLORES_VEHICULO = [
    "Blanco",
    "Negro",
    "Plata",
    "Gris",
    "Rojo",
    "Azul",
    "Verde",
    "Amarillo",
    "Naranja",
    "Café",
    "Beige",
    "Guinda",
    "Otro"
]

# Nota:
# Marca y modelo se consideran atributos estructurales,
# pero el documento indica que deben validarse contra valores válidos.
# En una versión real, esto vendría de una BD o catálogo externo.
# Aquí se deja abierto para crecimiento.
# =========================


# =========================
# PROPIETARIOS
# =========================

ESTADOS_LICENCIA = [
    "Vigente",
    "Suspendida",
    "Cancelada",
    "Vencida"
]

ESTADOS_PROPIETARIO = [
    "Activo",
    "Inactivo"
]

# =========================
# INFRACCIONES
# =========================

ESTADOS_INFRACCION = [
    "Pendiente",
    "Pagada",
    "Cancelada"
]

TIPOS_INFRACCION = [
    "Exceso de velocidad",
    "Estacionamiento prohibido",
    "No portar cinturón",
    "Uso de celular",
    "Conducir en estado de ebriedad",
    "Falta de documentos",
    "Otro"
]

TIPOS_CAPTURA_INFRACCION = [
    "En sitio",
    "Fotomulta"
]

# =========================
# AGENTES DE TRÁNSITO
# =========================

ESTADOS_AGENTE = [
    "Activo",
    "Inactivo"
]

# =========================
# USUARIOS DEL SISTEMA
# =========================

ROLES_USUARIO = [
    "Administrador",
    "Operador Administrativo",
    "Agente de Tránsito",
    "Supervisor"
]