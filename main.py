import sys
from PySide6.QtWidgets import QApplication
# 1. Importamos la ventana principal directamente
from views.principal import VentanaPrincipal
import views.estilos as estilos

# from views.login import VentanaLogin # <-- Lo silenciamos temporalmente

# ==========================================
# TRUCO DE DESARROLLO (MOCK USER)
# ==========================================
class UsuarioPrueba:
    """Un gafete falso para entrar directo al sistema sin loguearse."""
    def __init__(self):
        self.id_usuario = 1
        self.nombre_usuario = "Admin de Pruebas"
        self.rol = "Agente de Tránsito" # <- Si quieren cambiar el rol solo cambian esta string por otro rol disponible
    """
    Estos son los roles disponibles:
    ROLES_USUARIO = [
    "Administrador",
    "Operador Administrativo",
    "Agente de Tránsito",
    "Supervisor"
]
    """
def main():
    app = QApplication(sys.argv)

    # --- MODO PRODUCCIÓN (Silenciado por ahora) ---
    # ventana_login = VentanaLogin()
    # ventana_login.show()
    app.setStyleSheet(estilos.TEMA_OSCURO)
    # --- MODO DESARROLLO RÁPIDO ---
    # Creamos nuestro gafete VIP y abrimos la app directamente
    gafete_vip = UsuarioPrueba()
    ventana_principal = VentanaPrincipal(gafete_vip)
    ventana_principal.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()