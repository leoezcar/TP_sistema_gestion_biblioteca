"""
Script de pruebas funcionales para el Sistema de Gestión de Biblioteca Digital.

Ejecuta el checklist completo especificado en contexto_proyecto_biblioteca.md
sin depender del menú interactivo de main.py.
"""

import os
import sys
import traceback

# Agregar src al path igual que main.py
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_SRC = os.path.join(RUTA_BASE, "src")
sys.path.append(RUTA_SRC)

from gestores import GestorLibros, GestorUsuarios, GestorPrestamos

resultados = []
total = 0
ok = 0
fail = 0


def test(nombre, funcion):
    global total, ok, fail
    total += 1
    try:
        funcion()
        print(f"  [OK] {nombre}")
        resultados.append(("OK", nombre))
        ok += 1
    except Exception as e:
        print(f"  [FAIL] {nombre}")
        print(f"         Error: {e}")
        traceback.print_exc()
        resultados.append(("FAIL", nombre, str(e)))
        fail += 1


# ---------- INICIALIZACIÓN ----------
gestor_libros = GestorLibros()
gestor_usuarios = GestorUsuarios()
gestor_prestamos = GestorPrestamos()


# ========== GESTIÓN DE LIBROS ==========
print("\n===== GESTIÓN DE LIBROS =====")


def test_alta_libro():
    libro = gestor_libros.alta_libro("El principito", "Antoine de Saint-Exupéry", "ISBN001", 1943, 96)
    assert libro is not None
    assert libro.titulo == "El principito"
    assert libro.isbn == "ISBN001"
    assert libro.activo is True
    print(f"         -> {libro}")


test("Alta de libro (El principito)", test_alta_libro)


def test_alta_libro_2():
    libro = gestor_libros.alta_libro("1984", "George Orwell", "ISBN002", 1949, 328)
    assert libro is not None
    assert libro.titulo == "1984"
    print(f"         -> {libro}")


test("Alta de libro (1984)", test_alta_libro_2)


def test_alta_libro_isbn_duplicado():
    try:
        gestor_libros.alta_libro("Duplicado", "Autor", "ISBN001", 2000, 100)
        raise AssertionError("Debería haber lanzado ValueError por ISBN duplicado")
    except ValueError as e:
        print(f"         -> Rechazado correctamente: {e}")


test("Rechazo de alta con ISBN duplicado", test_alta_libro_isbn_duplicado)


def test_listado_libros():
    libros = gestor_libros.listar_libros()
    assert len(libros) == 2, f"Se esperaban 2 libros, hay {len(libros)}"
    for libro in libros:
        print(f"         -> {libro}")


test("Listado de libros", test_listado_libros)


def test_modificacion_libro():
    libro = gestor_libros.modificar_libro("ISBN001", titulo="El Principito (Edición Especial)")
    assert libro.titulo == "El Principito (Edición Especial)"
    print(f"         -> {libro}")


test("Modificación de libro", test_modificacion_libro)


def test_baja_libro():
    libro = gestor_libros.baja_libro("ISBN002")
    assert libro.activo is False
    print(f"         -> {libro}")


test("Baja de libro (1984)", test_baja_libro)


def test_listado_post_baja():
    libros = gestor_libros.listar_libros()
    activos = [l for l in libros if l.activo]
    inactivos = [l for l in libros if not l.activo]
    print(f"         -> Total: {len(libros)}, Activos: {len(activos)}, Inactivos: {len(inactivos)}")
    assert len(activos) == 1
    assert len(inactivos) == 1


test("Listado post-baja (activos vs inactivos)", test_listado_post_baja)


# ========== GESTIÓN DE USUARIOS ==========
print("\n===== GESTIÓN DE USUARIOS =====")


def test_alta_usuario():
    usuario = gestor_usuarios.alta_usuario("Juan", "Pérez", "12345678", "juan@email.com", "normal")
    assert usuario is not None
    assert usuario.dni == "12345678"
    assert usuario.activo is True
    print(f"         -> {usuario}")


test("Alta de usuario (Juan)", test_alta_usuario)


def test_alta_usuario_2():
    usuario = gestor_usuarios.alta_usuario("Ana", "Gómez", "87654321", "ana@email.com", "docente")
    assert usuario is not None
    print(f"         -> {usuario}")


test("Alta de usuario (Ana, docente)", test_alta_usuario_2)


def test_alta_usuario_dni_duplicado():
    try:
        gestor_usuarios.alta_usuario("Otro", "User", "12345678", "otro@email.com", "normal")
        raise AssertionError("Debería haber lanzado ValueError por DNI duplicado")
    except ValueError as e:
        print(f"         -> Rechazado correctamente: {e}")


test("Rechazo de alta con DNI duplicado", test_alta_usuario_dni_duplicado)


def test_listado_usuarios():
    usuarios = gestor_usuarios.listar_usuarios()
    assert len(usuarios) == 2
    for u in usuarios:
        print(f"         -> {u}")


test("Listado de usuarios", test_listado_usuarios)


def test_modificacion_usuario():
    usuario = gestor_usuarios.modificar_usuario("12345678", nombre="Juan Carlos")
    assert usuario.nombre == "Juan Carlos"
    print(f"         -> {usuario}")


test("Modificación de usuario", test_modificacion_usuario)


def test_baja_usuario():
    # Creamos un usuario extra para dar de baja sin afectar las pruebas de préstamos
    gestor_usuarios.alta_usuario("Carlos", "López", "99999999", "carlos@email.com", "normal")
    usuario = gestor_usuarios.baja_usuario("99999999")
    assert usuario.activo is False
    print(f"         -> {usuario}")


test("Baja de usuario", test_baja_usuario)


# ========== GESTIÓN DE PRÉSTAMOS (PARTE CRÍTICA) ==========
print("\n===== GESTIÓN DE PRÉSTAMOS (PARTE CRÍTICA) =====")

# Reactivamos el libro ISBN002 para las pruebas de préstamos
libro_1984 = gestor_libros.buscar_por_isbn("ISBN002")
libro_1984.activar()


def test_prestamo_valido():
    libro = gestor_libros.buscar_por_isbn("ISBN001")
    usuario = gestor_usuarios.buscar_por_dni("12345678")
    prestamo = gestor_prestamos.registrar_prestamo(libro, usuario)
    assert prestamo is not None
    assert prestamo.es_activo() is True
    print(f"         -> {prestamo.mostrar_detalle()}")


test("Registrar préstamo con libro y usuario válidos", test_prestamo_valido)


def test_prestamo_libro_ya_prestado():
    """REGLA CRÍTICA: un libro con préstamo activo NO puede volver a prestarse."""
    libro = gestor_libros.buscar_por_isbn("ISBN001")
    usuario = gestor_usuarios.buscar_por_dni("87654321")
    try:
        gestor_prestamos.registrar_prestamo(libro, usuario)
        raise AssertionError(
            "¡¡¡ ERROR CRÍTICO !!! Se permitió prestar un libro que ya tiene "
            "préstamo activo. La regla de negocio NO está funcionando."
        )
    except ValueError as e:
        print(f"         -> Rechazado correctamente: {e}")


test("Rechazar préstamo de libro ya prestado (REGLA CRÍTICA)", test_prestamo_libro_ya_prestado)


def test_listar_prestamos_activos():
    activos = gestor_prestamos.listar_prestamos_activos()
    assert len(activos) >= 1
    for p in activos:
        print(f"         -> {p.mostrar_detalle()}")


test("Listar préstamos activos", test_listar_prestamos_activos)


def test_devolucion():
    prestamo = gestor_prestamos.devolver_prestamo_por_isbn("ISBN001")
    assert prestamo.es_activo() is False
    print(f"         -> {prestamo.mostrar_detalle()}")


test("Registrar devolución", test_devolucion)


def test_re_prestamo_post_devolucion():
    """Después de devolver, el mismo libro DEBE poder volver a prestarse."""
    libro = gestor_libros.buscar_por_isbn("ISBN001")
    usuario = gestor_usuarios.buscar_por_dni("87654321")
    prestamo = gestor_prestamos.registrar_prestamo(libro, usuario)
    assert prestamo is not None
    assert prestamo.es_activo() is True
    print(f"         -> {prestamo.mostrar_detalle()}")


test("Re-prestar libro después de devolución", test_re_prestamo_post_devolucion)


# ========== PRUEBAS ADICIONALES ==========
print("\n===== PRUEBAS ADICIONALES =====")


def test_prestamo_libro_inactivo():
    """Un libro dado de baja no debería poder prestarse."""
    libro_baja = gestor_libros.buscar_por_isbn("ISBN002")
    libro_baja.desactivar()
    usuario = gestor_usuarios.buscar_por_dni("12345678")
    try:
        gestor_prestamos.registrar_prestamo(libro_baja, usuario)
        raise AssertionError("Se permitió prestar un libro inactivo")
    except ValueError as e:
        print(f"         -> Rechazado correctamente: {e}")


test("Rechazar préstamo de libro inactivo", test_prestamo_libro_inactivo)


def test_prestamo_usuario_inactivo():
    """Un usuario dado de baja no debería poder pedir préstamos."""
    libro_baja = gestor_libros.buscar_por_isbn("ISBN002")
    libro_baja.activar()  # reactivamos libro
    usuario_baja = gestor_usuarios.buscar_por_dni("99999999")
    try:
        gestor_prestamos.registrar_prestamo(libro_baja, usuario_baja)
        raise AssertionError("Se permitió prestar a un usuario inactivo")
    except ValueError as e:
        print(f"         -> Rechazado correctamente: {e}")


test("Rechazar préstamo a usuario inactivo", test_prestamo_usuario_inactivo)


def test_devolucion_inexistente():
    """Devolver un ISBN que no tiene préstamo activo debe fallar."""
    try:
        gestor_prestamos.devolver_prestamo_por_isbn("ISBN_NO_EXISTE")
        raise AssertionError("Se aceptó una devolución de ISBN inexistente")
    except ValueError as e:
        print(f"         -> Rechazado correctamente: {e}")


test("Rechazar devolución de ISBN sin préstamo activo", test_devolucion_inexistente)


def test_strategy_dias_normal():
    from patron_diseno import obtener_estrategia_por_usuario, EstrategiaPrestamoNormal
    usuario = gestor_usuarios.buscar_por_dni("12345678")  # tipo normal
    estrategia = obtener_estrategia_por_usuario(usuario)
    assert isinstance(estrategia, EstrategiaPrestamoNormal)
    assert estrategia.obtener_dias_maximos() == 15
    print(f"         -> Usuario normal: {estrategia.obtener_dias_maximos()} días")


test("Strategy: usuario normal -> 15 días", test_strategy_dias_normal)


def test_strategy_dias_docente():
    from patron_diseno import obtener_estrategia_por_usuario, EstrategiaPrestamoDocente
    usuario = gestor_usuarios.buscar_por_dni("87654321")  # tipo docente
    estrategia = obtener_estrategia_por_usuario(usuario)
    assert isinstance(estrategia, EstrategiaPrestamoDocente)
    assert estrategia.obtener_dias_maximos() == 30
    print(f"         -> Usuario docente: {estrategia.obtener_dias_maximos()} días")


test("Strategy: usuario docente -> 30 días", test_strategy_dias_docente)


def test_polimorfismo_mostrar_detalle():
    """Libro, Usuario y Prestamo deben tener su propio mostrar_detalle()."""
    libro = gestor_libros.buscar_por_isbn("ISBN001")
    usuario = gestor_usuarios.buscar_por_dni("12345678")
    prestamos = gestor_prestamos.listar_prestamos()

    detalle_libro = libro.mostrar_detalle()
    detalle_usuario = usuario.mostrar_detalle()
    detalle_prestamo = prestamos[0].mostrar_detalle()

    assert "ISBN" in detalle_libro
    assert "DNI" in detalle_usuario
    assert "Préstamo" in detalle_prestamo

    print(f"         -> Libro: {detalle_libro}")
    print(f"         -> Usuario: {detalle_usuario}")
    print(f"         -> Préstamo: {detalle_prestamo}")


test("Polimorfismo: mostrar_detalle() en Libro, Usuario, Prestamo", test_polimorfismo_mostrar_detalle)


def test_metaclase():
    """Verificar que MetaEntidad obliga a implementar validar()."""
    from metaclases import MetaEntidad
    from entidad import Entidad
    assert type(Entidad) is MetaEntidad
    assert type(gestor_libros.buscar_por_isbn("ISBN001").__class__) is MetaEntidad
    print(f"         -> type(Entidad) = {type(Entidad)}")
    print(f"         -> type(Libro) = {type(gestor_libros.buscar_por_isbn('ISBN001').__class__)}")

    # Intentar crear una clase sin validar() debería fallar
    try:
        class ClaseSinValidar(Entidad):
            pass
        raise AssertionError("MetaEntidad debería haber rechazado una clase sin validar()")
    except TypeError as e:
        print(f"         -> MetaEntidad rechazó correctamente clase sin validar(): {e}")


test("Metaclase: MetaEntidad obliga a implementar validar()", test_metaclase)


# ========== RESUMEN ==========
print("\n" + "=" * 50)
print(f"RESUMEN: {ok}/{total} tests pasaron, {fail} fallaron")
print("=" * 50)

if fail > 0:
    print("\nTests que fallaron:")
    for r in resultados:
        if r[0] == "FAIL":
            print(f"  - {r[1]}: {r[2]}")
