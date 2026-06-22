"""
Patrón de diseño aplicado: Strategy.

El sistema utiliza el patrón Strategy para calcular la cantidad máxima de días
de un préstamo según el tipo de usuario.

Justificación:
La duración de un préstamo puede cambiar según la regla elegida. En vez de
poner muchos if dentro de la clase Prestamo, se separa esa lógica en distintas
estrategias. Así, si más adelante se agrega otro tipo de usuario, se puede crear
una nueva estrategia sin modificar la clase Prestamo.
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
