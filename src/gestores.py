"""
Gestores del sistema.

Este archivo pertenece al Módulo C. Contiene las clases encargadas de administrar
colecciones de libros, usuarios y préstamos.
"""

from libro import Libro
from usuario import Usuario
from prestamo import Prestamo


class GestorLibros:
    """Administra altas, bajas, modificaciones y listados de libros."""

    def __init__(self):
        self.libros = []

    def alta_libro(self, titulo, autor, isbn, anio_publicacion, cantidad_paginas):
        """Crea un libro y lo agrega a la colección."""
        if self.buscar_por_isbn(isbn) is not None:
            raise ValueError("Ya existe un libro con ese ISBN.")

        libro = Libro(titulo, autor, isbn, anio_publicacion, cantidad_paginas)
        self.libros.append(libro)
        return libro

    def buscar_por_isbn(self, isbn):
        """Busca un libro por ISBN. Si no existe, devuelve None."""
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        return None

    def modificar_libro(self, isbn, titulo=None, autor=None, anio_publicacion=None, cantidad_paginas=None):
        """Modifica un libro existente."""
        libro = self.buscar_por_isbn(isbn)
        if libro is None:
            raise ValueError("No se encontró un libro con ese ISBN.")

        libro.modificar(titulo, autor, anio_publicacion, cantidad_paginas)
        return libro

    def baja_libro(self, isbn):
        """
        Da de baja un libro.

        Se usa baja lógica: el libro queda inactivo, pero no se borra de la lista.
        """
        libro = self.buscar_por_isbn(isbn)
        if libro is None:
            raise ValueError("No se encontró un libro con ese ISBN.")

        libro.desactivar()
        return libro

    def listar_libros(self, solo_activos=False):
        """Devuelve la lista de libros."""
        if solo_activos:
            return [libro for libro in self.libros if libro.activo]
        return self.libros


class GestorUsuarios:
    """Administra altas, bajas, modificaciones y listados de usuarios."""

    def __init__(self):
        self.usuarios = []

    def alta_usuario(self, nombre, apellido, dni, correo_electronico, tipo_usuario="normal"):
        """Crea un usuario y lo agrega a la colección."""
        if self.buscar_por_dni(dni) is not None:
            raise ValueError("Ya existe un usuario con ese DNI.")

        usuario = Usuario(nombre, apellido, dni, correo_electronico, tipo_usuario)
        self.usuarios.append(usuario)
        return usuario

    def buscar_por_dni(self, dni):
        """Busca un usuario por DNI. Si no existe, devuelve None."""
        for usuario in self.usuarios:
            if usuario.dni == dni:
                return usuario
        return None

    def modificar_usuario(self, dni, nombre=None, apellido=None, correo_electronico=None, tipo_usuario=None):
        """Modifica un usuario existente."""
        usuario = self.buscar_por_dni(dni)
        if usuario is None:
            raise ValueError("No se encontró un usuario con ese DNI.")

        usuario.modificar(nombre, apellido, correo_electronico, tipo_usuario)
        return usuario

    def baja_usuario(self, dni):
        """
        Da de baja un usuario.

        Se usa baja lógica: el usuario queda inactivo, pero no se borra de la lista.
        """
        usuario = self.buscar_por_dni(dni)
        if usuario is None:
            raise ValueError("No se encontró un usuario con ese DNI.")

        usuario.desactivar()
        return usuario

    def listar_usuarios(self, solo_activos=False):
        """Devuelve la lista de usuarios."""
        if solo_activos:
            return [usuario for usuario in self.usuarios if usuario.activo]
        return self.usuarios


class GestorPrestamos:
    """Administra préstamos, devoluciones y consultas de préstamos activos."""

    def __init__(self):
        self.prestamos = []

    def libro_tiene_prestamo_activo(self, libro):
        """
        Verifica si un libro ya tiene un préstamo activo.

        Esta regla es obligatoria: un libro no puede prestarse si ya posee un
        préstamo activo.
        """
        for prestamo in self.prestamos:
            if prestamo.libro == libro and prestamo.es_activo():
                return True
        return False

    def registrar_prestamo(self, libro, usuario):
        """Registra un préstamo nuevo si el libro está disponible."""
        if libro is None:
            raise ValueError("Debe indicar un libro válido.")
        if usuario is None:
            raise ValueError("Debe indicar un usuario válido.")

        if self.libro_tiene_prestamo_activo(libro):
            raise ValueError("El libro ya posee un préstamo activo.")

        prestamo = Prestamo(libro, usuario)
        self.prestamos.append(prestamo)
        return prestamo

    def devolver_prestamo_por_isbn(self, isbn):
        """Registra la devolución del préstamo activo asociado a un ISBN."""
        for prestamo in self.prestamos:
            if prestamo.libro.isbn == isbn and prestamo.es_activo():
                prestamo.devolver()
                return prestamo

        raise ValueError("No se encontró un préstamo activo para ese ISBN.")

    def listar_prestamos(self):
        """Devuelve todos los préstamos registrados."""
        return self.prestamos

    def listar_prestamos_activos(self):
        """Devuelve solamente los préstamos que siguen activos."""
        return [prestamo for prestamo in self.prestamos if prestamo.es_activo()]
