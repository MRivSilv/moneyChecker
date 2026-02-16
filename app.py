import os
import sys
import time
from model import presupuesto

# Colores para la terminal
class Color:
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    ROJO = '\033[91m'
    AMARILLO = '\033[93m'
    NEGRILLA = '\033[1m'
    FIN = '\033[0m'

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu(p):
    limpiar_pantalla()
    print(f"{Color.AZUL}{Color.NEGRILLA}=== GESTOR DE PRESUPUESTO ==={Color.FIN}")
    print(f"Saldo Total: {Color.VERDE}${p.monto_total}{Color.FIN}")
    print(f"Saldo sin asignar: {Color.AZUL}${p.monto_libre()}{Color.FIN}")
    print("-" * 30)
    
    # Mostrar categorías
    if p.categorias:
        print(f"{Color.NEGRILLA}Categorías:{Color.FIN}")
        for cat, monto in p.categorias.items():
            color_cat = Color.VERDE if monto >= 0 else Color.ROJO
            print(f" • {cat.capitalize()}: {color_cat}${monto}{Color.FIN}")
    else:
        print(f"{Color.AMARILLO}No hay categorías registradas.{Color.FIN}")
    
    print("-" * 30)
    print("1. Registrar Abono")
    print("2. Registrar Gasto")
    print("3. Gestionar Categorías (Añadir/Eliminar)")
    print("4. Asignar Monto a Categoría")
    print("4. Borrar Asignacion")
    print("5. Salir")
    print("-" * 30)

def main():
    # Inicializar la lógica de tu model.py
    p = presupuesto(0)
    p.cargar()

    while True:
        mostrar_menu(p)
        opcion = input(f"{Color.AMARILLO}Selecciona una opción: {Color.FIN}")

        if opcion == '1':
            try:
                monto = int(input("Monto del abono: "))
                p.registrar_abono(monto)
                p.guardar()
                print(f"{Color.VERDE}¡Abono registrado!{Color.FIN}")
                time.sleep(1)
            except ValueError:
                print(f"{Color.ROJO}Error: Ingresa un número válido.{Color.FIN}")
                time.sleep(2)

        elif opcion == '2':
            cat = input("Categoría del gasto: ").lower()
            try:
                monto = int(input("Monto del gasto: "))
                p.registrar_gasto(cat, monto)
                p.guardar()
                time.sleep(1)
            except ValueError:
                print(f"{Color.ROJO}Monto inválido.{Color.FIN}")
                time.sleep(2)

        elif opcion == '3':
            print("\n1. Añadir categoría\n2. Eliminar categoría")
            sub = input("Selecciona: ")
            nombre = input("Nombre de la categoría: ").lower()
            if sub == '1':
                p.agregar_categoria(nombre)
            elif sub == '2':
                p.eliminar_categoria(nombre)
            p.guardar()

        elif opcion == '4':
            cat = input("Categoría: ").lower()
            try:
                monto = int(input("Monto a asignar: "))
                p.asignar_monto(cat, monto)
                p.guardar()
            except ValueError:
                print(f"{Color.ROJO}Error en el monto.{Color.FIN}")
                time.sleep(2)

        elif opcion == '5':
            print(f"{Color.AZUL}¡Guardado! Saliendo...{Color.FIN}")
            p.guardar()
            break
        
        else:
            print(f"{Color.ROJO}Opción no válida.{Color.FIN}")
            time.sleep(1)

if __name__ == "__main__":
    main()