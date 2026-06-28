"""
Clase Usuario.

"""

from entidad import Entidad


class Usuario(Entidad):
    """
    Representa un usuario del sistema.

    Datos mínimos pedidos:
    nombre, apellido, DNI y correo electrónico.
    """

    def __init__(self, nombre, apellido, dni, correo_electronico, tipo_usuario="normal"):
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.correo_electronico = correo_electronico
        self.tipo_usuario = tipo_usuario
        self.validar()

    def validar(self):
        """Valida que los datos principales del usuario sean correctos."""
        if not self.nombre:
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not self.apellido:
            raise ValueError("El apellido del usuario no puede estar vacío.")
        if not self.dni:
            raise ValueError("El DNI del usuario no puede estar vacío.")
        if not self.correo_electronico or "@" not in self.correo_electronico:
            raise ValueError("El correo electrónico del usuario no es válido.")

    def modificar(self, nombre=None, apellido=None, correo_electronico=None, tipo_usuario=None):
        """
        Modifica los datos editables del usuario.

        El DNI no se modifica porque se usa como dato de búsqueda.
        """
        if nombre:
            self.nombre = nombre
        if apellido:
            self.apellido = apellido
        if correo_electronico:
            self.correo_electronico = correo_electronico
        if tipo_usuario:
            self.tipo_usuario = tipo_usuario

        self.validar()

    def mostrar_detalle(self):
        """Devuelve una descripción simple del usuario."""
        return (
            f"[{self.obtener_estado()}] "
            f"{self.nombre} {self.apellido} | "
            f"DNI: {self.dni} | Correo: {self.correo_electronico} | "
            f"Tipo: {self.tipo_usuario}"
        )

    def __str__(self):
        return self.mostrar_detalle()

    def __repr__(self):
        return f"Usuario(nombre='{self.nombre}', apellido='{self.apellido}', dni='{self.dni}')"
