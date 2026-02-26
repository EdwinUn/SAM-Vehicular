from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
QPushButton, QStackedWidget, QLabel, QFrame)
from PySide6.QtCore import Qt

# Importación de paneles de viewas
from views.panel_vehiculos import PanelVehiculos
from views.panel_multas import PanelMultas
from views.panel_propietarios import PanelPropietarios
from views.panel_reportes import PanelReportes
from views.panel_usuarios import PanelUsuarios

class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario_actual):
        super().__init__()
        # Recibimos el objeto Usuario completo desde el Login
        self.usuario = usuario_actual 
        self.setWindowTitle(f"Sistema Administrativo Municipal - {self.usuario.nombre_usuario}")
        self.resize(1000, 600)

        self.configurar_ui()
        self.aplicar_permisos_rol()

    def configurar_ui(self):
        # Widget central y layout principal horizontal
        widget_central = QWidget()
        layout_principal = QHBoxLayout(widget_central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)
        self.setCentralWidget(widget_central)

        # ==========================
        # 1. MENÚ LATERAL IZQUIERDO
        # ==========================
        self.menu_lateral = QFrame()
        self.menu_lateral.setFixedWidth(200)
        self.menu_lateral.setStyleSheet("background-color: #2c3e50; color: white;")
        layout_menu = QVBoxLayout(self.menu_lateral)
        layout_menu.setAlignment(Qt.AlignTop)
        layout_menu.setSpacing(10)

        # Info del usuario en el menú
        lbl_info_usuario = QLabel(f"Usuario:\n{self.usuario.nombre_usuario}\n\nRol:\n{self.usuario.rol}")
        lbl_info_usuario.setStyleSheet("font-weight: bold; margin-bottom: 20px;")
        lbl_info_usuario.setAlignment(Qt.AlignCenter)
        layout_menu.addWidget(lbl_info_usuario)

        # Botones de navegación
        self.btn_inicio = self.crear_boton_menu("Inicio")
        self.btn_vehiculos = self.crear_boton_menu("Vehículos")
        self.btn_propietarios = self.crear_boton_menu("Propietarios")
        self.btn_infracciones = self.crear_boton_menu("Infracciones")
        self.btn_reportes = self.crear_boton_menu("Reportes")
        self.btn_usuarios = self.crear_boton_menu("Gestión Usuarios")

        layout_menu.addWidget(self.btn_inicio)
        layout_menu.addWidget(self.btn_vehiculos)
        layout_menu.addWidget(self.btn_propietarios)
        layout_menu.addWidget(self.btn_infracciones)
        layout_menu.addWidget(self.btn_reportes)
        layout_menu.addWidget(self.btn_usuarios)

        # ==========================
        # 2. ÁREA DE CONTENIDO (QStackedWidget)
        # ==========================
        self.stacked_widget = QStackedWidget()
        
        # Instanciar las vistas iniciales
        self.vista_inicio = QLabel("Bienvenido al Sistema Administrativo Municipal")
        self.vista_inicio.setAlignment(Qt.AlignCenter)
        self.vista_inicio.setStyleSheet("font-size: 24px;")

        # Instanciamos los archivos creados
        self.vista_vehiculos = PanelVehiculos(self.usuario)
        self.vista_multas = PanelMultas(self.usuario)
        self.vista_propietarios = PanelPropietarios(self.usuario)
        self.vista_reportes = PanelReportes(self.usuario)
        self.vista_usuarios = PanelUsuarios(self.usuario)

        # Agregar las vistas al QStackedWidget (El orden importa para los índices)
        self.stacked_widget.addWidget(self.vista_inicio)       # Índice 0
        self.stacked_widget.addWidget(self.vista_vehiculos)    # Índice 1
        self.stacked_widget.addWidget(self.vista_propietarios) # Índice 2
        self.stacked_widget.addWidget(self.vista_multas)       # Índice 3
        self.stacked_widget.addWidget(self.vista_reportes)     # Índice 4
        self.stacked_widget.addWidget(self.vista_usuarios)     # Índice 5

        # Conectar botones con la función de cambio de página
        self.btn_inicio.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_vehiculos.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_propietarios.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_infracciones.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.btn_reportes.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.btn_usuarios.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))

        # Ensamblar el layout principal
        layout_principal.addWidget(self.menu_lateral)
        layout_principal.addWidget(self.stacked_widget)

    def crear_boton_menu(self, texto):
        """Función auxiliar para crear botones estilizados del menú lateral."""
        boton = QPushButton(texto)
        boton.setFixedHeight(40)
        boton.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                border: none;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """)
        return boton

    def aplicar_permisos_rol(self):
        """
        Oculta módulos en el menú dependiendo del rol del usuario autenticado.
        """
        rol = self.usuario.rol

        if rol == "Administrador":
            # Tiene acceso a todos los módulos y reportes completos [cite: 47-51].
            pass 
        
        elif rol == "Operador Administrativo":
            # Registra vehículos y actualiza datos permitidos, pero no gestiona configuraciones críticas [cite: 52-57].
            self.btn_infracciones.hide()
            self.btn_usuarios.hide()
            
        elif rol == "Agente de Tránsito":
            # Registra infracciones y consulta información básica, pero no modifica datos estructurales [cite: 58-61].
            self.btn_propietarios.hide()
            self.btn_reportes.hide()
            self.btn_usuarios.hide()
            
        elif rol == "Supervisor":
            # Consulta reportes y supervisa infracciones, pero no modifica información estructural [cite: 62-65].
            self.btn_vehiculos.hide()
            self.btn_propietarios.hide()
            self.btn_usuarios.hide()