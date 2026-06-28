"""
Decoradores propios del sistema.

"""

from functools import wraps


def registrar_accion(funcion):
    """
    Decorador que muestra por consola qué acción se ejecutó.

    Se usa en métodos como activar() y desactivar() de Entidad. Sirve para
    demostrar el uso de decoradores de manera simple y entendible.
    """

    @wraps(funcion)
    def envoltorio(*args, **kwargs):
        resultado = funcion(*args, **kwargs)
        nombre_accion = funcion.__name__.replace("_", " ")
        print(f"[Registro] Se ejecutó la acción: {nombre_accion}")
        return resultado

    return envoltorio
