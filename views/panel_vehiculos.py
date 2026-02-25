from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget
from PySide6.QtCore import Qt

# Importamos nuestros nuevos componentes limpios y modulares
from views.tabs.tab_registrar_vehiculo import TabRegistrarVehiculo
from views.tabs.tab_modificar_vehiculo import TabModificarVehiculo

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
        
        # Instanciamos nuestras clases independientes
        self.tab_registrar = TabRegistrarVehiculo()
        self.tab_modificar = TabModificarVehiculo()

        # Las agregamos al menú
        self.pestanas.addTab(self.tab_registrar, "Registrar Nuevo Vehículo")
        self.pestanas.addTab(self.tab_modificar, "Modificar Vehículo")

        layout_principal.addWidget(self.pestanas)