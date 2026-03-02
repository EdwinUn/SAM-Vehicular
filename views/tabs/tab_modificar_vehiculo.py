from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QFormLayout, QMessageBox, QInputDialog)
from PySide6.QtCore import Qt

# Importaciones del backend
import logic.catalogos as cat
from logic.gestor_vehiculos import GestorVehiculos
from logic.gestor_propietarios import GestorPropietarios
from logic.validador import Validador

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
        # Cambia el placeholder para que el operador sepa que puede usar la placa
        self.input_buscar_vin.setPlaceholderText("Ingrese VIN o Placa a buscar...")
        
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
        self.mod_color.addItems(cat.COLORES_VEHICULO)
        self.mod_color.setCurrentIndex(-1) # Forzamos a que empiece en blanco
        
        self.mod_estado = QComboBox()
        self.mod_estado.addItems(cat.ESTADOS_VEHICULO) 
        self.mod_estado.addItems(cat.ESTADOS_VEHICULO) 
        self.mod_estado.setCurrentIndex(-1) # Forzamos a que empiece en blanco

        # --- ENSAMBLAJE DEL FORMULARIO ---
        formulario.addRow("Marca:", self.mod_marca)
        formulario.addRow("Modelo:", self.mod_modelo)
        formulario.addRow("Clase:", self.mod_clase)
        formulario.addRow("Año:", self.mod_anio)
        formulario.addRow("ID Propietario:", layout_propietario)
        
        formulario.addRow("Placa Actual:", layout_placa)
        formulario.addRow("Color:", self.mod_color)
        formulario.addRow("Estado Legal:", self.mod_estado)
        
        layout.addLayout(formulario)

        # ==========================================
        # MARCA DE AGUA DE AUDITORÍA
        # ==========================================
        self.lbl_auditoria = QLabel("")
        self.lbl_auditoria.setStyleSheet("color: #7f8c8d; font-size: 11px; font-style: italic;")
        layout.addWidget(self.lbl_auditoria, alignment=Qt.AlignLeft)
        
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
        """Ejecuta el trámite sugiriendo una placa generada por el sistema."""
        
        if not self.mod_placa.text():
            QMessageBox.warning(self, "Acción Inválida", "Primero debe buscar y cargar un vehículo.")
            return

        vin = self.input_buscar_vin.text().strip().upper()
        
        # --- NUEVO: Generamos la placa sugerida ---
        placa_sugerida = Validador.generar_placa_automatica()
        
        # 1. Pedimos la placa, pero ya le damos el valor generado como default
        nueva_placa, ok = QInputDialog.getText(
            self, "Trámite Oficial de Reemplacamiento", 
            f"VIN: {vin}\n\nEl sistema sugiere la siguiente placa disponible:",
            QLineEdit.Normal,
            placa_sugerida # <--- Aquí se le pasa la sugerencia
        )
        
        if ok and nueva_placa.strip():
            nueva_placa = nueva_placa.strip().upper()
            
            # Validamos (por si el usuario borró la sugerencia y escribió otra cosa)
            es_valida, msj_error = Validador.validar_placa(nueva_placa)
            if not es_valida:
                QMessageBox.warning(self, "Formato Inválido", msj_error)
                return

            # 2. Confirmación final
            confirmacion = QMessageBox.question(
                self, "Confirmación de Trámite",
                f"¿Desea asignar oficialmente la placa {nueva_placa} a este vehículo?\n\nEste movimiento es irreversible.",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirmacion == QMessageBox.Yes:
                # El gestor verifica que no esté duplicada en la base de datos
                exito, msj = GestorVehiculos.realizar_reemplacamiento(
                    vin, nueva_placa, self.usuario_actual.id_usuario
                )
                if exito:
                    QMessageBox.information(self, "Éxito", "Trámite completado. Nueva placa asignada.")
                    self.mod_placa.setText(nueva_placa)
                else:
                    QMessageBox.warning(self, "Error", msj)

    def abrir_ventana_cambio_propietario(self):
        """Ejecuta la transferencia pidiendo la CURP en lugar de un ID interno."""
        
        # --- PROTECCIÓN: Verificar que haya un vehículo cargado ---
        if not self.mod_placa.text():
            QMessageBox.warning(self, "Acción Inválida", "Primero debe buscar y cargar un vehículo.")
            return
        # -----------------------------------------------------------

        vin = self.input_buscar_vin.text().strip().upper()
        
        # 1. Pedimos un dato de la vida real (CURP)
        curp, ok = QInputDialog.getText(
            self, "Trámite: Transferencia de Propiedad", 
            "Ingrese la CURP del NUEVO propietario registrado en el padrón:"
        )
        
        if ok and curp.strip():
            # 2. Buscamos al propietario con la función que ya tenías creada
            exito, resultado = GestorPropietarios.buscar_propietario_por_curp(curp.strip().upper())
            
            if exito:
                id_nuevo = resultado["id_propietario"]
                nombre_completo = f"{resultado['nombres']} {resultado['apellido_paterno']} {resultado['apellido_materno']}".strip()
                formato_prp = f"PRP-{id_nuevo:05d}"
                
                # 3. Toque realista: Mostramos una ficha formal para que el operador verifique
                mensaje_confirmacion = (
                    f"Se ha localizado al ciudadano en el padrón municipal:\n\n"
                    f"Nombre: {nombre_completo}\n"
                    f"Identificador: {formato_prp}\n"
                    f"CURP: {resultado['curp']}\n\n"
                    f"¿Autoriza la transferencia legal de este vehículo a su nombre?"
                )
                
                confirmacion = QMessageBox.question(
                    self, "Validación de Transferencia", mensaje_confirmacion,
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if confirmacion == QMessageBox.Yes:
                    exito_tramite, msj = GestorVehiculos.transferir_propiedad(
                        vin, id_nuevo, self.usuario_actual.id_usuario
                    )
                    if exito_tramite:
                        QMessageBox.information(self, "Trámite Aprobado", msj)
                        # Se actualiza la caja de texto con el formato PRP oficial
                        self.mod_id_propietario.setText(formato_prp)
                    else:
                        QMessageBox.warning(self, "Trámite Denegado", msj)
            else:
                # Si el usuario pone una CURP que no existe
                QMessageBox.warning(self, "Búsqueda Fallida", "La CURP ingresada no se encuentra registrada en el sistema. Primero debe dar de alta al propietario.")
    # ==========================================
    # MÉTODOS LÓGICOS (Búsqueda)
    # ==========================================
    def procesar_busqueda_vehiculo(self):
        """Busca el vehículo y rellena el formulario."""
        criterio_buscado = self.input_buscar_vin.text().strip().upper()
        
        if not criterio_buscado:
            QMessageBox.warning(self, "Atención", "Por favor, ingrese un VIN o Placa para buscar.")
            return
            
        # Llamamos a la nueva función universal
        exito, resultado = GestorVehiculos.buscar_vehiculo_universal(criterio_buscado)
        
        if exito:
            self.input_buscar_vin.setText(resultado["vin"]) 
            self.mod_placa.setText(resultado["placa"])
            self.mod_marca.setText(resultado["marca"])
            self.mod_modelo.setText(resultado["modelo"])
            self.mod_anio.setText(str(resultado["anio"]))
            self.mod_clase.setText(resultado["clase"])
            id_prop = resultado["id_propietario"]
            self.mod_id_propietario.setText(f"PRP-{id_prop:05d}")
            self.mod_color.setCurrentText(resultado["color"])
            self.mod_estado.setCurrentText(resultado["estado_legal"])
            
            # MOSTRAR AUDITORÍA
            creador = resultado["creador"]
            modificador = resultado["modificador"]
            self.lbl_auditoria.setText(f"Registro original por: {creador} | Última modificación por: {modificador}")
            self.lbl_auditoria.show()
            
            
        else:
            self.limpiar_formulario_modificar()
            self.lbl_auditoria.hide()
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
        
        self.lbl_auditoria.clear()
        self.lbl_auditoria.hide()
        
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
        exito, mensaje = GestorVehiculos.actualizar_vehiculo(
            vin_objetivo, nuevo_color, nuevo_estado, self.usuario_actual.id_usuario # <-- AÑADIDO
        )
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
            self.lbl_auditoria.setVisible(False)
            
            # 2. Bloqueamos los menús desplegables
            self.mod_color.setEnabled(False)
            self.mod_estado.setEnabled(False)