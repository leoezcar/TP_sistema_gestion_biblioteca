# Sistema de Gestión de Biblioteca Digital

Trabajo Práctico Final - Programación Avanzada.

## Descripción

Aplicación de consola desarrollada en Python para administrar una biblioteca digital.
Permite gestionar libros, usuarios y préstamos utilizando Programación Orientada a Objetos.

## Funcionalidades

- Alta, modificación, baja y listado de libros.
- Alta, modificación, baja y listado de usuarios.
- Registro de préstamos.
- Registro de devoluciones.
- Consulta de préstamos activos.
- Validación de que un libro no pueda tener más de un préstamo activo.

## Requerimientos técnicos incluidos

- Herencia: `Libro`, `Usuario` y `Prestamo` heredan de `Entidad`.
- Polimorfismo: las entidades implementan sus propios métodos de validación y detalle.
- Agregación: `Prestamo` relaciona un libro y un usuario existentes.
- Composición: `Prestamo` contiene un `DetallePrestamo`.
- Decorador propio: `registrar_accion`.
- Metaclase: `MetaEntidad`.
- Patrón de diseño: Strategy, aplicado a la duración de los préstamos.

## Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

## Integrantes

- Gianfranco Falcucci
- Thiago Canteros
- Leonardo Carabajal
