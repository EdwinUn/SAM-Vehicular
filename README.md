# SAM-Vehicular 🚗⚖️
### Sistema Administrativo Municipal de Control Vehicular e Infracciones

**SAM-Vehicular** es una solución de escritorio robusta diseñada para la gestión integral del padrón vehicular, registro de propietarios y control de infracciones de tránsito. El sistema destaca por su arquitectura **MVC (Modelo-Vista-Controlador)**, un sistema de auditoría interna basado en *triggers* de base de datos y una estricta segregación de funciones por roles.

> **Nota de Estado:** Este proyecto se encuentra actualmente en estado **Archivado**. Se mantiene público exclusivamente con fines de portafolio académico y profesional; no se aceptarán nuevas actualizaciones ni se brinda soporte técnico.

---

## ✨ Características Técnicas

* **Arquitectura Profesional:** Separación clara entre modelos de datos (`models/`), lógica de negocio (`logic/`) e interfaces gráficas (`views/`).
* **Control de Acceso Basado en Roles (RBAC):** Restricción modular según el perfil del usuario: Administrador, Operador Administrativo, Agente de Tránsito y Supervisor.
* **Auditoría de "Caja Negra":** Registro automático de cada inserción o modificación mediante disparadores SQL que capturan el usuario, la fecha y el detalle de los cambios.
* **Validaciones Biunívocas:** Reglas estrictas para formatos de VIN (17 caracteres), CURP, placas estatales y números de placa de agentes.
* **Interfaz Moderna:** Diseño en **Modo Oscuro** desarrollado con PySide6 y hojas de estilo QSS personalizadas.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+.
* **GUI:** PySide6 (Qt for Python).
* **Base de Datos:** SQLite3 con soporte para integridad referencial.
* **Seguridad:** Encriptación de contraseñas mediante SHA-256.

---

## 🔑 Credenciales de Acceso (Demo)

El sistema cuenta con perfiles preconfigurados en el script de semillas (`semilla_datos.py`):

| Rol | Usuario | Contraseña | Capacidades |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin_central` | `admin123` | Gestión de usuarios, agentes y auditoría completa. |
| **Operador** | `operador_1` | `operador123` | Alta de vehículos, propietarios y trámites. |
| **Agente** | `agente_007` | `agente123` | Registro de infracciones en sitio o fotomultas. |
| **Supervisor** | `supervisor_general`| `super123` | Cobro/cancelación de multas y reportes. |

---

## ⚖️ Reglas de Negocio Implementadas

1.  **Bloqueo por Adeudos:** No se permiten trámites de reemplacamiento o transferencia de propiedad si existen infracciones "Pendientes".
2.  **Inmutabilidad:** Atributos estructurales (VIN, Marca, Modelo, Año) son inmutables tras el registro.
3.  **Seguridad:** Usuarios con claves temporales deben cambiarlas en su primer inicio de sesión.
4.  **Tabulador Oficial:** Las multas deben respetar los rangos mínimos y máximos legales definidos en el catálogo.

---

## 🚀 Futuras Mejoras (Roadmap)

A pesar de ser un proyecto finalizado, se identifican las siguientes áreas de crecimiento técnico:
* **Seguridad Avanzada:** Implementación de *Salt* aleatorio para hasheo y gestión de sesiones con tokens.
* **Base de Datos Relacional:** Migración a PostgreSQL para soportar concurrencia real en red.
* **Módulo de Pagos:** Integración con pasarelas de pago para multas en línea.
* **Notificaciones:** Envío automatizado de boletas de infracción vía SMTP o SMS.

---

## 🤖 Declaración de Uso de IA

Este proyecto fue desarrollado utilizando herramientas de **Inteligencia Artificial** como asistentes de programación. La IA intervino en:
* Generación de estructuras base para la interfaz gráfica (PySide6).
* Optimización de consultas SQL y lógica de triggers de auditoría.
* Refactorización de código para cumplimiento de patrones de diseño.
* Redacción de documentación técnica.

*La lógica de negocio, la arquitectura del sistema y la supervisión técnica fueron validadas y corregidas integralmente por el autor.*

---

## 📦 Instalación

1.  **Configurar entorno:** `python -m venv venv` y activar.
2.  **Dependencias:** `pip install PySide6`.
3.  **Inicializar:** `python semilla_datos.py` (Crea la DB y simula trámites).
4.  **Ejecutar:** `python main.py`.