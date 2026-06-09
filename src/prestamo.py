from datetime import datetime
from libro import Libro
from usuario import Usuario
from entidad import Entidad


class DetallePrestamo:
    def __init__(self):
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = None

    def registrar_devolucion(self):
        self.fecha_devolucion = datetime.now()

    def esta_activo(self) -> bool:
        return self.fecha_devolucion is None


class Prestamo(Entidad):
    def __init__(self, libro: Libro, usuario: Usuario):
        super().__init__()
        self.libro = libro
        self.usuario = usuario
        self.detalle = DetallePrestamo()
        self.validar()

    def validar(self):
        if not self.libro or not self.usuario:
            raise ValueError(
                "El préstamo requiere un libro y un usuario válidos"
            )
        if not self.libro.activo:
            raise ValueError("El libro no está disponible en el sistema")
        if not self.usuario.activo:
            raise ValueError("El usuario no está activo en el sistema")

    def devolver(self):
        self.detalle.registrar_devolucion()

    def es_activo(self) -> bool:
        return self.detalle.esta_activo()

    def mostrar_detalle(self) -> str:
        if self.es_activo():
            estado = "Activo"
        else:
            fecha = self.detalle.fecha_devolucion.strftime("%Y-%m-%d")
            estado = f"Devuelto el {fecha}"
        return (
            f"Préstamo: {self.libro.titulo} -> "
            f"{self.usuario.nombre} {self.usuario.apellido} | {estado}"
        )

    def __repr__(self) -> str:
        return (
            f"Prestamo(libro='{self.libro.titulo}', "
            f"usuario='{self.usuario.nombre} {self.usuario.apellido}')"
        )
