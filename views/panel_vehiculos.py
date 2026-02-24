from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QMessageBox, QSpinBox)
from PySide6.QtCore import Qt
import logic.catalogos as cat

class PanelVehiculos(QWidget):
    def __init__(self):
        super().__init__()
        self.configurar_ui()

    def configurar_ui(self):
        # Layout principal del panel
        layout_principal = QVBoxLayout(self)
        
        # Título del módulo
        lbl_titulo = QLabel("Módulo de Gestión de Vehículos")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(lbl_titulo)

        # ==========================================
        # CREACIÓN DE PESTAÑAS (QTabWidget)
        # ==========================================
        self.pestanas = QTabWidget()
        
        self.tab_registrar = QWidget()
        self.tab_modificar = QWidget()
        
        self.pestanas.addTab(self.tab_registrar, "Registrar Nuevo Vehículo")
        self.pestanas.addTab(self.tab_modificar, "Modificar Vehículo")
        
        layout_principal.addWidget(self.pestanas)

        # Construir el contenido de cada pestaña
        self.construir_tab_registrar()
        self.construir_tab_modificar()

    # ==========================================
    # PESTAÑA 1: REGISTRAR VEHÍCULO
    # ==========================================
    def construir_tab_registrar(self):
        """Construye el formulario garantizando la integridad de los datos mediante catálogos cerrados."""
        layout = QVBoxLayout(self.tab_registrar)
        formulario = QFormLayout()
        
        # 1. Entradas de texto restringidas
        self.input_vin = QLineEdit()
        self.input_vin.setMaxLength(17) # Frontend Defensivo: Evita que escriban de más
        self.input_vin.setPlaceholderText("Ej: 3G1SE516X3S205891")
        self.input_placa = QLineEdit()
        self.input_placa.setPlaceholderText("Ej: YYU-021-A")
        self.input_id_propietario = QLineEdit()
        self.input_id_propietario.setPlaceholderText("ID numérico del propietario")
        
        self.input_anio = QSpinBox()
        self.input_anio.setRange(1900, 2030)
        self.input_anio.setValue(2024)
        self.input_anio.setButtonSymbols(QSpinBox.PlusMinus)
        # 2. Listas Desplegables (QComboBox) conectadas a catalogos.py
        self.combo_marca = QComboBox()
        # Llenamos la marca con las "llaves" de tu diccionario (Nissan, Chevrolet, etc.)
        self.combo_marca.addItems(cat.MARCAS_MODELOS_VEHICULO.keys())
        
        self.combo_modelo = QComboBox()
        # Nota: No lo llenamos aquí, lo llenará la función dinámica más abajo.
        
        self.combo_color = QComboBox()
        self.combo_color.addItems(cat.COLORES_VEHICULO)
        
        self.combo_clase = QComboBox()
        self.combo_clase.addItems(cat.CLASES_VEHICULO)
        
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(cat.ESTADOS_VEHICULO)

        self.combo_procedencia = QComboBox()
        self.combo_procedencia.addItems(cat.PROCEDENCIAS_VEHICULO)

        # 3. CONEXIÓN DINÁMICA (Menú en Cascada)
        # Cuando el usuario cambie la marca, se ejecuta self.actualizar_modelos
        self.combo_marca.currentTextChanged.connect(self.actualizar_modelos)
        
        # Forzamos una primera actualización manual para que el modelo no empiece vacío al abrir el programa
        self.actualizar_modelos(self.combo_marca.currentText())

        # 4. Ensamblaje del Formulario
        formulario.addRow("VIN (17 caracteres):", self.input_vin)
        formulario.addRow("Placa:", self.input_placa)
        formulario.addRow("Marca:", self.combo_marca)
        formulario.addRow("Modelo:", self.combo_modelo)
        formulario.addRow("Año:", self.input_anio)
        formulario.addRow("Color:", self.combo_color)
        formulario.addRow("Clase:", self.combo_clase)
        formulario.addRow("Estado Legal:", self.combo_estado)
        formulario.addRow("Procedencia:", self.combo_procedencia)
        formulario.addRow("ID Propietario:", self.input_id_propietario)

        layout.addLayout(formulario)

        # Botón de Guardado
        self.btn_guardar = QPushButton("Guardar Vehículo")
        self.btn_guardar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;")
        layout.addWidget(self.btn_guardar, alignment=Qt.AlignRight)

    # ==========================================
    # MÉTODO AUXILIAR PARA LA INTERFAZ
    # ==========================================
    def actualizar_modelos(self, marca_seleccionada):
        """
        Slot que se dispara al cambiar la marca. 
        Limpia el QComboBox de modelos y lo rellena con la lista correspondiente.
        """
        self.combo_modelo.clear() # Borra los modelos de la marca anterior
        
        # Busca la marca en el diccionario y agrega su lista de modelos
        if marca_seleccionada in cat.MARCAS_MODELOS_VEHICULO:
            modelos_permitidos = cat.MARCAS_MODELOS_VEHICULO[marca_seleccionada]
            self.combo_modelo.addItems(modelos_permitidos)
    # ==========================================
    # PESTAÑA 2: MODIFICAR VEHÍCULO
    # ==========================================
    def construir_tab_modificar(self):
        layout = QVBoxLayout(self.tab_modificar)
        
        # Zona de búsqueda
        layout_busqueda = QHBoxLayout()
        self.input_buscar_vin = QLineEdit()
        self.input_buscar_vin.setPlaceholderText("Ingrese el VIN a buscar...")
        btn_buscar = QPushButton("Buscar")
        
        layout_busqueda.addWidget(QLabel("VIN del Vehículo:"))
        layout_busqueda.addWidget(self.input_buscar_vin)
        layout_busqueda.addWidget(btn_buscar)
        
        layout.addLayout(layout_busqueda)

        # Formulario de modificación (Solo los campos permitidos según tus reglas)
        formulario = QFormLayout()
        
        self.mod_placa = QLineEdit()
        self.mod_color = QComboBox()
        self.mod_color.addItems(cat.COLORES_VEHICULO)
        
        self.mod_estado = QComboBox()
        self.mod_estado.addItems(["Activo", "Inactivo", "Robado"]) # Debería venir de catálogos

        formulario.addRow("Nueva Placa:", self.mod_placa)
        formulario.addRow("Nuevo Color:", self.mod_color)
        formulario.addRow("Estado Legal:", self.mod_estado)
        
        layout.addLayout(formulario)

        # Botón de actualización
        self.btn_actualizar = QPushButton("Actualizar Datos")
        self.btn_actualizar.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 10px;")
        
        layout.addStretch() # Empuja el botón hacia abajo
        layout.addWidget(self.btn_actualizar, alignment=Qt.AlignRight)