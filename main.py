"""
Sistema de Gestión de Biblioteca Digital.

Este archivo pertenece al Módulo C. Contiene un menú de consola simple para
usar los gestores de libros, usuarios y préstamos.
"""

import os
import sys

# Se agrega la carpeta src al path para poder importar los módulos del proyecto
# cuando el programa se ejecuta desde la raíz del repositorio.
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_SRC = os.path.join(RUTA_BASE, "src")
sys.path.append(RUTA_SRC)

from gestores import GestorLibros, GestorUsuarios, GestorPrestamos


def leer_entero(mensaje):
    """Pide un número entero por consola y valida que sea correcto."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero.")


def mostrar_lista(elementos, mensaje_vacio):
    """Muestra una lista de elementos usando su representación en texto."""
    if not elementos:
        print(mensaje_vacio)
        return

    for elemento in elementos:
        print("-", elemento)


def menu_libros(gestor_libros):
    """Submenú para administrar libros."""
    while True:
        print()
        print("--- Gestión de libros ---")
        print("1. Alta de libro")
        print("2. Modificar libro")
        print("3. Baja de libro")
        print("4. Listar libros")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                titulo = input("Título: ")
                autor = input("Autor: ")
                isbn = input("ISBN: ")
                anio = leer_entero("Año de publicación: ")
                paginas = leer_entero("Cantidad de páginas: ")

                libro = gestor_libros.alta_libro(titulo, autor, isbn, anio, paginas)
                print("Libro creado correctamente:")
                print(libro)

            elif opcion == "2":
                isbn = input("ISBN del libro a modificar: ")
                print("Deje vacío el dato que no quiera modificar.")
                titulo = input("Nuevo título: ")
                autor = input("Nuevo autor: ")
                anio = input("Nuevo año de publicación: ")
                paginas = input("Nueva cantidad de páginas: ")

                libro = gestor_libros.modificar_libro(isbn, titulo, autor, anio, paginas)
                print("Libro modificado correctamente:")
                print(libro)

            elif opcion == "3":
                isbn = input("ISBN del libro a dar de baja: ")
                libro = gestor_libros.baja_libro(isbn)
                print("Libro dado de baja correctamente:")
                print(libro)

            elif opcion == "4":
                mostrar_lista(gestor_libros.listar_libros(), "No hay libros registrados.")

            elif opcion == "0":
                break

            else:
                print("Opción inválida.")

        except ValueError as error:
            print(f"Error: {error}")


def menu_usuarios(gestor_usuarios):
    """Submenú para administrar usuarios."""
    while True:
        print()
        print("--- Gestión de usuarios ---")
        print("1. Alta de usuario")
        print("2. Modificar usuario")
        print("3. Baja de usuario")
        print("4. Listar usuarios")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                dni = input("DNI: ")
                correo = input("Correo electrónico: ")
                tipo_usuario = input("Tipo de usuario (normal/docente/investigador): ")

                if not tipo_usuario:
                    tipo_usuario = "normal"

                usuario = gestor_usuarios.alta_usuario(
                    nombre, apellido, dni, correo, tipo_usuario
                )
                print("Usuario creado correctamente:")
                print(usuario)

            elif opcion == "2":
                dni = input("DNI del usuario a modificar: ")
                print("Deje vacío el dato que no quiera modificar.")
                nombre = input("Nuevo nombre: ")
                apellido = input("Nuevo apellido: ")
                correo = input("Nuevo correo electrónico: ")
                tipo_usuario = input("Nuevo tipo de usuario: ")

                usuario = gestor_usuarios.modificar_usuario(
                    dni, nombre, apellido, correo, tipo_usuario
                )
                print("Usuario modificado correctamente:")
                print(usuario)

            elif opcion == "3":
                dni = input("DNI del usuario a dar de baja: ")
                usuario = gestor_usuarios.baja_usuario(dni)
                print("Usuario dado de baja correctamente:")
                print(usuario)

            elif opcion == "4":
                mostrar_lista(gestor_usuarios.listar_usuarios(), "No hay usuarios registrados.")

            elif opcion == "0":
                break

            else:
                print("Opción inválida.")

        except ValueError as error:
            print(f"Error: {error}")


def menu_prestamos(gestor_libros, gestor_usuarios, gestor_prestamos):
    """Submenú para administrar préstamos y devoluciones."""
    while True:
        print()
        print("--- Gestión de préstamos ---")
        print("1. Registrar préstamo")
        print("2. Registrar devolución")
        print("3. Listar préstamos activos")
        print("4. Listar todos los préstamos")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                isbn = input("ISBN del libro: ")
                dni = input("DNI del usuario: ")

                libro = gestor_libros.buscar_por_isbn(isbn)
                usuario = gestor_usuarios.buscar_por_dni(dni)

                prestamo = gestor_prestamos.registrar_prestamo(libro, usuario)
                print("Préstamo registrado correctamente:")
                print(prestamo.mostrar_detalle())

            elif opcion == "2":
                isbn = input("ISBN del libro a devolver: ")
                prestamo = gestor_prestamos.devolver_prestamo_por_isbn(isbn)
                print("Devolución registrada correctamente:")
                print(prestamo.mostrar_detalle())

            elif opcion == "3":
                prestamos = gestor_prestamos.listar_prestamos_activos()
                if not prestamos:
                    print("No hay préstamos activos.")
                else:
                    for prestamo in prestamos:
                        print("-", prestamo.mostrar_detalle())

            elif opcion == "4":
                prestamos = gestor_prestamos.listar_prestamos()
                if not prestamos:
                    print("No hay préstamos registrados.")
                else:
                    for prestamo in prestamos:
                        print("-", prestamo.mostrar_detalle())

            elif opcion == "0":
                break

            else:
                print("Opción inválida.")

        except ValueError as error:
            print(f"Error: {error}")


def cargar_datos_de_prueba(gestor_libros, gestor_usuarios):
    """
    Carga algunos datos iniciales para probar el sistema más rápido.

    Esto no reemplaza las altas del menú, solo facilita la demostración.
    """
    gestor_libros.alta_libro("El principito", "Antoine de Saint-Exupéry", "ISBN001", 1943, 96)
    gestor_libros.alta_libro("1984", "George Orwell", "ISBN002", 1949, 328)

    gestor_usuarios.alta_usuario("Juan", "Pérez", "12345678", "juan@email.com", "normal")
    gestor_usuarios.alta_usuario("Ana", "Gómez", "87654321", "ana@email.com", "docente")


def main():
    """Función principal del programa."""
    gestor_libros = GestorLibros()
    gestor_usuarios = GestorUsuarios()
    gestor_prestamos = GestorPrestamos()

    cargar_datos_de_prueba(gestor_libros, gestor_usuarios)

    while True:
        print()
        print("===== Biblioteca Digital =====")
        print("1. Gestión de libros")
        print("2. Gestión de usuarios")
        print("3. Gestión de préstamos")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_libros(gestor_libros)
        elif opcion == "2":
            menu_usuarios(gestor_usuarios)
        elif opcion == "3":
            menu_prestamos(gestor_libros, gestor_usuarios, gestor_prestamos)
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
