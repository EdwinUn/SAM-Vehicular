from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QGridLayout, 
                             QMessageBox, QGroupBox, QScrollArea)
from PySide6.QtCore import Qt
import logic.catalogos as cat
from logic.gestor_propietarios import GestorPropietarios

class TabModificarPropietario(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.configurar_ui()

    def configurar_ui(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        widget_contenedor = QWidget()
        layout_principal = QVBoxLayout(widget_contenedor)
        layout_principal.setSpacing(20)
        layout_principal.setContentsMargins(30, 20, 30, 20)

        # --- BÚSQUEDA ---
        layout_busqueda = QHBoxLayout()
        self.input_buscar_curp = QLineEdit()
        self.input_buscar_curp.setPlaceholderText("CURP a buscar...")
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.procesar_busqueda)
        layout_busqueda.addWidget(QLabel("Nombre:"))
        layout_busqueda.addWidget(self.input_buscar_curp)
        layout_busqueda.addWidget(btn_buscar)
        layout_principal.addLayout(layout_busqueda)

        # --- BLOQUE 1: DATOS PERSONALES (SOLO LECTURA) ---
        grupo_personales = QGroupBox("Datos Personales (Inmutables)")
        grupo_personales.setStyleSheet("QGroupBox { font-weight: bold; color: #f38ba8; padding-top: 20px; }")
        grid_pers = QGridLayout()
        grid_pers.setSpacing(15)

        self.mod_id = QLineEdit(); self.mod_id.setReadOnly(True)
        self.mod_nombres = QLineEdit(); self.mod_nombres.setReadOnly(True)
        self.mod_ap_paterno = QLineEdit(); self.mod_ap_paterno.setReadOnly(True)
        self.mod_ap_materno = QLineEdit(); self.mod_ap_materno.setReadOnly(True)
        self.mod_curp = QLineEdit(); self.mod_curp.setReadOnly(True)

        grid_pers.addWidget(QLabel("ID Propietario:"), 0, 0); grid_pers.addWidget(self.mod_id, 0, 1)
        grid_pers.addWidget(QLabel("CURP:"), 0, 2); grid_pers.addWidget(self.mod_curp, 0, 3)
        grid_pers.addWidget(QLabel("Nombre(s):"), 1, 0); grid_pers.addWidget(self.mod_nombres, 1, 1, 1, 3)
        grid_pers.addWidget(QLabel("Ap. Paterno:"), 2, 0); grid_pers.addWidget(self.mod_ap_paterno, 2, 1)
        grid_pers.addWidget(QLabel("Ap. Materno:"), 2, 2); grid_pers.addWidget(self.mod_ap_materno, 2, 3)
        grupo_personales.setLayout(grid_pers); layout_principal.addWidget(grupo_personales)

        # --- BLOQUE 2: DIRECCIÓN (EDITABLE) ---
        grupo_dir = QGroupBox("Dirección Actualizable")
        grupo_dir.setStyleSheet("QGroupBox { font-weight: bold; color: #89b4fa; padding-top: 20px; }")
        grid_dir = QGridLayout(); grid_dir.setSpacing(15)

        self.mod_calle = QLineEdit()
        self.mod_num_ext = QLineEdit()
        self.mod_num_int = QLineEdit()
        self.mod_colonia = QLineEdit()
        self.mod_cp = QLineEdit()
        self.mod_ciudad = QLineEdit()
        self.mod_ciudad.setReadOnly(True)
        self.mod_ciudad.setStyleSheet("background-color: #181825; color: #a6adc8;")
        self.mod_estado_prov = QLineEdit()
        self.mod_estado_prov.setReadOnly(True)
        self.mod_estado_prov.setStyleSheet("background-color: #181825; color: #a6adc8;")

        grid_dir.addWidget(QLabel("Calle:"), 0, 0); grid_dir.addWidget(self.mod_calle, 0, 1, 1, 3)
        grid_dir.addWidget(QLabel("No. Ext:"), 1, 0); grid_dir.addWidget(self.mod_num_ext, 1, 1)
        grid_dir.addWidget(QLabel("No. Int:"), 1, 2); grid_dir.addWidget(self.mod_num_int, 1, 3)
        grid_dir.addWidget(QLabel("Colonia:"), 2, 0); grid_dir.addWidget(self.mod_colonia, 2, 1)
        grid_dir.addWidget(QLabel("C.P.:"), 2, 2); grid_dir.addWidget(self.mod_cp, 2, 3)
        self.mod_cp.textChanged.connect(self.autocompletar_ubicacion_mod)
        grid_dir.addWidget(QLabel("Ciudad:"), 3, 0); grid_dir.addWidget(self.mod_ciudad, 3, 1)
        grid_dir.addWidget(QLabel("Estado:"), 3, 2); grid_dir.addWidget(self.mod_estado_prov, 3, 3)
        grupo_dir.setLayout(grid_dir); layout_principal.addWidget(grupo_dir)

        # --- BLOQUE 3: CONTACTO Y ESTADO (EDITABLE) ---
        grupo_cont = QGroupBox("Contacto y Estado Administrativo")
        grupo_cont.setStyleSheet("QGroupBox { font-weight: bold; color: #89b4fa; padding-top: 20px; }")
        grid_cont = QGridLayout(); grid_cont.setSpacing(15)

        self.mod_tel = QLineEdit()
        self.mod_correo = QLineEdit()
        self.mod_lic = QComboBox(); self.mod_lic.addItems(cat.ESTADOS_LICENCIA)
        self.mod_estado_sis = QComboBox(); self.mod_estado_sis.addItems(cat.ESTADOS_PROPIETARIO)
        self.mod_estado_sis.setCurrentIndex(-1)
        grid_cont.addWidget(QLabel("Teléfono:"), 0, 0); grid_cont.addWidget(self.mod_tel, 0, 1)
        grid_cont.addWidget(QLabel("Correo:"), 0, 2); grid_cont.addWidget(self.mod_correo, 0, 3)
        grid_cont.addWidget(QLabel("Licencia:"), 1, 0); grid_cont.addWidget(self.mod_lic, 1, 1)
        grid_cont.addWidget(QLabel("Estado:"), 1, 2); grid_cont.addWidget(self.mod_estado_sis, 1, 3)
        grupo_cont.setLayout(grid_cont); layout_principal.addWidget(grupo_cont)

        # Auditoría
        self.lbl_auditoria = QLabel("")
        self.lbl_auditoria.setStyleSheet("color: #7f8c8d; font-size: 11px; font-style: italic;")
        layout_principal.addWidget(self.lbl_auditoria)

        # Botón
        self.btn_actualizar = QPushButton("Actualizar Propietario")
        self.btn_actualizar.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 12px;")
        self.btn_actualizar.clicked.connect(self.procesar_actualizacion)
        layout_principal.addWidget(self.btn_actualizar, alignment=Qt.AlignRight)

        scroll_area.setWidget(widget_contenedor)
        QVBoxLayout(self).addWidget(scroll_area)

    def procesar_busqueda(self):
        curp = self.input_buscar_curp.text().strip().upper()
        exito, res = GestorPropietarios.buscar_propietario_por_curp(curp)
        if exito:
            self.mod_id.setText(f"PRP-{res['id_propietario']:05d}")
            self.mod_nombres.setText(res['nombres']); self.mod_ap_paterno.setText(res['apellido_paterno'])
            self.mod_ap_materno.setText(res['apellido_materno']); self.mod_curp.setText(res['curp'])
            self.mod_calle.setText(res['calle']); self.mod_num_ext.setText(res['numero_exterior'])
            self.mod_num_int.setText(res['numero_interior']); self.mod_colonia.setText(res['colonia'])
            self.mod_cp.setText(res['codigo_postal']); self.mod_ciudad.setText(res['ciudad'])
            self.mod_estado_prov.setText(res['estado_provincia']); self.mod_tel.setText(res['telefono'])
            self.mod_correo.setText(res['correo']); self.mod_lic.setCurrentText(res['estado_licencia'])
            self.mod_estado_sis.setCurrentText(res['estado'])
            self.lbl_auditoria.setText(f"Registrado por: {res['creador']} | Última modificación: {res['modificador']}")
        else:
            QMessageBox.critical(self, "Error", res)

    def procesar_actualizacion(self):
        id_prop = int(self.mod_id.text().replace("PRP-", ""))
        datos = {
            "calle": self.mod_calle.text().strip().upper(), "num_ext": self.mod_num_ext.text().strip().upper(),
            "num_int": self.mod_num_int.text().strip().upper(), "colonia": self.mod_colonia.text().strip().upper(),
            "cp": self.mod_cp.text().strip(), "ciudad": self.mod_ciudad.text().strip().upper(),
            "estado_prov": self.mod_estado_prov.text().strip().upper(), "telefono": self.mod_tel.text().strip(),
            "correo": self.mod_correo.text().strip().lower(), "licencia": self.mod_lic.currentText(),
            "estado": self.mod_estado_sis.currentText()
        }
        exito, msj = GestorPropietarios.modificar_propietario(id_prop, datos, self.usuario_actual.id_usuario)
        if exito: QMessageBox.information(self, "Éxito", msj)
        else: QMessageBox.critical(self, "Error", msj)
        
    def autocompletar_ubicacion_mod(self, cp_texto):
        if cp_texto in cat.MAPEO_CP:
            ciudad, estado = cat.MAPEO_CP[cp_texto]
            self.mod_ciudad.setText(ciudad)
            self.mod_estado_prov.setText(estado)

    def aplicar_permisos(self):
        """Bloquea los elementos editables si el usuario es Agente o Supervisor."""
        rol = self.usuario_actual.rol
        
        if rol not in [cat.ROLES_USUARIO[0], cat.ROLES_USUARIO[3]]:
            self.lbl_auditoria.setVisible(False)
        
        if rol in [cat.ROLES_USUARIO[2], cat.ROLES_USUARIO[3]]:
            self.btn_actualizar.setVisible(False)
            
            # Usando los nombres de variables reales definidos en configurar_ui
            self.mod_calle.setReadOnly(True)
            self.mod_num_ext.setReadOnly(True)
            self.mod_num_int.setReadOnly(True)
            self.mod_colonia.setReadOnly(True)
            self.mod_cp.setReadOnly(True)
            self.mod_tel.setReadOnly(True)
            self.mod_correo.setReadOnly(True)
            
            self.mod_lic.setEnabled(False)
            self.mod_estado_sis.setEnabled(False)