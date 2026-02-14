import json

class presupuesto():
    def __init__(self, monto_total):
        self.monto_total = monto_total
        self.categorias = {
        }

    def registrar_abono(self, monto):
        self.monto_total += monto

    def registrar_gasto(self, cat, monto):
        if cat in self.categorias:
            self.categorias[cat] -= monto
            self.monto_total -= monto
            print(f"Gastaste ${monto} en {cat}")
        else:
            print(f"La categoria {cat} no existe")

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
            del self.categorias[cat]
        else:
            print("Categoria no existe")
    
    def asignar_monto(self, cat, monto):
        if cat in self.categorias:
            self.categorias[cat] = monto
            if (cat.lower() == "ahorro"):
                self.monto_total -= monto
        else:
            print("Categoria Inexistente")
            
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





