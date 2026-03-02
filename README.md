# SAM-Vehicular 🚗⚖️
### Sistema Administrativo Municipal de Control Vehicular e Infracciones

**SAM-Vehicular** es una solución de escritorio robusta diseñada para la gestión integral del padrón vehicular, registro de propietarios y control de infracciones de tránsito. El sistema destaca por su arquitectura **MVC (Modelo-Vista-Controlador)**, un sistema de auditoría interna basado en *triggers* de base de datos y una estricta segregación de funciones por roles.

---

## ✨ Características Técnicas

* **Arquitectura Profesional:** Separación clara entre modelos de datos (`models/`), lógica de negocio (`logic/`) e interfaces gráficas (`views/`).
* **Control de Acceso Basado en Roles (RBAC):** Restricción de módulos y acciones según el perfil del usuario (Administrador, Operador, Agente y Supervisor).
* **Auditoría de "Caja Negra":** Registro automático de cada inserción o modificación en la base de datos, capturando el usuario responsable y los valores anteriores/nuevos para máxima transparencia.
* **Validaciones Biunívocas:** Reglas estrictas para formatos de VIN (17 caracteres), CURP, placas estatales y números de placa de agentes.
* **Interfaz Moderna:** Diseño en **Modo Oscuro** desarrollado con PySide6 y hojas de estilo QSS personalizadas.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+.
* **GUI:** PySide6 (Qt for Python).
* **Base de Datos:** SQLite3 con soporte para integridad referencial y disparadores.
* **Seguridad:** Encriptación de contraseñas mediante SHA-256.

---

## 🔑 Credenciales de Acceso (Demo)

El sistema cuenta con perfiles preconfigurados para demostración de permisos:

| Rol | Usuario | Contraseña | Capacidades |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin_central` | `admin123` | Gestión de usuarios, agentes y auditoría completa. |
| **Operador** | `operador_1` | `operador123` | Alta de vehículos, propietarios y trámites de control. |
| **Agente** | `agente_007` | `agente123` | Registro de infracciones en sitio o fotomultas. |
| **Supervisor** | `supervisor_general`| `super123` | Cobro/cancelación de multas y reportes gerenciales. |

---

## ⚖️ Reglas de Negocio Implementadas

Para garantizar la legalidad y el orden administrativo, el sistema aplica las siguientes reglas:

1.  **Bloqueo por Adeudos:** No se permite realizar trámites de reemplacamiento o transferencia de propiedad si el vehículo tiene infracciones en estado "Pendiente".
2.  **Inmutabilidad de Datos:** Los atributos estructurales del vehículo (VIN, Marca, Modelo, Año, Clase y Procedencia) no pueden ser modificados tras el registro inicial.
3.  **Seguridad de Acceso:** Los usuarios con contraseñas temporales (generadas por el Admin) están obligados a cambiar su contraseña en el primer inicio de sesión.
4.  **Integridad de Multas:** No se puede marcar como "Pagada" una infracción que ya ha sido "Cancelada".
5.  **Geolocalización Local:** Autocompletado de Ciudad y Estado basado en el Código Postal (enfocado en el estado de Yucatán).
6.  **Tabulador Oficial:** El sistema impide registrar montos de multas fuera de los rangos mínimos y máximos establecidos en el reglamento municipal para cada tipo de infracción.

---

## 🚀 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/sam-vehicular.git](https://github.com/tu-usuario/sam-vehicular.git)
    cd sam-vehicular
    ```

2.  **Configurar el entorno:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install PySide6
    ```

3.  **Inicializar con datos:**
    ```bash
    # Crea la base de datos y carga la simulación de trámites
    python semilla_datos.py 
    ```

4.  **Ejecutar:**
    ```bash
    python main.py
    ```

---
*Este proyecto es parte de un portafolio académico y profesional de desarrollo de software.*