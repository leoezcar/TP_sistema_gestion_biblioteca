"""
Clase base del dominio.

Entidad representa los datos y comportamientos comunes de las clases principales
del sistema. Libro, Usuario y Prestamo heredan de esta clase.
"""

from metaclases import MetaEntidad
from decoradores import registrar_accion


class Entidad(metaclass=MetaEntidad):
    """
    Clase base para las entidades del sistema.

    Aporta un identificador automático y un estado activo/inactivo. El estado
    activo permite hacer una baja lógica: el objeto no se elimina de memoria,
    pero queda marcado como inactivo.
    """

    _ultimo_id = 0

    def __init__(self):
        Entidad._ultimo_id += 1
        self.id = Entidad._ultimo_id
        self.activo = True

    @registrar_accion
    def activar(self):
        """Marca la entidad como activa."""
        self.activo = True

    @registrar_accion
    def desactivar(self):
        """Marca la entidad como inactiva."""
        self.activo = False

    def validar(self):
        """
        Método base de validación.

        Las clases hijas deben redefinir este método con sus propias reglas.
        """
        raise NotImplementedError("Las clases hijas deben implementar validar().")

    def obtener_estado(self):
        """Devuelve el estado de la entidad en formato texto."""
        if self.activo:
            return "Activo"
        return "Inactivo"
