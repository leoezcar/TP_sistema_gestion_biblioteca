"""
Clase Libro.

Este archivo pertenece al Módulo A. Modela los libros de la biblioteca digital.
"""

from entidad import Entidad


class Libro(Entidad):
    """
    Representa un libro dentro del sistema.

    Datos mínimos pedidos por la consigna:
    título, autor, ISBN, año de publicación y cantidad de páginas.
    """

    def __init__(self, titulo, autor, isbn, anio_publicacion, cantidad_paginas):
        super().__init__()
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.anio_publicacion = int(anio_publicacion)
        self.cantidad_paginas = int(cantidad_paginas)
        self.validar()

    def validar(self):
        """Valida que los datos principales del libro sean correctos."""
        if not self.titulo:
            raise ValueError("El título del libro no puede estar vacío.")
        if not self.autor:
            raise ValueError("El autor del libro no puede estar vacío.")
        if not self.isbn:
            raise ValueError("El ISBN del libro no puede estar vacío.")
        if self.anio_publicacion <= 0:
            raise ValueError("El año de publicación debe ser mayor a cero.")
        if self.cantidad_paginas <= 0:
            raise ValueError("La cantidad de páginas debe ser mayor a cero.")

    def modificar(self, titulo=None, autor=None, anio_publicacion=None, cantidad_paginas=None):
        """
        Modifica los datos editables del libro.

        El ISBN no se modifica porque se usa como dato de búsqueda.
        """
        if titulo:
            self.titulo = titulo
        if autor:
            self.autor = autor
        if anio_publicacion:
            self.anio_publicacion = int(anio_publicacion)
        if cantidad_paginas:
            self.cantidad_paginas = int(cantidad_paginas)

        self.validar()

    def mostrar_detalle(self):
        """Devuelve una descripción simple del libro."""
        return (
            f"[{self.obtener_estado()}] "
            f"{self.titulo} - {self.autor} | "
            f"ISBN: {self.isbn} | Año: {self.anio_publicacion} | "
            f"Páginas: {self.cantidad_paginas}"
        )

    def __str__(self):
        return self.mostrar_detalle()

    def __repr__(self):
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}')"
