# Gestor de Presupuesto en Consola

Aplicación de terminal en Python para administrar un presupuesto personal por categorías, con navegación por teclado (`↑/↓` + `Enter`) y persistencia en `presupuesto.json`.

## Características

- Registro de abonos al saldo total.
- Registro de gastos por categoría.
- Creación y eliminación de categorías.
- Asignación de monto por categoría.
- Borrado de asignación de una categoría.
- Eliminación completa del presupuesto guardado.
- Menús navegables con flechas del teclado.
- Opción `Volver` en submenús de selección.

## Requisitos

- Python 3.8+ (recomendado 3.10 o superior).
- Terminal compatible con secuencias ANSI.
  - Linux/macOS: soportado por `termios`/`tty`.
  - Windows: soportado con `msvcrt`.

## Estructura del proyecto

```text
.
├── app.py            # Interfaz de consola, menús y flujo principal
├── model.py          # Lógica de negocio y persistencia
└── presupuesto.json  # Datos guardados (se crea automáticamente)
```

## Cómo ejecutar

Desde la carpeta del proyecto:

```bash
python app.py
```

## Controles de teclado

### Menú principal

- `↑/↓`: mover selección.
- `Enter`: confirmar opción.
- También puedes usar números `1..7` como acceso rápido.

Opciones:

1. Registrar Abono
2. Registrar Gasto
3. Gestionar Categorías (Añadir/Eliminar)
4. Asignar Monto a Categoría
5. Borrar Asignación
6. Salir
7. Borrar presupuesto

### Submenús

- En cada selector con flechas existe la opción `Volver`.
- `Volver` cancela la acción actual y regresa al paso anterior.

## Flujo de uso recomendado

1. Ejecutar la app.
2. Registrar abonos para definir el saldo total.
3. Crear categorías además de `Ahorro`.
4. Asignar montos por categoría.
5. Registrar gastos seleccionando la categoría.
6. Salir para guardar y cerrar.

## Persistencia de datos

La aplicación guarda estado en `presupuesto.json` con este formato:

```json
{
  "monto_total": 120000,
  "categorias": {
    "Ahorro": 30000,
    "Comida": 25000,
    "Transporte": 15000
  }
}
```

Carga y guardado:

- Al iniciar, `model.py` intenta cargar `presupuesto.json`.
- Si no existe, inicia un presupuesto nuevo.
- En cada operación relevante se vuelve a guardar.

## Reglas actuales del dominio

- La categoría `Ahorro` existe por defecto.
- `Ahorro` no se puede eliminar.
- Un gasto descuenta del `monto_total` y de la categoría elegida.
- Si no hay saldo suficiente para un gasto, se rechaza.

## Archivos clave

- `app.py`: interfaz y navegación del usuario.
- `model.py`: clase `presupuesto` y reglas de negocio.

## Notas y mejoras pendientes

- Actualmente se usan `int` para montos; no hay decimales.
- Faltan validaciones extra (por ejemplo, montos negativos).
- No hay tests automatizados todavía.
- Se puede mejorar el manejo de errores y mensajes en algunos flujos.

## Ideas de siguientes pasos

- Agregar reporte mensual y resumen por categoría.
