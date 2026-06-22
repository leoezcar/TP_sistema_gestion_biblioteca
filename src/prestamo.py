"""
Módulo B: clases relacionadas con préstamos.

Este archivo contiene DetallePrestamo y Prestamo. Además, Prestamo utiliza el
patrón Strategy definido en patron_diseno.py para calcular la duración máxima
del préstamo según el tipo de usuario.
"""

from datetime import datetime, timedelta

from entidad import Entidad
from libro import Libro
from usuario import Usuario
from patron_diseno import obtener_estrategia_por_usuario


class DetallePrestamo:
    """
    Maneja las fechas de un préstamo.

    Esta clase se usa como composición dentro de Prestamo, porque el detalle de
    fechas existe como parte del préstamo.
    """

    def __init__(self, dias_maximos):
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = None
        self.dias_maximos = dias_maximos
        self.fecha_vencimiento = self.fecha_prestamo + timedelta(days=dias_maximos)

    def registrar_devolucion(self):
        """Registra la fecha de devolución del préstamo."""
        self.fecha_devolucion = datetime.now()

    def esta_activo(self):
        """Indica si el préstamo sigue activo."""
        return self.fecha_devolucion is None


class Prestamo(Entidad):
    """
    Representa un préstamo de un libro a un usuario.

    Recibe un libro y un usuario. La validación de que el libro no tenga otro
    préstamo activo se realiza en GestorPrestamos, porque el gestor conoce la
    colección completa de préstamos.
    """

    def __init__(self, libro: Libro, usuario: Usuario):
        super().__init__()
        self.libro = libro
        self.usuario = usuario

        # Se aplica el patrón Strategy para definir los días máximos del préstamo
        # según el tipo de usuario.
        self.estrategia = obtener_estrategia_por_usuario(usuario)
        self.detalle = DetallePrestamo(self.estrategia.obtener_dias_maximos())

        self.validar()

    def validar(self):
        """Valida que el préstamo tenga libro y usuario activos."""
        if not self.libro or not self.usuario:
            raise ValueError("El préstamo requiere un libro y un usuario válidos.")
        if not self.libro.activo:
            raise ValueError("El libro no está disponible en el sistema.")
        if not self.usuario.activo:
            raise ValueError("El usuario no está activo en el sistema.")

    def devolver(self):
        """Registra la devolución del préstamo."""
        self.detalle.registrar_devolucion()

    def es_activo(self):
        """Devuelve True si el préstamo sigue activo."""
        return self.detalle.esta_activo()

    def mostrar_detalle(self):
        """Devuelve un texto descriptivo del préstamo."""
        fecha_prestamo = self.detalle.fecha_prestamo.strftime("%Y-%m-%d")
        fecha_vencimiento = self.detalle.fecha_vencimiento.strftime("%Y-%m-%d")

        if self.es_activo():
            estado = "Activo"
        else:
            fecha_devolucion = self.detalle.fecha_devolucion.strftime("%Y-%m-%d")
            estado = f"Devuelto el {fecha_devolucion}"

        return (
            f"Préstamo: {self.libro.titulo} -> "
            f"{self.usuario.nombre} {self.usuario.apellido} | "
            f"Fecha préstamo: {fecha_prestamo} | "
            f"Vencimiento: {fecha_vencimiento} | "
            f"Días máximos: {self.detalle.dias_maximos} | "
            f"Estado: {estado}"
        )

    def __str__(self):
        return self.mostrar_detalle()

    def __repr__(self):
        return (
            f"Prestamo(libro='{self.libro.titulo}', "
            f"usuario='{self.usuario.nombre} {self.usuario.apellido}')"
        )
