import customtkinter as ctk
from model import presupuesto

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

p = presupuesto(0)
p.cargar()

app = ctk.CTk()
app.geometry("1000x650")
app.title("Gestor de Presupuesto")

# ---------------- CONFIG GRID ---------------- #

app.grid_columnconfigure((0, 1, 2), weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(3, weight=1)

# ---------------- FUNCIONES ---------------- #

def actualizar_total():
    label_total.configure(text=f"Total disponible: ${p.monto_total}")

def actualizar_lista():
    lista_categorias.delete("0.0", "end")
    for cat, monto in p.categorias.items():
        lista_categorias.insert("end", f"{cat}: ${monto}\n")

def registrar_abono():
    try:
        monto = float(entry_abono.get())
        p.registrar_abono(monto)
        entry_abono.delete(0, "end")
        actualizar_total()
    except:
        pass

def registrar_gasto():
    cat = entry_gasto_cat.get().strip().lower()
    try:
        monto = float(entry_gasto_monto.get())
        p.registrar_gasto(cat, monto)
        entry_gasto_monto.delete(0, "end")
        actualizar_total()
        actualizar_lista()
    except:
        pass

def agregar_categoria():
    cat = entry_categoria.get().strip().lower()
    if cat:
        p.agregar_categoria(cat)
        entry_categoria.delete(0, "end")
        actualizar_lista()

def eliminar_categoria():
    cat = entry_categoria.get().strip().lower()
    p.eliminar_categoria(cat)
    entry_categoria.delete(0, "end")
    actualizar_lista()

def asignar_monto_categoria():
    cat = entry_categoria.get().strip().lower()
    try:
        monto = float(entry_asignar_monto.get())
        p.asignar_monto(cat, monto)
        entry_asignar_monto.delete(0, "end")
        actualizar_total()
        actualizar_lista()
    except:
        pass

def cerrar_app():
    p.guardar()
    app.destroy()

# ---------------- TITULO ---------------- #

titulo = ctk.CTkLabel(app, text="GESTOR DE PRESUPUESTO", font=("Arial", 24))
titulo.grid(row=0, column=0, columnspan=3, pady=20)

# ---------------- COLUMNA 1 - ABONO ---------------- #

frame_abono = ctk.CTkFrame(app)
frame_abono.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

ctk.CTkLabel(frame_abono, text="Registrar Abono", font=("Arial", 18)).pack(pady=15)

entry_abono = ctk.CTkEntry(frame_abono, placeholder_text="Monto")
entry_abono.pack(pady=10)

ctk.CTkButton(frame_abono, text="Agregar", command=registrar_abono).pack(pady=10)

# ---------------- COLUMNA 2 - GASTO ---------------- #

frame_gasto = ctk.CTkFrame(app)
frame_gasto.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

ctk.CTkLabel(frame_gasto, text="Registrar Gasto", font=("Arial", 18)).pack(pady=15)

entry_gasto_cat = ctk.CTkEntry(frame_gasto, placeholder_text="Categoria")
entry_gasto_cat.pack(pady=5)

entry_gasto_monto = ctk.CTkEntry(frame_gasto, placeholder_text="Monto")
entry_gasto_monto.pack(pady=5)

ctk.CTkButton(frame_gasto, text="Registrar", command=registrar_gasto).pack(pady=10)

# ---------------- COLUMNA 3 - CATEGORIAS ---------------- #

frame_categoria = ctk.CTkFrame(app)
frame_categoria.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")

ctk.CTkLabel(frame_categoria, text="Categorias", font=("Arial", 18)).pack(pady=15)

entry_categoria = ctk.CTkEntry(frame_categoria, placeholder_text="Nombre categoria")
entry_categoria.pack(pady=5)

ctk.CTkButton(frame_categoria, text="Agregar", command=agregar_categoria).pack(pady=5)
ctk.CTkButton(frame_categoria, text="Eliminar", command=eliminar_categoria).pack(pady=5)

entry_asignar_monto = ctk.CTkEntry(frame_categoria, placeholder_text="Monto a asignar")
entry_asignar_monto.pack(pady=10)

ctk.CTkButton(frame_categoria, text="Asignar Monto", command=asignar_monto_categoria).pack(pady=5)

# ---------------- INFO INFERIOR ---------------- #

label_total = ctk.CTkLabel(app, text="", font=("Arial", 20))
label_total.grid(row=2, column=0, columnspan=3, pady=10)

lista_categorias = ctk.CTkTextbox(app, height=150)
lista_categorias.grid(row=3, column=0, columnspan=3, padx=40, pady=10, sticky="nsew")

# ---------------- BOTON SALIR ---------------- #

ctk.CTkButton(app, text="Guardar y Salir", command=cerrar_app).grid(
    row=4, column=0, columnspan=3, pady=15
)

# ---------------- INIT ---------------- #

actualizar_total()
actualizar_lista()

app.protocol("WM_DELETE_WINDOW", cerrar_app)
app.mainloop()
