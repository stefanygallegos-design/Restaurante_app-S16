# Restaurante App - Semana 16

**Estudiante:** Stefany Gallegos Zari

**Asignatura:** Programación Orientada a Objetos

**Semana:** 16

**Tema:** Manejo de eventos en Tkinter

---

## Descripción

Restaurante App es una aplicación desarrollada en Python utilizando Tkinter para la gestión básica de un restaurante.

La aplicación permite administrar usuarios, productos y ventas utilizando una arquitectura modular y archivos JSON para la persistencia de información.

La Semana 16 se enfoca principalmente en la implementación de eventos de Tkinter aplicados a la gestión de usuarios.

---

## Estructura

```text
restaurante_app/

├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
│
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
│
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
│
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
│
├── assets/
│
├── main.py
└── README.md
