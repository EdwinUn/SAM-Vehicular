from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QLineEdit, QPushButton, QComboBox, QTabWidget, 
QFormLayout, QTableWidget, QTableWidgetItem, 
QHeaderView, QMessageBox, QApplication)
from PySide6.QtCore import Qt
import logic.catalogos as cat
import random
import string

# Importamos el backend
from logic.auth import Auth
from models.usuario import Usuario
from logic.gestor_usuarios import GestorUsuarios


class PanelUsuarios(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()
        self.aplicar_permisos()
        self.cargar_lista_usuarios() # Llenar la tabla al abrir

    def configurar_ui(self):
        layout_principal = QVBoxLayout(self)

        lbl_titulo = QLabel("Gestión de Usuarios y Accesos")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(lbl_titulo)

        self.pestanas = QTabWidget()
        self.tab_registrar = QWidget()
        self.tab_gestionar = QWidget()
        
        self.pestanas.addTab(self.tab_registrar, "Nuevo Usuario")
        self.pestanas.addTab(self.tab_gestionar, "Control de Accesos")
        
        layout_principal.addWidget(self.pestanas)

        self.construir_tab_registrar()
        self.construir_tab_gestionar()

    def construir_tab_registrar(self):
        layout = QVBoxLayout(self.tab_registrar)
        formulario = QFormLayout()

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: operador_juan")
        
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(cat.ROLES_USUARIO)

        formulario.addRow("Nombre de Usuario:", self.input_nombre)
        
        formulario.addRow("Rol en el sistema:", self.combo_rol)

        layout.addLayout(formulario)

        self.btn_registrar = QPushButton("Crear Cuenta")
        self.btn_registrar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px;")
        self.btn_registrar.clicked.connect(self.procesar_registro)
        layout.addWidget(self.btn_registrar, alignment=Qt.AlignRight)

    def construir_tab_gestionar(self):
        layout = QVBoxLayout(self.tab_gestionar)

        # Tabla de usuarios
        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(4)
        self.tabla_usuarios.setHorizontalHeaderLabels(["ID", "Usuario", "Rol", "Estado"])
        self.tabla_usuarios.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_usuarios.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_usuarios.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Estilo oscuro para consistencia
        self.tabla_usuarios.setStyleSheet("""
            QTableWidget { background-color: #2b2b2b; alternate-background-color: #353535; color: #ffffff; }
            QHeaderView::section { background-color: #1e1e1e; color: #ffffff; font-weight: bold; }
        """)
        self.tabla_usuarios.itemSelectionChanged.connect(self.seleccionar_usuario_tabla)
        layout.addWidget(self.tabla_usuarios)

        # Controles de edición
        layout_edicion = QHBoxLayout()
        
        self.lbl_id_edit = QLabel("ID seleccionado: -")
        layout_edicion.addWidget(self.lbl_id_edit)

        layout_edicion.addWidget(QLabel("Nuevo Rol:"))
        self.combo_edit_rol = QComboBox()
        self.combo_edit_rol.addItems(cat.ROLES_USUARIO)
        layout_edicion.addWidget(self.combo_edit_rol)

        layout_edicion.addWidget(QLabel("Estado:"))
        self.combo_edit_estado = QComboBox()
        self.combo_edit_estado.addItems(["Activo", "Inactivo"])
        layout_edicion.addWidget(self.combo_edit_estado)

        # --- BOTÓN DE ACTUALIZAR ---
        self.btn_actualizar = QPushButton("Aplicar Cambios")
        self.btn_actualizar.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; padding: 8px;")
        self.btn_actualizar.clicked.connect(self.procesar_actualizacion)
        self.btn_actualizar.setEnabled(False) # Se activa al seleccionar a alguien
        layout_edicion.addWidget(self.btn_actualizar)
        
        # --- BOTÓN DE RESTABLECER ---
        self.btn_restablecer = QPushButton("Restablecer Contraseña")
        self.btn_restablecer.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold; padding: 8px;")
        self.btn_restablecer.clicked.connect(self.procesar_restablecimiento)
        self.btn_restablecer.setEnabled(False) # Se activa al seleccionar a alguien
        layout_edicion.addWidget(self.btn_restablecer)
        
        
        # ==========================================
        # MARCA DE AGUA DE AUDITORÍA
        # ==========================================
        self.lbl_auditoria = QLabel("")
        self.lbl_auditoria.setStyleSheet("color: #7f8c8d; font-size: 11px; font-style: italic; margin-top: 10px;")
        layout.addWidget(self.lbl_auditoria, alignment=Qt.AlignRight)

        layout.addLayout(layout_edicion)

    def aplicar_permisos(self):
        """Si por algún motivo alguien que no es Admin llega aquí, bloqueamos todo."""
        if self.usuario_actual.rol != cat.ROLES_USUARIO[0]: # Uso del índice [0] para Administrador
            self.pestanas.setEnabled(False)
            

    # ==========================================
    # LÓGICA DE INTERFAZ Y BACKEND
    # ==========================================
    def procesar_registro(self):
        nombre = self.input_nombre.text().strip()
        rol = self.combo_rol.currentText()

        if not nombre:
            QMessageBox.warning(self, "Datos Incompletos", "El nombre de usuario es obligatorio.")
            return

        # Generador de contraseña temporal (Ej. TMP-X8K9V)
        caracteres = string.ascii_uppercase + string.digits
        password_temporal = "TMP-" + "".join(random.choices(caracteres, k=5))

        # Se registra el usuario. La BD automáticamente pondrá 'debe_cambiar_password' en 1
        nuevo_usuario = Usuario(nombre_usuario=nombre,
                                password=password_temporal,
                                rol=rol,
                                id_usuario_registro=self.usuario_actual.id_usuario)
        
        exito, msj = Auth.registrar_usuario(nuevo_usuario)

        if exito:
            # Mostramos la contraseña temporal para que el Admin la anote y se la dé al empleado
            mensaje_exito = (
                f"{msj}\n\n"
                f"La cuenta ha sido creada con éxito. Entregue estas credenciales al usuario:\n\n"
                f"Usuario: {nombre}\n"
                f"Contraseña Temporal: {password_temporal}\n\n"
                f"NOTA: El sistema le exigirá cambiar esta contraseña en su primer inicio de sesión."
            )
            
            QApplication.clipboard().setText(f"Tus credenciales de acceso:\nUsuario: {nombre}\nContraseña: {password_temporal}")
            QMessageBox.information(self, "Cuenta Creada", mensaje_exito + "\n\n Las credenciales han sido copiadas al portapapeles. Puede pegarlas (Ctrl+V) para enviarlas al usuario.")
            self.input_nombre.clear()
            self.cargar_lista_usuarios() 
        else:
            QMessageBox.critical(self, "Error", msj)

    def cargar_lista_usuarios(self):
        self.tabla_usuarios.setRowCount(0)
        exito, datos = GestorUsuarios.obtener_todos_los_usuarios()
        
        if exito and datos:
            self.tabla_usuarios.setRowCount(len(datos))
            for fila_idx, usuario in enumerate(datos):
                # usuario = (id, nombre, rol, estado, creador, modificador)
                
                for col_idx in range(4): # Solo dibujamos las primeras 4 columnas
                    item = QTableWidgetItem(str(usuario[col_idx]))
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    # Guardamos el creador y modificador de forma invisible en la columna 0 (ID)
                    if col_idx == 0:
                        creador = usuario[4] if usuario[4] else "Sistema"
                        modificador = usuario[5] if usuario[5] else "Sin modificaciones"
                        item.setData(Qt.UserRole, f"Registrado por: {creador} | Última modificación: {modificador}")
                        
                    self.tabla_usuarios.setItem(fila_idx, col_idx, item)

    def seleccionar_usuario_tabla(self):
        filas_seleccionadas = self.tabla_usuarios.selectedItems()
        if filas_seleccionadas:
            fila = filas_seleccionadas[0].row()
            id_usuario = self.tabla_usuarios.item(fila, 0).text()
            rol_actual = self.tabla_usuarios.item(fila, 2).text()
            estado_actual = self.tabla_usuarios.item(fila, 3).text()

            # EXTRAEMOS LA AUDITORÍA OCULTA Y LA MOSTRAMOS
            texto_auditoria = self.tabla_usuarios.item(fila, 0).data(Qt.UserRole)
            self.lbl_auditoria.setText(texto_auditoria)

            self.lbl_id_edit.setText(f"ID seleccionado: {id_usuario}")
            self.combo_edit_rol.setCurrentText(rol_actual)
            self.combo_edit_estado.setCurrentText(estado_actual)
            self.btn_actualizar.setEnabled(True)
            self.btn_restablecer.setEnabled(True)
            
    def procesar_actualizacion(self):
        texto_id = self.lbl_id_edit.text().replace("ID seleccionado: ", "")
        if texto_id == "-":
            return

        id_usuario = int(texto_id)
        nuevo_rol = self.combo_edit_rol.currentText()
        nuevo_estado = self.combo_edit_estado.currentText()

        exito, msj = GestorUsuarios.actualizar_usuario(
            id_usuario, nuevo_rol, nuevo_estado,
            self.usuario_actual.id_usuario)

        if exito:
            QMessageBox.information(self, "Actualizado", msj)
            self.cargar_lista_usuarios()
            self.btn_actualizar.setEnabled(False)
            self.lbl_id_edit.setText("ID seleccionado: -")
            self.lbl_auditoria.clear()
        else:
            QMessageBox.critical(self, "Error", msj)
            
    def procesar_restablecimiento(self):
        # 1. Obtenemos el ID del usuario seleccionado
        texto_id = self.lbl_id_edit.text().replace("ID seleccionado: ", "")
        if texto_id == "-":
            return
            
        id_usuario = int(texto_id)
        
        # 2. Extraemos el nombre de usuario desde la tabla (columna 1) para el mensaje
        fila_seleccionada = self.tabla_usuarios.selectedItems()[0].row()
        nombre_usuario = self.tabla_usuarios.item(fila_seleccionada, 1).text()

        # 3. Preguntamos al administrador si está seguro (Doble confirmación)
        respuesta = QMessageBox.question(
            self, "Confirmar Restablecimiento", 
            f"¿Está seguro que desea revocar el acceso actual y generar una nueva contraseña temporal para el usuario '{nombre_usuario}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            # 4. Generamos la nueva contraseña (Ej. TMP-A1B2C)
            caracteres = string.ascii_uppercase + string.digits
            password_temporal = "TMP-" + "".join(random.choices(caracteres, k=5))
            
            # 5. Enviamos al backend
            exito, msj = Auth.restablecer_password_temporal(id_usuario, password_temporal, self.usuario_actual.id_usuario)
            
            if exito:
                # 6. Copiamos al portapapeles y avisamos
                QApplication.clipboard().setText(f"Nuevas credenciales de acceso:\nUsuario: {nombre_usuario}\nContraseña Temporal: {password_temporal}")
                
                QMessageBox.information(self, "Contraseña Restablecida", 
                    f"Se ha generado una nueva clave para {nombre_usuario}.\n\n"
                    f"Contraseña Temporal: {password_temporal}\n\n"
                    f" Las credenciales han sido copiadas al portapapeles. Presione Ctrl+V para enviarlas al empleado.")
                
                # Deseleccionamos todo por seguridad
                self.btn_actualizar.setEnabled(False)
                self.btn_restablecer.setEnabled(False)
                self.lbl_id_edit.setText("ID seleccionado: -")
            else:
                QMessageBox.critical(self, "Error", msj)