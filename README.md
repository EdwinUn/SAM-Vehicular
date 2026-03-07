# SAM-Vehicular

Sistema de escritorio para la administración del padrón vehicular, registro de propietarios y control de infracciones de tránsito de un municipio. Desarrollado con arquitectura MVC, auditoría mediante triggers de base de datos y control de acceso por roles.

> **Estado:** Proyecto archivado. Se mantiene público únicamente con fines de portafolio. No se brinda soporte ni se aceptan contribuciones.

---

## Características

- **Arquitectura MVC:** Separación entre modelos (`models/`), lógica de negocio (`logic/`) e interfaces gráficas (`views/`).
- **Control de acceso por roles (RBAC):** Cuatro perfiles: Administrador, Operador Administrativo, Agente de Tránsito y Supervisor.
- **Auditoría automática:** Triggers SQL registran cada inserción o modificación con usuario, fecha y detalle del cambio.
- **Validaciones de formato:** VIN (17 caracteres), CURP, placas estatales y número de placa de agentes.
- **Interfaz en modo oscuro:** Construida con PySide6 y hojas de estilo QSS.

---

## Stack

| Componente | Tecnología |
| :--- | :--- |
| Lenguaje | Python 3.10+ |
| GUI | PySide6 (Qt for Python) |
| Base de datos | SQLite3 |
| Seguridad | Hashing SHA-256 |

---

## Instalación
```bash
python -m venv venv && source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install PySide6
python semilla_datos.py   # Crea la base de datos y carga datos de prueba
python main.py
```

---

## Credenciales de demo

Definidas en `semilla_datos.py`.

| Rol | Usuario | Contraseña | Acceso |
| :--- | :--- | :--- | :--- |
| Administrador | `admin_central` | `admin123` | Usuarios, agentes y auditoría |
| Operador | `operador_1` | `operador123` | Vehículos, propietarios y trámites |
| Agente | `agente_007` | `agente123` | Registro de infracciones |
| Supervisor | `supervisor_general` | `super123` | Cobro, cancelación y reportes |

---

## Reglas de negocio

- Los trámites de reemplacamiento o transferencia quedan bloqueados si existen infracciones pendientes.
- VIN, marca, modelo y año son inmutables tras el registro inicial.
- Usuarios con contraseña temporal deben cambiarla en el primer inicio de sesión.
- Los montos de multa deben respetar los rangos del catálogo oficial.

---

## Mejoras identificadas

- Hasheo con salt aleatorio y gestión de sesiones con tokens.
- Migración a PostgreSQL para concurrencia en red.
- Integración con pasarelas de pago.
- Envío de boletas por correo (SMTP).

---

## Uso de IA

El proyecto utilizó asistentes de IA para la generación de estructuras base de la interfaz, optimización de consultas SQL y documentación. La lógica de negocio, la arquitectura y la supervisión técnica fueron responsabilidad del autor.