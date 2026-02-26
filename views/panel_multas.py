from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QDoubleSpinBox, QDateEdit, QTimeEdit, QMessageBox,
QTableWidget, QTableWidgetItem, QHeaderView, QFrame) # <-- Agregamos QTable y QFrame
from PySide6.QtCore import Qt, QDate, QTime
import logic.catalogos as cat

#Importaciones backend
from models.infraccion import Infraccion
from logic.gestor_infracciones import GestorInfracciones
from logic.gestor_agentes import GestorAgentes
from logic.gestor_vehiculos import GestorVehiculos

class PanelMultas(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()
        self.aplicar_permisos()

    def configurar_ui(self):
        """
        Configura la estructura principal del panel, dividiéndolo en pestañas
        para separar el registro de nuevas multas y el cobro/cancelación de las existentes.
        """
        layout_principal = QVBoxLayout(self)
        
        lbl_titulo = QLabel("Módulo de Infracciones de Tránsito")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(lbl_titulo)

        self.pestanas = QTabWidget()
        
        self.tab_registrar = QWidget()
        self.tab_gestionar = QWidget()
        
        self.construir_tab_registrar()
        self.construir_tab_gestionar()

        # --- APLICACIÓN DE ROLES (RBAC) ---
        rol = self.usuario_actual.rol
        
        if rol == cat.ROLES_USUARIO[0]: # Administrador
            self.pestanas.addTab(self.tab_registrar, "Registrar Infracción")
            self.pestanas.addTab(self.tab_gestionar, "Cobro y Cancelación")
            
        elif rol == cat.ROLES_USUARIO[2]: # Agente de Tránsito
            self.pestanas.addTab(self.tab_registrar, "Registrar Infracción")
            
        elif rol == cat.ROLES_USUARIO[3]: # Supervisor
            self.pestanas.addTab(self.tab_gestionar, "Consultar Infracción")

        layout_principal.addWidget(self.pestanas)

    # ==========================================
    # PESTAÑA 1: REGISTRAR INFRACCIÓN
    # ==========================================
    def construir_tab_registrar(self):
        layout = QVBoxLayout(self.tab_registrar)
        formulario = QFormLayout()
        
        self.input_vin = QLineEdit()
        self.input_vin.setPlaceholderText("Ingrese VIN o Placa del infractor")
        
        self.combo_agentes = QComboBox()
        self.combo_agentes.addItem("Seleccione al agente que levantó la multa...", None)
        
        exito, lista_agentes = GestorAgentes.obtener_agentes_para_combo()
        if exito:
            for id_agente, placa, nombre in lista_agentes:
                self.combo_agentes.addItem(f"{placa} - {nombre}", id_agente)
                
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())
        
        self.input_hora = QTimeEdit()
        self.input_hora.setTime(QTime.currentTime())

        self.input_lugar = QLineEdit()
        
        self.input_motivo = QLineEdit()
        self.input_motivo.setReadOnly(True) 
        self.input_motivo.setStyleSheet("background-color: #2c3e50; color: #bdc3c7; font-weight: bold;") 
        
        self.combo_tipo = QComboBox()
        for clave, datos in cat.TABULADOR_INFRACCIONES.items():
            self.combo_tipo.addItem(datos["descripcion"], clave)

        self.lbl_rango_monto = QLabel("Rango permitido: $0.00 - $0.00")
        self.lbl_rango_monto.setStyleSheet("color: #e67e22; font-style: italic; font-weight: bold;")

        self.input_monto = QDoubleSpinBox()
        self.input_monto.setRange(1.0, 999999.99)
        self.input_monto.setPrefix("$ ")
        self.input_monto.setDecimals(2)

        self.combo_captura = QComboBox()
        self.combo_captura.addItems(cat.TIPOS_CAPTURA_INFRACCION)
        
        self.input_licencia = QLineEdit()
        self.input_licencia.setPlaceholderText("Opcional (Obligatorio en sitio)")

        formulario.addRow("VIN Infractor:", self.input_vin)
        formulario.addRow("Agente de Tránsito:", self.combo_agentes)
        formulario.addRow("Fecha del hecho:", self.input_fecha)
        formulario.addRow("Hora del hecho:", self.input_hora)
        formulario.addRow("Lugar:", self.input_lugar)
        formulario.addRow("Tipo de Infracción:", self.combo_tipo)
        formulario.addRow("", self.lbl_rango_monto) 
        formulario.addRow("Motivo:", self.input_motivo)
        formulario.addRow("Monto de la multa:", self.input_monto)
        formulario.addRow("Método de Captura:", self.combo_captura)
        formulario.addRow("Licencia Conductor:", self.input_licencia)

        layout.addLayout(formulario)

        self.btn_registrar = QPushButton("Emitir Infracción")
        self.btn_registrar.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold; padding: 10px;")
        self.btn_registrar.clicked.connect(self.procesar_registro)
        
        layout.addWidget(self.btn_registrar, alignment=Qt.AlignRight)

        self.combo_tipo.currentIndexChanged.connect(self.actualizar_info_multa)
        self.actualizar_info_multa() 

    def actualizar_info_multa(self):
        clave_seleccionada = self.combo_tipo.currentData()
        
        if clave_seleccionada in cat.TABULADOR_INFRACCIONES:
            datos = cat.TABULADOR_INFRACCIONES[clave_seleccionada]
            
            minimo = datos["multa"]["min"]
            maximo = datos["multa"]["max"]
            self.lbl_rango_monto.setText(f"Rango permitido: ${minimo:,.2f} - ${maximo:,.2f} MXN")
            
            motivo_legal = f"{datos['articulo']} - {datos['descripcion']}"
            self.input_motivo.setText(motivo_legal)
            
            self.input_monto.setValue(minimo)

    # ==========================================
    # PESTAÑA 2: GESTIONAR ESTADO (COBROS)
    # ==========================================
    def construir_tab_gestionar(self):
        layout = QVBoxLayout(self.tab_gestionar)
        
        # 1. ZONA DE BÚSQUEDA POR PLACA
        lbl_ayuda = QLabel("🔍 ¿No conoce el folio? Busque las multas del vehículo:")
        lbl_ayuda.setStyleSheet("font-weight: bold; color: #a6adc8; margin-top: 10px;")
        layout.addWidget(lbl_ayuda)

        layout_busqueda_placa = QHBoxLayout()
        self.input_buscar_placa = QLineEdit()
        self.input_buscar_placa.setPlaceholderText("Ingrese Placa o VIN del vehículo...")
        
        btn_buscar_placa = QPushButton("Buscar Multas")
        btn_buscar_placa.setStyleSheet("background-color: #45475a; color: white;")
        btn_buscar_placa.clicked.connect(self.buscar_multas_por_placa)
        
        layout_busqueda_placa.addWidget(self.input_buscar_placa)
        layout_busqueda_placa.addWidget(btn_buscar_placa)
        layout.addLayout(layout_busqueda_placa)

        # TABLA DE RESULTADOS
        self.tabla_multas = QTableWidget()
        self.tabla_multas.setColumnCount(5)
        self.tabla_multas.setHorizontalHeaderLabels(["Folio", "Fecha", "Infracción", "Monto", "Estado"])
        self.tabla_multas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_multas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_multas.setEditTriggers(QTableWidget.NoEditTriggers) 
        self.tabla_multas.setMaximumHeight(150) 
        
        # EVENTO CLAVE: Autocompletar el folio al hacer clic
        self.tabla_multas.itemClicked.connect(self.seleccionar_folio_de_tabla)
        layout.addWidget(self.tabla_multas)
        
        # LÍNEA SEPARADORA
        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setStyleSheet("background-color: #45475a; margin: 15px 0px;")
        layout.addWidget(linea)

        # 2. ZONA DE ACCIÓN: CAMBIAR ESTADO
        layout_busqueda = QHBoxLayout()
        self.input_buscar_folio = QLineEdit()
        self.input_buscar_folio.setPlaceholderText("Ej: INF-20260223-A1B2C3")
        self.input_buscar_folio.setStyleSheet("font-weight: bold; color: #f9e2af;") 
        
        layout_busqueda.addWidget(QLabel("Folio a Pagar/Cancelar:"))
        layout_busqueda.addWidget(self.input_buscar_folio)
        layout.addLayout(layout_busqueda)

        formulario = QFormLayout()
        self.combo_nuevo_estado = QComboBox()
        self.combo_nuevo_estado.addItems(["Pagada", "Cancelada"]) 

        formulario.addRow("Cambiar estado a:", self.combo_nuevo_estado)
        layout.addLayout(formulario)

        self.btn_actualizar_estado = QPushButton("Aplicar Cambio de Estado")
        self.btn_actualizar_estado.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; padding: 10px;")
        self.btn_actualizar_estado.clicked.connect(self.procesar_cambio_estado)
        
        layout.addStretch() 
        layout.addWidget(self.btn_actualizar_estado, alignment=Qt.AlignRight)
        
    def aplicar_permisos(self):
        rol = self.usuario_actual.rol
        if rol == cat.ROLES_USUARIO[3]: 
            self.btn_actualizar_estado.setVisible(False)
            self.combo_nuevo_estado.setEnabled(False)
            
    # ==========================================
    # LÓGICA DE INTERFAZ Y BACKEND
    # ==========================================
    def procesar_registro(self):
        criterio_vehiculo = self.input_vin.text().strip().upper()
        lugar = self.input_lugar.text().strip().upper()
        motivo = self.input_motivo.text().strip().upper()
        tipo_texto = self.combo_tipo.currentText() 
        clave_infraccion = self.combo_tipo.currentData() 
        tipo_captura = self.combo_captura.currentText()
        monto = self.input_monto.value()
        licencia = self.input_licencia.text().strip().upper()
        fecha = self.input_fecha.date().toString("yyyy-MM-dd")
        hora = self.input_hora.time().toString("HH:mm")
        id_agente = self.combo_agentes.currentData()

        if not criterio_vehiculo or not lugar or not motivo:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor llene todos los campos obligatorios.")
            return

        if len(lugar) < 5: 
            QMessageBox.warning(self, "Detalles Insuficientes", "El 'Lugar' debe ser más descriptivo (mínimo 5 caracteres).")
            return
            
        if not id_agente:
            QMessageBox.warning(self, "Agente no seleccionado", "Por favor, seleccione al Agente de Tránsito que levantó la boleta.")
            return

        exito_vehiculo, datos_vehiculo = GestorVehiculos.buscar_vehiculo_universal(criterio_vehiculo)
        
        if not exito_vehiculo:
            QMessageBox.warning(self, "Vehículo No Encontrado", "No existe ningún vehículo registrado con esa Placa o VIN.")
            return
            
        vin_real = datos_vehiculo["vin"] 

        if clave_infraccion in cat.TABULADOR_INFRACCIONES:
            datos_oficiales = cat.TABULADOR_INFRACCIONES[clave_infraccion]
            min_permitido = datos_oficiales["multa"]["min"]
            max_permitido = datos_oficiales["multa"]["max"]
            
            if monto < min_permitido or monto > max_permitido:
                QMessageBox.critical(self, "Monto Ilegal", 
                    f"El monto de ${monto:,.2f} está fuera de la ley.\n"
                    f"Para esta infracción el reglamento exige cobrar entre ${min_permitido:,.2f} y ${max_permitido:,.2f}."
                )
                return

        nueva_infraccion = Infraccion(
            vin_infractor=vin_real, id_agente=id_agente, fecha=fecha, hora=hora,
            lugar=lugar, tipo_infraccion=tipo_texto, motivo=motivo,
            monto=monto, licencia_conductor=licencia
        )

        exito, msj = GestorInfracciones.registrar_infraccion(nueva_infraccion, tipo_captura)

        if exito:
            QMessageBox.information(self, "Éxito", msj)
            self.limpiar_formulario_registro()
        else:
            QMessageBox.critical(self, "Error al Registrar", msj)

    def buscar_multas_por_placa(self):
        """Busca las multas en SQLite y las dibuja en la tabla."""
        criterio = self.input_buscar_placa.text().strip().upper()
        if not criterio:
            QMessageBox.warning(self, "Atención", "Ingrese una placa o VIN para buscar.")
            return
            
        exito, lista_multas = GestorInfracciones.obtener_infracciones_por_vehiculo(criterio)
        
        self.tabla_multas.setRowCount(0) 
        
        if exito and lista_multas:
            for fila, multa in enumerate(lista_multas):
                self.tabla_multas.insertRow(fila)
                self.tabla_multas.setItem(fila, 0, QTableWidgetItem(multa[0]))
                self.tabla_multas.setItem(fila, 1, QTableWidgetItem(multa[1]))
                self.tabla_multas.setItem(fila, 2, QTableWidgetItem(multa[2]))
                self.tabla_multas.setItem(fila, 3, QTableWidgetItem(f"${multa[3]:,.2f}"))
                
                item_estado = QTableWidgetItem(multa[4])
                if multa[4] == "Pendiente":
                    item_estado.setForeground(Qt.yellow)
                elif multa[4] == "Pagada":
                    item_estado.setForeground(Qt.green)
                else: 
                    item_estado.setForeground(Qt.red)
                    
                self.tabla_multas.setItem(fila, 4, item_estado)
        else:
            QMessageBox.information(self, "Resultado", "No se encontraron multas para este vehículo.")

    def seleccionar_folio_de_tabla(self, item):
        """Copia el folio de la fila seleccionada a la caja de texto."""
        fila_seleccionada = item.row()
        folio = self.tabla_multas.item(fila_seleccionada, 0).text()
        self.input_buscar_folio.setText(folio)

    def procesar_cambio_estado(self):
        folio = self.input_buscar_folio.text().strip().upper()
        nuevo_estado = self.combo_nuevo_estado.currentText()
        
        if not folio:
            QMessageBox.warning(self, "Falta Folio", "Por favor ingrese el folio de la infracción.")
            return
            
        exito, msj = GestorInfracciones.cambiar_estado_infraccion(folio, nuevo_estado)
        
        if exito:
            QMessageBox.information(self, "Actualización Exitosa", msj)
            self.input_buscar_folio.clear()
            # Si buscamos previamente, recargamos la tabla para ver el nuevo estado
            if self.input_buscar_placa.text():
                self.buscar_multas_por_placa()
        else:
            QMessageBox.critical(self, "Error", msj)
            
    def limpiar_formulario_registro(self):
        self.input_vin.clear()
        self.input_lugar.clear()
        self.input_licencia.clear()
        
        self.combo_tipo.setCurrentIndex(0)
        self.combo_captura.setCurrentIndex(0)
        self.combo_agentes.setCurrentIndex(0)