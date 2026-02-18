import json
import time
from pathlib import Path

class presupuesto():
    def __init__(self, monto_total):
        self.monto_total = int(monto_total)
        self.categorias = {
            "Ahorro": 0,
        }

    def registrar_abono(self, monto):
        self.monto_total += monto


    def registrar_gasto(self, cat, monto):
        if self.monto_total >= monto:
            if cat in self.categorias:
                self.categorias[cat] -= monto
                self.monto_total -= monto
                print(f"Gastaste ${monto} en {cat}")
                if self.categorias[cat] < monto:
                    resto = {monto - self.categorias[cat]}
                    print(f"Superaste tus gastos esperados para {cat}")
                    print(f"Se retiraran ${resto} de tu cuenta de ahorros")
                    self.categorias[cat] += resto
                    self.categorias["Ahorro"] -= resto
            else:
                print(f"La categoria {cat} no existe")
        else:
            print("No posee saldo suficiente en su cuenta")
            time.sleep(3)

    def ver_presupuesto_categoria(self, cat):
        print(f"Para {cat} le queda un presupuesto de {self.categorias[cat]}\n")

    def ver_presupuesto_total(self):
        print(f"Te queda un total de ${self.monto_total}")

    def agregar_categoria(self, cat):
        if cat not in self.categorias:
            self.categorias[cat]=0
        else:
            print(f"Categoria {cat} ya existe")

    def eliminar_categoria(self, cat):
        if cat in self.categorias:
            if cat != "Ahorro":
                del self.categorias[cat]
            else:
                print(f"Categoria {cat}, se encuentra protegida")
                time.sleep(2)
        else:
            print("Categoria no existe")
            time.sleep(2)
    
    def asignar_monto(self, cat, monto):
        if monto <= self.monto_libre():
            if cat in self.categorias:
                self.categorias[cat] = monto
                
            else:
                print("Categoria Inexistente")
        else:
            print("No posees ese monto disponible")
            time.sleep(3)
            
    def cargar(self):
        try:
            with open("presupuesto.json", "r") as archivo:
                datos = json.load(archivo)
                self.monto_total = datos["monto_total"]
                self.categorias = datos["categorias"]
        except FileNotFoundError:
            print("No hay presupuesto guardado, se usará uno nuevo.")
    
    def guardar(self):
        datos = {
            "monto_total": self.monto_total,
            "categorias": self.categorias
        }
        with open("presupuesto.json", "w") as archivo:
            json.dump(datos, archivo)
    
    def monto_libre(self):
        suma_asignada = 0
        for x in self.categorias:
            suma_asignada += self.categorias[x]
        monto_libre = self.monto_total - suma_asignada
        return monto_libre
    
    def borrar_asignaciones_categoria(self, cat):
        if cat in self.categorias:
            self.categorias[cat] = 0
        else:
            print(f"Categoria {cat} no existe")
    
    def nuke_json(self):
        ruta = Path("presupuesto.json")
        if ruta.exists() and ruta.is_file():
            ruta.unlink()
        else:
            print("ERROR\n")






