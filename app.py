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

MENU_OPCIONES = [
    ('1', 'Registrar Abono'),
    ('2', 'Registrar Gasto'),
    ('3', 'Gestionar Categorías (Añadir/Eliminar)'),
    ('4', 'Asignar Monto a Categoría'),
    ('5', 'Borrar Asignacion'),
    ('6', 'Salir'),
    ('7', 'Borrar presupuesto'),
]
SUBMENU_CATEGORIAS = [
    'Añadir categoría',
    'Eliminar categoría',
]

SI_NO = [
    'SI',
    'NO',
]

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def leer_tecla_menu():
    if os.name == 'nt':
        import msvcrt
        tecla = msvcrt.getch()
        if tecla in (b'\x00', b'\xe0'):
            especial = msvcrt.getch()
            if especial == b'H':
                return 'UP'
            if especial == b'P':
                return 'DOWN'
            return ''
        if tecla == b'\r':
            return 'ENTER'
        return tecla.decode('utf-8', errors='ignore').lower()
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        config_anterior = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            tecla = sys.stdin.read(1)
            if tecla == '\x1b':
                seq = sys.stdin.read(2)
                if seq == '[A':
                    return 'UP'
                if seq == '[B':
                    return 'DOWN'
                return ''
            if tecla in ('\r', '\n'):
                return 'ENTER'
            return tecla.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, config_anterior)

def mostrar_menu(p, seleccion):
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
    print("Usa flechas ↑/↓ y Enter para seleccionar")
    for i, (clave, texto) in enumerate(MENU_OPCIONES):
        if i == seleccion:
            print(f"{Color.AMARILLO}> [{clave}] {texto}{Color.FIN}")
        else:
            print(f"  [{clave}] {texto}")
    print("-" * 30)

def leer_opcion_menu(p):
    indice = 0
    while True:
        mostrar_menu(p, indice)
        tecla = leer_tecla_menu()

        if tecla == 'UP':
            indice = (indice - 1) % len(MENU_OPCIONES)
        elif tecla == 'DOWN':
            indice = (indice + 1) % len(MENU_OPCIONES)
        elif tecla == 'ENTER':
            return MENU_OPCIONES[indice][0]
        elif tecla in {op[0] for op in MENU_OPCIONES}:
            return tecla

def seleccionar_con_flechas(titulo, opciones, incluir_volver=True):
    opciones_menu = list(opciones)
    if incluir_volver:
        opciones_menu.append("Volver")
    if not opciones_menu:
        return None

    indice = 0
    while True:
        limpiar_pantalla()
        print(f"{Color.AZUL}{Color.NEGRILLA}{titulo}{Color.FIN}")
        print("-" * 30)
        print("Usa flechas ↑/↓ y Enter para seleccionar")
        for i, opcion in enumerate(opciones_menu):
            if i == indice:
                print(f"{Color.AMARILLO}> {opcion}{Color.FIN}")
            else:
                print(f"  {opcion}")
        print("-" * 30)

        tecla = leer_tecla_menu()
        if tecla == 'UP':
            indice = (indice - 1) % len(opciones_menu)
        elif tecla == 'DOWN':
            indice = (indice + 1) % len(opciones_menu)
        elif tecla == 'ENTER':
            seleccion = opciones_menu[indice]
            if seleccion == "Volver":
                return None
            return seleccion

def main():
    # Inicializar la lógica de tu model.py
    p = presupuesto(0)
    p.cargar()

    while True:
        opcion = leer_opcion_menu(p)

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
            categorias = list(p.categorias.keys())
            cat = seleccionar_con_flechas("Selecciona categoría del gasto", categorias)
            if cat is None:
                continue
            try:
                monto = int(input("Monto del gasto: "))
                p.registrar_gasto(cat, monto)
                p.guardar()
                time.sleep(1)
            except ValueError:
                print(f"{Color.ROJO}Monto inválido.{Color.FIN}")
                time.sleep(2)

        elif opcion == '3':
            sub = seleccionar_con_flechas("Gestionar categorías", SUBMENU_CATEGORIAS)
            if sub is None:
                continue
            if sub == 'Añadir categoría':
                nombre = input("Nombre de la categoría: ").capitalize()
                p.agregar_categoria(nombre)
            elif sub == 'Eliminar categoría':
                categorias = [cat for cat in p.categorias.keys() if cat != "Ahorro"]
                nombre = seleccionar_con_flechas("Selecciona categoría a eliminar", categorias)
                if nombre is None:
                    continue
                p.eliminar_categoria(nombre)
            p.guardar()

        elif opcion == '4':
            categorias = list(p.categorias.keys())
            cat = seleccionar_con_flechas("Selecciona categoría para asignar monto", categorias)
            if cat is None:
                continue
            try:
                monto = int(input("Monto a asignar: "))
                p.asignar_monto(cat, monto)
                p.guardar()
            except ValueError:
                print(f"{Color.ROJO}Error en el monto.{Color.FIN}")
                time.sleep(2)
        
        elif opcion == '5':
            categorias = list(p.categorias.keys())
            cat = seleccionar_con_flechas("Selecciona categoría para borrar asignación", categorias)
            if cat is None:
                continue
            try:
                p.borrar_asignaciones_categoria(cat)
                p.guardar()
            except ValueError:
                print(f"Categoria {cat} no existe")
                time.sleep(2)


        elif opcion == '6':
            print(f"{Color.AZUL}¡Guardado! Saliendo...{Color.FIN}")
            p.guardar()
            break

        elif opcion == '7':
            sub = seleccionar_con_flechas("¿Esta seguro de seguir?", SI_NO)
            if sub == "SI":
                print(f"Borrando tu presupuesto por completo\n")
                time.sleep(2)
                p.nuke_json()
                time.sleep(2)
                print("Reinicie app para volver a usar\n")
                time.sleep(2)
                break
            elif sub == "NO":
                True  
        else:
            print(f"{Color.ROJO}Opción no válida.{Color.FIN}")
            time.sleep(1)

if __name__ == "__main__":
    main()
