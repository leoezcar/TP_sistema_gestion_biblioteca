# Diagrama UML - Sistema de Gestión de Biblioteca Digital

Este diagrama representa las clases principales del sistema, sus atributos, métodos principales y relaciones.

```mermaid
classDiagram
    class MetaEntidad {
        <<metaclass>>
        +__new__(nombre, bases, atributos)
    }

    class Entidad {
        <<abstracta>>
        -_ultimo_id: int
        +id: int
        +activo: bool
        +__init__()
        +activar()
        +desactivar()
        +validar()
        +obtener_estado()
    }

    class Libro {
        +titulo: str
        +autor: str
        +isbn: str
        +anio_publicacion: int
        +cantidad_paginas: int
        +__init__(titulo, autor, isbn, anio_publicacion, cantidad_paginas)
        +validar()
        +modificar(titulo, autor, anio_publicacion, cantidad_paginas)
        +mostrar_detalle()
    }

    class Usuario {
        +nombre: str
        +apellido: str
        +dni: str
        +correo_electronico: str
        +tipo_usuario: str
        +__init__(nombre, apellido, dni, correo_electronico, tipo_usuario)
        +validar()
        +modificar(nombre, apellido, correo_electronico, tipo_usuario)
        +mostrar_detalle()
    }

    class Prestamo {
        +libro: Libro
        +usuario: Usuario
        +estrategia: EstrategiaPrestamo
        +detalle: DetallePrestamo
        +__init__(libro, usuario)
        +validar()
        +devolver()
        +es_activo()
        +mostrar_detalle()
    }

    class DetallePrestamo {
        +fecha_prestamo: datetime
        +fecha_devolucion: datetime
        +dias_maximos: int
        +fecha_vencimiento: datetime
        +__init__(dias_maximos)
        +registrar_devolucion()
        +esta_activo()
    }

    class EstrategiaPrestamo {
        <<interface>>
        +obtener_dias_maximos()
    }

    class EstrategiaPrestamoNormal {
        +obtener_dias_maximos()
    }

    class EstrategiaPrestamoDocente {
        +obtener_dias_maximos()
    }

    class EstrategiaPrestamoInvestigador {
        +obtener_dias_maximos()
    }

    class GestorLibros {
        +libros: list
        +alta_libro(titulo, autor, isbn, anio_publicacion, cantidad_paginas)
        +buscar_por_isbn(isbn)
        +modificar_libro(isbn, titulo, autor, anio_publicacion, cantidad_paginas)
        +baja_libro(isbn)
        +listar_libros(solo_activos)
    }

    class GestorUsuarios {
        +usuarios: list
        +alta_usuario(nombre, apellido, dni, correo_electronico, tipo_usuario)
        +buscar_por_dni(dni)
        +modificar_usuario(dni, nombre, apellido, correo_electronico, tipo_usuario)
        +baja_usuario(dni)
        +listar_usuarios(solo_activos)
    }

    class GestorPrestamos {
        +prestamos: list
        +libro_tiene_prestamo_activo(libro)
        +registrar_prestamo(libro, usuario)
        +devolver_prestamo_por_isbn(isbn)
        +listar_prestamos()
        +listar_prestamos_activos()
    }

    MetaEntidad ..> Entidad : define estructura
    Entidad <|-- Libro
    Entidad <|-- Usuario
    Entidad <|-- Prestamo

    Prestamo o-- Libro : agregación
    Prestamo o-- Usuario : agregación
    Prestamo *-- DetallePrestamo : composición
    Prestamo --> EstrategiaPrestamo : usa

    EstrategiaPrestamo <|.. EstrategiaPrestamoNormal
    EstrategiaPrestamo <|.. EstrategiaPrestamoDocente
    EstrategiaPrestamo <|.. EstrategiaPrestamoInvestigador

    GestorLibros o-- Libro : administra
    GestorUsuarios o-- Usuario : administra
    GestorPrestamos o-- Prestamo : administra
```

## Explicación de las relaciones

### Herencia

`Libro`, `Usuario` y `Prestamo` heredan de `Entidad`.

Esto permite reutilizar atributos y métodos comunes, como `id`, `activo`, `activar()`, `desactivar()` y `obtener_estado()`.

### Agregación

`Prestamo` se relaciona con `Libro` y `Usuario`.

Se considera agregación porque el libro y el usuario existen independientemente del préstamo. Es decir, si se elimina un préstamo, el libro y el usuario siguen existiendo en el sistema.

### Composición

`Prestamo` contiene un `DetallePrestamo`.

Se considera composición porque el detalle de fechas existe como parte del préstamo. Si el préstamo no existe, el detalle del préstamo tampoco tiene sentido por sí solo.

### Patrón de diseño Strategy

El sistema utiliza el patrón Strategy mediante la clase `EstrategiaPrestamo` y sus implementaciones:

- `EstrategiaPrestamoNormal`
- `EstrategiaPrestamoDocente`
- `EstrategiaPrestamoInvestigador`

Este patrón permite calcular la duración máxima del préstamo según el tipo de usuario sin modificar la clase `Prestamo`.

### Metaclase

`MetaEntidad` se utiliza para controlar que las clases principales del dominio que heredan de `Entidad` tengan un método `validar()`.

### Decorador

El decorador `registrar_accion` se utiliza en métodos como `activar()` y `desactivar()` para registrar acciones realizadas sobre las entidades.
