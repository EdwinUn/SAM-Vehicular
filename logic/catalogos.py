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
    "Autobús"
]

PROCEDENCIAS_VEHICULO = [
    "Nacional",
    "Importado"
]

# =========================
# MARCAS Y MODELOS (Estructura Jerárquica)
# =========================
# Diccionario donde la clave es la Marca y el valor es una lista de Modelos permitidos.
# Esto asegura que no haya entrada libre en estos campos y facilita los menús dinámicos.
#PENDIENTE A MEJORAR Y AGREGAR MÁS MODELOS Y MARCAS REALES
MARCAS_MODELOS_VEHICULO = {
    "Nissan": ["Versa", "Sentra", "March", "Tsuru", "Altima", "Kicks", "Frontier", "NP300"],
    "Chevrolet": ["Aveo", "Chevy", "Beat", "Spark", "Onix", "Trax", "Silverado", "Colorado"],
    "Volkswagen": ["Jetta", "Vento", "Gol", "Polo", "Virtus", "Tiguan", "Saveiro", "Taos"],
    "Toyota": ["Corolla", "Yaris", "Camry", "Prius", "RAV4", "Hilux", "Tacoma", "Avanza"],
    "Honda": ["Civic", "City", "Accord", "CR-V", "HR-V", "BR-V"],
    "Ford": ["Figo", "Fiesta", "Focus", "Mustang", "Escape", "Ranger", "F-150", "Explorer"],
    "Mazda": ["Mazda 2", "Mazda 3", "Mazda 6", "CX-3", "CX-5", "CX-30"],
    "Kia": ["Rio", "Forte", "Soul", "Seltos", "Sportage", "Sorento"],
    "Hyundai": ["Grand i10", "Accent", "Elantra", "Tucson", "Creta"]
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