"""
Módulo de metaclases del sistema.

La consigna pide implementar una metaclase utilizando type o una clase derivada
de type. En este archivo se define MetaEntidad, que se usa en la clase base
Entidad.
"""


class MetaEntidad(type):
    """
    Metaclase para las clases principales del dominio.

    Esta metaclase controla que toda clase concreta que herede directamente de
    Entidad implemente el método validar(). De esta forma, Libro, Usuario y
    Prestamo quedan obligadas a tener una validación propia.
    """

    def __new__(mcls, nombre, bases, atributos):
        clase = super().__new__(mcls, nombre, bases, atributos)

        # No validamos la clase base Entidad, porque justamente Entidad define
        # la estructura común que luego van a reutilizar las demás clases.
        if nombre != "Entidad" and any(base.__name__ == "Entidad" for base in bases):
            if "validar" not in atributos:
                raise TypeError(
                    f"La clase {nombre} debe implementar el método validar()."
                )

        return clase
