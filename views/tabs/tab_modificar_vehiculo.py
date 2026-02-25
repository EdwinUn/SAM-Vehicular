from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QFormLayout, QMessageBox, QDialog)
from PySide6.QtCore import Qt

# Importaciones del backend
import logic.catalogos as cat
from logic.gestor_vehiculos import GestorVehiculos

# [REFACTORIZACIÓN]: Nombramos la clase específicamente para su función.
# Hereda de QWidget, lo que la convierte en una pestaña autosuficiente.
class TabModificarVehiculo(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()
        self.aplicar_permisos()
        
    def configurar_ui(self):
        # [REFACTORIZACIÓN]: El layout base se aplica a 'self' (esta pestaña), 
        # eliminando la referencia a 'self.tab_modificar' que existía en el panel general.
        layout = QVBoxLayout(self)
        
        # ==========================================
        # 1. ZONA DE BÚSQUEDA
        # ==========================================
        layout_busqueda = QHBoxLayout()
        self.input_buscar_vin = QLineEdit()
        self.input_buscar_vin.setPlaceholderText("Ingrese el VIN a buscar...")
        
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.procesar_busqueda_vehiculo)

        layout_busqueda.addWidget(QLabel("VIN del Vehículo:"))
        layout_busqueda.addWidget(self.input_buscar_vin)
        layout_busqueda.addWidget(btn_buscar)
        
        layout.addLayout(layout_busqueda)

        # ==========================================
        # 2. FORMULARIO DE MODIFICACIÓN (Lectura y Escritura)
        # ==========================================
        formulario = QFormLayout()
        
        # --- CAMPOS DE SOLO LECTURA ---
        self.mod_marca = QLineEdit()
        self.mod_marca.setReadOnly(True)

        self.mod_modelo = QLineEdit()
        self.mod_modelo.setReadOnly(True)

        self.mod_anio = QLineEdit()
        self.mod_anio.setReadOnly(True)

        self.mod_clase = QLineEdit()
        self.mod_clase.setReadOnly(True)

        # --- CAMPO PROPIETARIO (Lectura + Botón) ---
        self.mod_id_propietario = QLineEdit()
        self.mod_id_propietario.setReadOnly(True)
        
        self.btn_cambiar_propietario = QPushButton("Cambio de Propietario")
        self.btn_cambiar_propietario.setStyleSheet("background-color: #9b59b6; color: white; font-weight: bold;")
        self.btn_cambiar_propietario.clicked.connect(self.abrir_ventana_cambio_propietario)
        
        
        layout_propietario = QHBoxLayout()
        layout_propietario.addWidget(self.mod_id_propietario)
        layout_propietario.addWidget(self.btn_cambiar_propietario)

        # --- CAMPO PLACAS (Lectura + Botón) ---
        self.mod_placa = QLineEdit()
        self.mod_placa.setReadOnly(True)
        
        self.btn_cambiar_placa = QPushButton("Realizar Reemplacamiento")
        self.btn_cambiar_placa.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        self.btn_cambiar_placa.clicked.connect(self.abrir_ventana_reemplacamiento)

        layout_placa = QHBoxLayout()
        layout_placa.addWidget(self.mod_placa)
        layout_placa.addWidget(self.btn_cambiar_placa)

        # --- CAMPOS EDITABLES ---
        self.mod_color = QComboBox()
        self.mod_color.addItems(cat.COLORES_VEHICULO)
        self.mod_color.setPlaceholderText("Seleccione un color...") # Texto fantasma
        self.mod_color.addItems(cat.COLORES_VEHICULO)
        self.mod_color.setCurrentIndex(-1) # Forzamos a que empiece en blanco
        
        self.mod_estado = QComboBox()
        self.mod_estado.addItems(cat.ESTADOS_VEHICULO) 
        self.mod_estado.setPlaceholderText("Seleccione un estado...")
        self.mod_estado.addItems(cat.ESTADOS_VEHICULO) 
        self.mod_estado.setCurrentIndex(-1) # Forzamos a que empiece en blanco

        # --- ENSAMBLAJE DEL FORMULARIO ---
        formulario.addRow("Marca:", self.mod_marca)
        formulario.addRow("Modelo:", self.mod_modelo)
        formulario.addRow("Clase:", self.mod_clase)
        formulario.addRow("Año:", self.mod_anio)
        formulario.addRow("ID Propietario:", layout_propietario)
        
        formulario.addRow("Placa Actual:", layout_placa)
        formulario.addRow("Nuevo Color:", self.mod_color)
        formulario.addRow("Estado Legal:", self.mod_estado)
        
        layout.addLayout(formulario)

        # ==========================================
        # 3. BOTÓN DE ACTUALIZACIÓN
        # ==========================================
        self.btn_actualizar = QPushButton("Actualizar Datos")
        self.btn_actualizar.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 10px;")
        
        self.btn_actualizar.clicked.connect(self.procesar_actualizacion)
        
        layout.addStretch() 
        layout.addWidget(self.btn_actualizar, alignment=Qt.AlignRight)

    # ==========================================
    # MÉTODOS DE VENTANAS EMERGENTES (Trámites)
    # ==========================================
    def abrir_ventana_reemplacamiento(self):
        """Abre una ventana modal (pop-up) para el trámite de cambio de placas."""
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Trámite de Reemplacamiento")
        dialogo.setFixedSize(450, 200) 
        
        layout = QVBoxLayout(dialogo)
        
        mensaje = QLabel("🚧 Módulo de Reemplacamiento en Desarrollo 🚧")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setStyleSheet("font-size: 18px; color: #e67e22; font-weight: bold;")
        
        sub_mensaje = QLabel("Próximamente:\nHistorial de placas, pagos de derechos\ny asignación de nuevos metales.")
        sub_mensaje.setAlignment(Qt.AlignCenter)
        sub_mensaje.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        
        btn_cerrar = QPushButton("Entendido")
        btn_cerrar.clicked.connect(dialogo.accept) 
        
        layout.addStretch()
        layout.addWidget(mensaje)
        layout.addWidget(sub_mensaje)
        layout.addStretch()
        layout.addWidget(btn_cerrar, alignment=Qt.AlignCenter)
        
        dialogo.exec()
    
    def abrir_ventana_cambio_propietario(self):
        """Abre una ventana modal para el trámite de cambio de propietario (compra-venta)."""
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Trámite de Cambio de Propietario")
        dialogo.setFixedSize(450, 200) 
        
        layout = QVBoxLayout(dialogo)
        
        mensaje = QLabel("🚧 Módulo de Cambio de Propietario en Desarrollo 🚧")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setStyleSheet("font-size: 18px; color: #8e44ad; font-weight: bold;")
        
        sub_mensaje = QLabel("Próximamente:\nHistorial de compra-venta, validación de no adeudos\ny transferencia de responsabilidades legales.")
        sub_mensaje.setAlignment(Qt.AlignCenter)
        sub_mensaje.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        
        btn_cerrar = QPushButton("Entendido")
        btn_cerrar.clicked.connect(dialogo.accept) 
        
        layout.addStretch()
        layout.addWidget(mensaje)
        layout.addWidget(sub_mensaje)
        layout.addStretch()
        layout.addWidget(btn_cerrar, alignment=Qt.AlignCenter)
        
        dialogo.exec()

    # ==========================================
    # MÉTODOS LÓGICOS (Búsqueda)
    # ==========================================
    def procesar_busqueda_vehiculo(self):
        """Busca el vehículo en la BD y rellena el formulario de modificación."""
        vin_buscado = self.input_buscar_vin.text().strip().upper()
        
        if not vin_buscado:
            QMessageBox.warning(self, "Atención", "Por favor, ingrese un VIN para buscar.")
            return
            
        exito, resultado = GestorVehiculos.buscar_vehiculo_por_vin(vin_buscado)
        
        if exito:
            self.mod_placa.setText(resultado["placa"])
            self.mod_marca.setText(resultado["marca"])
            self.mod_modelo.setText(resultado["modelo"])
            self.mod_anio.setText(str(resultado["anio"]))
            self.mod_clase.setText(resultado["clase"])
            self.mod_id_propietario.setText(str(resultado["id_propietario"]))
            
            self.mod_color.setCurrentText(resultado["color"])
            self.mod_estado.setCurrentText(resultado["estado_legal"])
            
            QMessageBox.information(self, "Vehículo Encontrado", "Datos cargados correctamente. Modifique lo necesario.")
        else:
            self.limpiar_formulario_modificar()
            QMessageBox.critical(self, "No encontrado", resultado)

    def limpiar_formulario_modificar(self):
        """Vacía las cajas de texto por si se busca un auto que no existe."""
        self.mod_placa.clear()
        self.mod_marca.clear()
        self.mod_modelo.clear()
        self.mod_anio.clear()
        self.mod_clase.clear()
        self.mod_id_propietario.clear()
        
        self.mod_color.setCurrentIndex(-1)
        self.mod_estado.setCurrentIndex(-1)
        
    def procesar_actualizacion(self):
        """Captura los datos permitidos y los envía al backend para actualizar."""
        
        # 1. Frontend Defensivo: Verificamos que realmente haya un vehículo cargado en pantalla
        # Si la caja de la placa está vacía, es porque no han buscado nada aún
        if not self.mod_placa.text():
            QMessageBox.warning(self, "Acción Inválida", "Primero debe buscar y cargar un vehículo antes de actualizar.")
            return

        # 2. Extraemos el VIN original y los nuevos valores de los combos
        vin_objetivo = self.input_buscar_vin.text().strip().upper()
        nuevo_color = self.mod_color.currentText()
        nuevo_estado = self.mod_estado.currentText()
        
        # 3. Mandamos al Gestor a hacer el UPDATE
        exito, mensaje = GestorVehiculos.actualizar_vehiculo(vin_objetivo, nuevo_color, nuevo_estado)
        
        # 4. Retroalimentación visual
        if exito:
            QMessageBox.information(self, "Actualización Exitosa", mensaje)
            self.limpiar_formulario_modificar()
            self.input_buscar_vin.clear() # Limpiamos el buscador para dejar todo como nuevo
        else:
            QMessageBox.critical(self, "Error al Actualizar", mensaje)
            
    # ==========================================
    # SEGURIDAD Y PERMISOS (RBAC)
    # ==========================================
    def aplicar_permisos(self):
        """Bloquea o esconde elementos visuales según el rol del usuario."""
        rol = self.usuario_actual.rol
        
        # Si es Agente de Tránsito [2] o Supervisor [3]
        if rol in [cat.ROLES_USUARIO[2], cat.ROLES_USUARIO[3]]:
            # 1. Escondemos por completo los botones de acción
            self.btn_actualizar.setVisible(False)
            self.btn_cambiar_propietario.setVisible(False)
            self.btn_cambiar_placa.setVisible(False)
            
            # 2. Bloqueamos los menús desplegables
            self.mod_color.setEnabled(False)
            self.mod_estado.setEnabled(False)