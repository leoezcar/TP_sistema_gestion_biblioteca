"""
Patrones de diseño aplicados: Strategy y Singleton.

Strategy:
    El sistema utiliza el patrón Strategy para calcular la cantidad máxima de
    días de un préstamo según el tipo de usuario. La duración puede cambiar
    según la regla elegida. En vez de poner muchos if dentro de la clase
    Prestamo, se separa esa lógica en distintas estrategias. Así, si más
    adelante se agrega otro tipo de usuario, se puede crear una nueva
    estrategia sin modificar la clase Prestamo.

Singleton:
    Las clases gestoras (GestorLibros, GestorUsuarios, GestorPrestamos) usan
    la metaclase SingletonMeta para garantizar que exista una única instancia
    de cada gestor. Esto evita que se creen colecciones duplicadas de datos
    durante la ejecución del programa.
"""


class EstrategiaPrestamo:
    """Interfaz base para las estrategias de duración de préstamos."""

    def obtener_dias_maximos(self):
        """Devuelve la cantidad máxima de días del préstamo."""
        raise NotImplementedError("Las estrategias deben implementar obtener_dias_maximos().")


class EstrategiaPrestamoNormal(EstrategiaPrestamo):
    """Estrategia para usuarios normales."""

    def obtener_dias_maximos(self):
        return 15


class EstrategiaPrestamoDocente(EstrategiaPrestamo):
    """Estrategia para usuarios docentes."""

    def obtener_dias_maximos(self):
        return 30


class EstrategiaPrestamoInvestigador(EstrategiaPrestamo):
    """Estrategia para usuarios investigadores."""

    def obtener_dias_maximos(self):
        return 45


def obtener_estrategia_por_usuario(usuario):
    """
    Devuelve la estrategia correspondiente según el tipo de usuario.

    Si el usuario no tiene definido un tipo específico, se utiliza la estrategia
    normal como valor por defecto.
    """
    tipo_usuario = getattr(usuario, "tipo_usuario", "normal").lower()

    if tipo_usuario == "docente":
        return EstrategiaPrestamoDocente()

    if tipo_usuario == "investigador":
        return EstrategiaPrestamoInvestigador()

    return EstrategiaPrestamoNormal()


class SingletonMeta(type):
    """
    Metaclase que implementa el patrón Singleton.

    Se utiliza en las clases gestoras (GestorLibros, GestorUsuarios,
    GestorPrestamos) para garantizar que solo exista una instancia de cada
    gestor durante la ejecución del programa.

    Justificación:
    En una biblioteca digital tiene sentido que la colección de libros, usuarios
    y préstamos sea administrada por un único gestor. Si se pudieran crear
    múltiples instancias, los datos podrían quedar desincronizados.
    """

    _instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            cls._instancias[cls] = super().__call__(*args, **kwargs)
        return cls._instancias[cls]
