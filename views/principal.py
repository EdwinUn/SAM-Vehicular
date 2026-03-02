from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
QPushButton, QStackedWidget, QLabel, QFrame, QGridLayout, QLineEdit, QMessageBox)
from PySide6.QtCore import Qt

# Importación de paneles de vistas
from views.panel_vehiculos import PanelVehiculos
from views.panel_multas import PanelMultas
from views.panel_propietarios import PanelPropietarios
from views.panel_reportes import PanelReportes
from views.panel_usuarios import PanelUsuarios
from views.panel_agentes import PanelAgentes

# Importación del backend para el Dashboard
from logic.gestor_vehiculos import GestorVehiculos
import logic.catalogos as cat

class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario_actual):
        super().__init__()
        # Recibimos el objeto Usuario completo desde el Login
        self.usuario = usuario_actual 
        self.setWindowTitle(f"Sistema Administrativo Municipal - {self.usuario.nombre_usuario}")
        self.resize(1000, 600)

        self.configurar_ui()
        self.aplicar_permisos_rol()
        
        # === NUEVO: Cargar los datos del Dashboard al arrancar ===
        self.actualizar_dashboard()

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
        self.btn_agentes = self.crear_boton_menu("Agentes")
        

        self.btn_cerrar_sesion = self.crear_boton_menu("Cerrar Sesión")
        # Le damos un estilo rojo peligro para diferenciarlo
        self.btn_cerrar_sesion.setStyleSheet("""
            QPushButton {
                background-color: #c0392b; 
                border: none;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        
        layout_menu.addWidget(self.btn_inicio)
        layout_menu.addWidget(self.btn_vehiculos)
        layout_menu.addWidget(self.btn_propietarios)
        layout_menu.addWidget(self.btn_infracciones)
        layout_menu.addWidget(self.btn_agentes)
        layout_menu.addWidget(self.btn_reportes)
        layout_menu.addWidget(self.btn_usuarios)
        
        layout_menu.addStretch() 
        layout_menu.addWidget(self.btn_cerrar_sesion)
        
        # ==========================
        # 2. ÁREA DE CONTENIDO (QStackedWidget)
        # ==========================
        self.stacked_widget = QStackedWidget()
        
        # Instanciamos los paneles
        self.vista_inicio = self.pantalla_inicio() # <--- AHORA LLAMA A LA FUNCIÓN DEL DASHBOARD
        self.vista_vehiculos = PanelVehiculos(self.usuario)
        self.vista_propietarios = PanelPropietarios(self.usuario)
        self.vista_multas = PanelMultas(self.usuario)
        self.vista_agentes = PanelAgentes(self.usuario)
        self.vista_reportes = PanelReportes(self.usuario)
        self.vista_usuarios = PanelUsuarios(self.usuario)

        # Agregar las vistas al QStackedWidget (El orden importa para los índices)
        self.stacked_widget.addWidget(self.vista_inicio)       # Índice 0
        self.stacked_widget.addWidget(self.vista_vehiculos)    # Índice 1
        self.stacked_widget.addWidget(self.vista_propietarios) # Índice 2
        self.stacked_widget.addWidget(self.vista_multas)       # Índice 3
        self.stacked_widget.addWidget(self.vista_reportes)     # Índice 4
        self.stacked_widget.addWidget(self.vista_usuarios)     # Índice 5
        self.stacked_widget.addWidget(self.vista_agentes)

        # Conectar botones con la función de cambio de página
        # === NUEVO: Al darle a inicio, también actualiza los números ===
        self.btn_inicio.clicked.connect(self.mostrar_inicio) 
        self.btn_vehiculos.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_propietarios.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_infracciones.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.btn_reportes.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.btn_usuarios.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        self.btn_agentes.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))
        self.btn_cerrar_sesion.clicked.connect(self.ejecutar_cierre_sesion)
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
    
    # === FUNCIÓN AUXILIAR PARA EL BOTÓN INICIO ===
    def mostrar_inicio(self):
        """Muestra el panel de inicio y refresca los datos al vuelo."""
        self.stacked_widget.setCurrentIndex(0)
        self.actualizar_dashboard()

    # ==========================
    # DASHBOARD
    # ==========================
    def pantalla_inicio(self):
        """Configura el Dashboard principal con tarjetas de resumen."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # TÍTULO
        titulo = QLabel("Panel de Control (Dashboard)")
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #cdd6f4;")
        layout.addWidget(titulo)
        
        subtitulo = QLabel("Resumen operativo del padrón vehicular")
        subtitulo.setStyleSheet("font-size: 16px; color: #a6adc8; margin-bottom: 20px;")
        layout.addWidget(subtitulo)

        # CONTENEDOR DE TARJETAS
        grid_tarjetas = QGridLayout()
        grid_tarjetas.setSpacing(20)
        
        def crear_tarjeta(titulo_texto, valor_inicial, color_borde):
            tarjeta = QWidget()
            tarjeta.setStyleSheet(f"""
                QWidget {{
                    background-color: #313244;
                    border-radius: 10px;
                    border-left: 5px solid {color_borde};
                }}
            """)
            t_layout = QVBoxLayout(tarjeta)
            
            lbl_tit = QLabel(titulo_texto)
            lbl_tit.setStyleSheet("font-size: 14px; font-weight: bold; color: #a6adc8; border: none;")
            
            lbl_val = QLabel(str(valor_inicial))
            lbl_val.setStyleSheet("font-size: 32px; font-weight: bold; color: #cdd6f4; border: none;")
            
            t_layout.addWidget(lbl_tit)
            t_layout.addWidget(lbl_val)
            
            return tarjeta, lbl_val 

        # Creamos las tarjetas
        tarjeta_1, self.lbl_tot_vehiculos = crear_tarjeta("Total Vehículos", "0", "#89b4fa")
        tarjeta_2, self.lbl_tot_reportados = crear_tarjeta("Autos Reportados", "0", "#f38ba8")
        tarjeta_3, self.lbl_tot_multas = crear_tarjeta("Multas Pendientes", "0", "#f9e2af")
        tarjeta_4, self.lbl_tot_recaudacion = crear_tarjeta("Recaudación", "$0.00", "#a6e3a1")

        grid_tarjetas.addWidget(tarjeta_1, 0, 0)
        grid_tarjetas.addWidget(tarjeta_2, 0, 1)
        grid_tarjetas.addWidget(tarjeta_3, 1, 0)
        grid_tarjetas.addWidget(tarjeta_4, 1, 1)
        
        layout.addLayout(grid_tarjetas)
        
        # BOTÓN DE ACTUALIZAR
        layout.addSpacing(30)

        btn_actualizar = QPushButton("↻ Refrescar Datos")
        btn_actualizar.setMaximumWidth(200)
        btn_actualizar.clicked.connect(self.actualizar_dashboard)
        layout.addWidget(btn_actualizar, alignment=Qt.AlignCenter)
        
        layout.addStretch()

        layout.addWidget(btn_actualizar, alignment=Qt.AlignCenter)
        
        # ==========================================
        # NUEVO: SECCIÓN DE BÚSQUEDA RÁPIDA
        # ==========================================
        layout.addSpacing(30)
        
        # 1. Línea separadora visual
        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setStyleSheet("background-color: #45475a; max-height: 1px;")
        layout.addWidget(linea)
        
        layout.addSpacing(20)

        # 2. Título de la sección
        lbl_busqueda = QLabel("Búsqueda Rápida de Vehículo")
        lbl_busqueda.setStyleSheet("font-size: 18px; font-weight: bold; color: #cdd6f4;")
        layout.addWidget(lbl_busqueda)

        # 3. Barra de búsqueda y botón
        layout_buscar = QHBoxLayout()
        self.input_busqueda_rapida = QLineEdit()
        self.input_busqueda_rapida.setPlaceholderText("Ingrese Placa o VIN (Ej. YUC-1234)...")
        self.input_busqueda_rapida.setMinimumHeight(40)
        
        btn_buscar_rapido = QPushButton("🔍 Buscar")
        btn_buscar_rapido.setMinimumHeight(40)
        btn_buscar_rapido.setStyleSheet("background-color: #89b4fa; color: #1e1e2e; font-weight: bold; padding: 0px 20px;")
        btn_buscar_rapido.clicked.connect(self.ejecutar_busqueda_rapida)

        layout_buscar.addWidget(self.input_busqueda_rapida)
        layout_buscar.addWidget(btn_buscar_rapido)
        layout.addLayout(layout_buscar)

        # 4. Etiqueta para mostrar el resultado (inicia oculta)
        self.lbl_resultado_busqueda = QLabel("")
        self.lbl_resultado_busqueda.setWordWrap(True)
        self.lbl_resultado_busqueda.hide() 
        layout.addWidget(self.lbl_resultado_busqueda)

        layout.addStretch() # (Asegúrate de mantener este addStretch al final)
        
        return widget
        
        # === IMPORTANTE: Ahora retornamos el widget en lugar de añadirlo aquí ===
        return widget 

    def actualizar_dashboard(self):
        """Consulta el backend y actualiza los números de las tarjetas."""
        stats = GestorVehiculos.obtener_estadisticas_dashboard()
        
        self.lbl_tot_vehiculos.setText(f"{stats['total_vehiculos']:,}")
        self.lbl_tot_reportados.setText(f"{stats['reportados']:,}")
        self.lbl_tot_multas.setText(f"{stats['multas_pendientes']:,}")
        self.lbl_tot_recaudacion.setText(f"${stats['recaudacion']:,.2f} MXN")

    def ejecutar_busqueda_rapida(self):
        """Busca un vehículo desde el dashboard y muestra una mini-tarjeta de resultado."""
        criterio = self.input_busqueda_rapida.text().strip().upper()
        
        if not criterio:
            self.lbl_resultado_busqueda.setText("⚠️ Por favor, ingrese un VIN o Placa para buscar.")
            self.lbl_resultado_busqueda.setStyleSheet("color: #f9e2af; background-color: #181825; padding: 15px; border-radius: 5px; border-left: 5px solid #f9e2af;")
            self.lbl_resultado_busqueda.show()
            return
            
        # Reutilizamos nuestro "Omnibox" del Gestor
        exito, resultado = GestorVehiculos.buscar_vehiculo_universal(criterio)
        
        if exito:
            # Si lo encuentra, usamos un poco de HTML para dibujar una tabla bonita dentro del QLabel
            estado = resultado['estado_legal']
            color_estado = "#a6e3a1" if estado == "Activo" else "#f38ba8" # Verde si activo, rojo si reportado
            
            texto_html = f"""
            <table width='100%' cellpadding='5'>
                <tr>
                    <td><b>Placa:</b> {resultado['placa']}</td>
                    <td><b>VIN:</b> {resultado['vin']}</td>
                </tr>
                <tr>
                    <td><b>Marca:</b> {resultado['marca']}</td>
                    <td><b>Modelo:</b> {resultado['modelo']} ({resultado['anio']})</td>
                </tr>
                <tr>
                    <td><b>Color:</b> {resultado['color']}</td>
                    <td><b>Estado:</b> <span style='color: {color_estado}; font-weight: bold;'>{estado}</span></td>
                </tr>
            </table>
            """
            self.lbl_resultado_busqueda.setText(texto_html)
            self.lbl_resultado_busqueda.setStyleSheet("color: #cdd6f4; background-color: #313244; padding: 15px; border-radius: 5px; border-left: 5px solid #89b4fa;")
        else:
            # Si no existe, mostramos error
            self.lbl_resultado_busqueda.setText(f"❌ {resultado}")
            self.lbl_resultado_busqueda.setStyleSheet("color: #f38ba8; background-color: #181825; padding: 15px; border-radius: 5px; border-left: 5px solid #f38ba8;")
            
        self.lbl_resultado_busqueda.show()



    # ==========================
    # PERMISOS Y SEGREGACIÓN DE FUNCIONES
    # ==========================
    def aplicar_permisos_rol(self):
        rol = self.usuario.rol

        # 1. Administrador (IT / Seguridad) -> Solo gestiona el sistema y vigila
        if rol == cat.ROLES_USUARIO[0]:
            # El admin NO hace trabajo operativo
            self.btn_vehiculos.hide()
            self.btn_propietarios.hide()
            self.btn_infracciones.hide()
            # Se queda con: Inicio, Agentes (Catálogo), Reportes (Auditoría) y Usuarios.
        
        # 2. Operador Administrativo -> Trámites de Padrón Vehicular
        elif rol == cat.ROLES_USUARIO[1]:
            # No toca multas ni accesos al sistema
            self.btn_infracciones.hide()
            self.btn_usuarios.hide()
            self.btn_agentes.hide() 
            
        # 3. Agente de Tránsito -> Multas de calle
        elif rol == cat.ROLES_USUARIO[2]:
            # Solo levanta multas, no ve nada de gestión ni reportes financieros
            self.btn_propietarios.hide()
            self.btn_reportes.hide()
            self.btn_usuarios.hide()
            self.btn_agentes.hide()
            
        # 4. Supervisor -> Jefatura, cobros y reportes
        elif rol == cat.ROLES_USUARIO[3]:
            # Solo ve reportes y cancela/cobra multas. No registra autos nuevos.
            self.btn_vehiculos.hide()
            self.btn_propietarios.hide()
            self.btn_usuarios.hide()
            self.btn_agentes.hide()
            
    def ejecutar_cierre_sesion(self):
        """Muestra un diálogo de confirmación antes de cerrar la sesión."""
        
        # 1. Crear la ventana emergente de pregunta
        respuesta = QMessageBox.question(
            self, 
            "Confirmar Cierre de Sesión", 
            "¿Está seguro de que desea salir de su cuenta?",
            QMessageBox.Yes | QMessageBox.No, # Botones a mostrar
            QMessageBox.No # Botón seleccionado por defecto (para evitar enter accidental)
        )
        
        # 2. Evaluar qué botón presionó el usuario
        if respuesta == QMessageBox.Yes:
            # IMPORTACIÓN LOCAL: Solo se ejecuta si el usuario dice "Sí"
            from views.login import VentanaLogin 
            
            # Instanciamos la ventana de Login de nuevo
            self.ventana_login = VentanaLogin()
            self.ventana_login.show()
            
            # Destruimos la ventana principal actual
            self.close()