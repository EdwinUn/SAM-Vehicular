from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QMessageBox, QSpinBox, QDialog)
from PySide6.QtCore import Qt

#Conexiones con el backend (logic)
import logic.catalogos as cat
from models.vehiculo import Vehiculo
from logic.gestor_vehiculos import GestorVehiculos

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
        self.combo_marca.addItems(cat.MARCAS_MODELOS_VEHICULO.keys())
        
        self.combo_modelo = QComboBox()
        
        self.combo_color = QComboBox()
        self.combo_color.addItems(cat.COLORES_VEHICULO)
        
        self.combo_clase = QComboBox()
        # Nota: Ya NO llenamos la clase aquí con cat.CLASES_VEHICULO. 
        # La clase se llenará sola dependiendo del modelo.
        
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(cat.ESTADOS_VEHICULO)

        self.combo_procedencia = QComboBox()
        self.combo_procedencia.addItems(cat.PROCEDENCIAS_VEHICULO)

        # 3. CONEXIÓN DINÁMICA (Cascada Doble)
        # Primera cascada: Al cambiar Marca -> Actualiza Modelos
        self.combo_marca.currentTextChanged.connect(self.actualizar_modelos)
        
        # Segunda cascada: Al cambiar Modelo -> Actualiza Clases
        self.combo_modelo.currentTextChanged.connect(self.actualizar_clases)
        
        # Forzamos la primera actualización para arrancar con datos
        self.actualizar_modelos(self.combo_marca.currentText())

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

        # Conexion con el backend
        self.btn_guardar.clicked.connect(self.procesar_registro)
        layout.addWidget(self.btn_guardar, alignment=Qt.AlignRight)
        
        
    # ==========================================
    # MÉTODOS AUXILIARES PARA LA INTERFAZ
    # ==========================================
    def actualizar_modelos(self, marca_seleccionada):
        """Primera cascada: Llena los modelos basados en la marca."""
        self.combo_modelo.clear() 
        
        if marca_seleccionada in cat.MARCAS_MODELOS_VEHICULO:
            # Ahora extraemos solo las llaves (los nombres de los modelos)
            modelos_permitidos = list(cat.MARCAS_MODELOS_VEHICULO[marca_seleccionada].keys())
            self.combo_modelo.addItems(modelos_permitidos)
    
    def actualizar_clases(self, modelo_seleccionado):
        """Segunda cascada: Llena las clases y bloquea el campo si solo hay una opción."""
        self.combo_clase.clear()
        
        marca_actual = self.combo_marca.currentText()
        
        # Verificamos que la marca y el modelo existan en el catálogo
        if marca_actual in cat.MARCAS_MODELOS_VEHICULO and modelo_seleccionado in cat.MARCAS_MODELOS_VEHICULO[marca_actual]:
            
            # Traemos la lista de clases permitidas (ej. ["Sedán", "Hatchback"] o solo ["Sedán"])
            clases_permitidas = cat.MARCAS_MODELOS_VEHICULO[marca_actual][modelo_seleccionado]
            self.combo_clase.addItems(clases_permitidas)
            
            # Frontend Defensivo: Si solo hay una clase, bloqueamos el menú para evitar errores
            if len(clases_permitidas) == 1:
                self.combo_clase.setEnabled(False) # Se pone gris y no se puede cambiar
            else:
                self.combo_clase.setEnabled(True)  # Se habilita para que el operador elija
    
    def procesar_registro(self):
        """Extraemos los datos de la interfaz, los empaqueta y los enviamos al backend."""
        
        # 1. Extraer datos (Usamos .strip() para quitar espacios accidentales)
        # Convertimos VIN y Placa a mayúsculas automáticamente como medida defensiva
        vin = self.input_vin.text().strip().upper()
        placa = self.input_placa.text().strip().upper()
        marca = self.combo_marca.currentText()
        modelo = self.combo_modelo.currentText()
        anio = self.input_anio.value()
        color = self.combo_color.currentText()
        clase = self.combo_clase.currentText()
        estado = self.combo_estado.currentText()
        procedencia = self.combo_procedencia.currentText()
        
        id_propietario_str = self.input_id_propietario.text().strip()

        # Validación visual rápida: Que no intenten guardar con campos vacíos críticos
        if not vin or not placa or not id_propietario_str:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor, llene el VIN, Placa y el ID del Propietario.")
            return

        # Convertir el ID a entero (Si el usuario escribió letras, lo atrapamos aquí)
        try:
            id_propietario = int(id_propietario_str)
        except ValueError:
            QMessageBox.warning(self, "Error de Formato", "El ID del propietario debe ser un número entero válido.")
            return

        # 2. Empaquetar en el Modelo
        nuevo_vehiculo = Vehiculo(
            vin=vin, 
            placa=placa, 
            marca=marca, 
            modelo=modelo, 
            anio=anio, 
            color=color, 
            clase=clase, 
            estado_legal=estado, 
            procedencia=procedencia, 
            id_propietario=id_propietario
        )

        # 3. Enviar al Backend
        # Aquí cruzamos los dedos. El Gestor validará todo e insertará en SQLite
        exito, mensaje = GestorVehiculos.registrar_vehiculo(nuevo_vehiculo)

        # 4. Dar Retroalimentación al Operador
        if exito:
            QMessageBox.information(self, "Registro Exitoso", mensaje)
            self.limpiar_formulario() # Limpiamos la pantalla para el siguiente auto
        else:
            # Si falló (ej. VIN repetido, modelo inválido), mostramos el mensaje exacto de tu validador
            QMessageBox.critical(self, "Error al Guardar", mensaje)

    def limpiar_formulario(self):
        """Limpia las cajas de texto después de un guardado exitoso."""
        self.input_vin.clear()
        self.input_placa.clear()
        self.input_id_propietario.clear()
        self.input_anio.setValue(2024) # Regresamos al valor por defecto
        self.combo_marca.setCurrentIndex(0) # Regresamos a la primera marca
    


    # ==========================================
    # PESTAÑA 2: MODIFICAR VEHÍCULO
    # ==========================================

    def construir_tab_modificar(self):
        layout = QVBoxLayout(self.tab_modificar)
        
        # Zona de búsqueda
        layout_busqueda = QHBoxLayout()
        self.input_buscar_vin = QLineEdit()

        #--BOTON BUSCAR Y CONEXION BACKEND---
        self.input_buscar_vin.setPlaceholderText("Ingrese el VIN a buscar...")
        
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.procesar_busqueda_vehiculo)


        layout_busqueda.addWidget(QLabel("VIN del Vehículo:"))
        layout_busqueda.addWidget(self.input_buscar_vin)
        layout_busqueda.addWidget(btn_buscar)
        
        layout.addLayout(layout_busqueda)

        # ==========================================
        # Formulario de modificación mixto (Lectura y Escritura)
        # ==========================================
        formulario = QFormLayout()
        
        # --- CAMPOS DE SOLO LECTURA  ---
        self.mod_marca = QLineEdit()
        self.mod_marca.setReadOnly(True)
        self.mod_marca.setStyleSheet("background-color: #e0e0e0; color: #555;") # Se pinta gris para indicar que está bloqueado
        
        self.mod_modelo = QLineEdit()
        self.mod_modelo.setReadOnly(True)
        self.mod_modelo.setStyleSheet("background-color: #e0e0e0; color: #555;")
        
        self.mod_anio = QLineEdit()
        self.mod_anio.setReadOnly(True)
        self.mod_anio.setStyleSheet("background-color: #e0e0e0; color: #555;")

        self.mod_clase = QLineEdit()
        self.mod_clase.setReadOnly(True)
        self.mod_clase.setStyleSheet("background-color: #e0e0e0; color: #555;")

        # --- CAMPOS DE PROPIETARIO (Lectura y boton de tramite  ---
        self.mod_id_propietario = QLineEdit()
        self.mod_id_propietario.setReadOnly(True)
        self.mod_id_propietario.setStyleSheet("background-color: #e0e0e0; color: #555;")
        self.btn_cambiar_propietario = QPushButton("Cambio de Propietario")
        self.btn_cambiar_propietario.setStyleSheet("background-color: #9b59b6; color: white; font-weight: bold;")

        self.btn_cambiar_propietario.clicked.connect(self.abrir_ventana_cambio_propietario)

            # Agrupamos la cajita y el botón
        layout_propietario = QHBoxLayout()
        layout_propietario.addWidget(self.mod_id_propietario)
        layout_propietario.addWidget(self.btn_cambiar_propietario)

            #---- CAMPOS DE PLACAS-----
        self.mod_placa = QLineEdit()
        self.mod_placa.setReadOnly(True)
        self.mod_placa.setStyleSheet("background-color: #e0e0e0; color: #555;")
        
        self.btn_cambiar_placa = QPushButton("Realizaar Reemplacamiento")
        self.btn_cambiar_placa.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")

        #Creacion de boton e ingreso de funcion para abrir pestana emergente
        self.btn_cambiar_placa.clicked.connect(self.abrir_ventana_reemplacamiento)

        #layout horizontal pequeño para juntar la cajita y el botón
        layout_placa = QHBoxLayout()
        layout_placa.addWidget(self.mod_placa)
        layout_placa.addWidget(self.btn_cambiar_placa)

        #agregamos el layout completo
        
            #----COLOR-----
        self.mod_color = QComboBox()
        self.mod_color.addItems(cat.COLORES_VEHICULO)
            #----ESTADO-----
        self.mod_estado = QComboBox()
        self.mod_estado.addItems(cat.ESTADOS_VEHICULO) 

        # --- ENSAMBLAJE DEL FORMULARIO ---
        # Primero mostramos lo que no se toca
        formulario.addRow("Marca:", self.mod_marca)
        formulario.addRow("Modelo:", self.mod_modelo)
        formulario.addRow("Clase:", self.mod_clase)
        formulario.addRow("Año:", self.mod_anio)
        formulario.addRow("ID Propietario:", layout_propietario)
        
        # Luego lo que sí pueden cambiare
        formulario.addRow("Placa Actual:", layout_placa)
        formulario.addRow("Nuevo Color:", self.mod_color)
        formulario.addRow("Estado Legal:", self.mod_estado)
        
        layout.addLayout(formulario)

        # Botón de actualización
        self.btn_actualizar = QPushButton("Actualizar Datos")
        self.btn_actualizar.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 10px;")
        
        layout.addStretch() # Empuja el botón hacia abajo
        layout.addWidget(self.btn_actualizar, alignment=Qt.AlignRight)


    def abrir_ventana_reemplacamiento(self):
        """Abre una ventana modal (pop-up) para el trámite de cambio de placas."""
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Trámite de Reemplacamiento")
        dialogo.setFixedSize(450, 200) # Una ventanita de buen tamaño
        
        layout = QVBoxLayout(dialogo)
        
        mensaje = QLabel("🚧 Módulo de Reemplacamiento en Desarrollo 🚧")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setStyleSheet("font-size: 18px; color: #e67e22; font-weight: bold;")
        
        sub_mensaje = QLabel("Próximamente:\nHistorial de placas, pagos de derechos\ny asignación de nuevos metales.")
        sub_mensaje.setAlignment(Qt.AlignCenter)
        sub_mensaje.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        
        btn_cerrar = QPushButton("Entendido")
        btn_cerrar.clicked.connect(dialogo.accept) # Cierra la ventanita
        
        layout.addStretch()
        layout.addWidget(mensaje)
        layout.addWidget(sub_mensaje)
        layout.addStretch()
        layout.addWidget(btn_cerrar, alignment=Qt.AlignCenter)
        
        # .exec() hace que la ventana sea "modal" (no puedes tocar lo de atrás hasta cerrarla)
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
        
        # Texto realista sobre lo que hará el backend en el futuro
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

    def procesar_busqueda_vehiculo(self):
        """Busca el vehículo en la BD y rellena el formulario de modificación."""
        vin_buscado = self.input_buscar_vin.text().strip().upper()
        
        if not vin_buscado:
            QMessageBox.warning(self, "Atención", "Por favor, ingrese un VIN para buscar.")
            return
            
        # Llamamos al backend (Asegúrate de tener importado GestorVehiculos arriba)
        exito, resultado = GestorVehiculos.buscar_vehiculo_por_vin(vin_buscado)
        
        if exito:
            # resultado es el diccionario que armamos en el Gestor
            # 1. Rellenamos los campos de solo lectura
            self.mod_placa.setText(resultado["placa"])
            self.mod_marca.setText(resultado["marca"])
            self.mod_modelo.setText(resultado["modelo"])
            self.mod_anio.setText(str(resultado["anio"]))
            self.mod_clase.setText(resultado["clase"])
            self.mod_id_propietario.setText(str(resultado["id_propietario"]))
            
            # 2. Ajustamos los menús desplegables editables a su valor actual
            self.mod_color.setCurrentText(resultado["color"])
            self.mod_estado.setCurrentText(resultado["estado_legal"])
            
            # Mensaje opcional para que el operador sepa que todo salió bien
            QMessageBox.information(self, "Vehículo Encontrado", "Datos cargados correctamente. Modifique lo necesario.")
        else:
            # Si no existe, vaciamos el formulario y mostramos el error
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
        # Regresamos los combos al primer elemento por defecto
        self.mod_color.setCurrentIndex(0)
        self.mod_estado.setCurrentIndex(0)