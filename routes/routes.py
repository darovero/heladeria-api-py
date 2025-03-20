from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models.db import db
from models.producto import Producto
from models.ingredientes import Ingrediente
from models.heladeria import Heladeria
from models.user import User  # 🔹 Se agrega la importación del modelo User

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def home():
    """Carga la lista de productos y muestra la página de inicio."""
    productos = Producto.query.all()

    if not productos:
        return "⚠ No hay productos disponibles.", 500

    return render_template("index.html", productos=productos)

@app_routes.route('/welcome')
@login_required
def welcome():
    """Página de bienvenida después del inicio de sesión."""
    return render_template("welcome.html", username=current_user.username)

@app_routes.route('/vender/<int:producto_id>')
def vender_producto(producto_id):
    """Intenta vender un producto y maneja los errores si faltan ingredientes."""
    heladeria = Heladeria.query.first()
    
    if not heladeria:
        return jsonify({"error": "No hay datos en la base de datos"}), 500

    producto = Producto.query.get(producto_id)
    
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    if not producto.ingredientes:
        return jsonify({"mensaje": "Este producto no tiene ingredientes asociados"}), 400

    try:
        resultado = producto.vender()
        return jsonify({"mensaje": resultado}), 200
    except ValueError as error:
        return jsonify({"mensaje": f"¡Oh no! Nos hemos quedado sin {error}"}), 400

def cargar_datos_iniciales():
    """Carga los datos de usuarios, ingredientes y productos en la base de datos."""
    with db.session.no_autoflush:

        # 🔹 Verificar si ya existe una heladería antes de crear una nueva
        heladeria = Heladeria.query.first()
        if not heladeria:
            heladeria = Heladeria(nombre="Heladería del Proyecto", ubicacion="Centro")
            db.session.add(heladeria)
            db.session.commit()

        # 🔹 Verificar si existen ingredientes antes de agregarlos
        if not Ingrediente.query.first():
            ingredientes = [
                Ingrediente(nombre="Fresa", precio=500, calorias=30, stock=10, heladeria_id=heladeria.id),
                Ingrediente(nombre="Vainilla", precio=600, calorias=40, stock=10, heladeria_id=heladeria.id),
                Ingrediente(nombre="Chocolate", precio=700, calorias=50, stock=10, heladeria_id=heladeria.id),
                Ingrediente(nombre="Leche", precio=200, calorias=20, stock=10, heladeria_id=heladeria.id),
            ]
            db.session.bulk_save_objects(ingredientes)
            db.session.commit()

        # 🔹 Verificar si existen productos antes de agregarlos
        if not Producto.query.first():
            productos = [
                Producto(nombre='Copa Fresa', precio=7500, tipo='Copa', heladeria_id=heladeria.id),
                Producto(nombre='Copa Vainilla', precio=7200, tipo='Copa', heladeria_id=heladeria.id),
                Producto(nombre='Malteada Choco', precio=8500, tipo='Malteada', heladeria_id=heladeria.id),
                Producto(nombre='Malteada Vainilla', precio=8300, tipo='Malteada', heladeria_id=heladeria.id),
            ]
            db.session.bulk_save_objects(productos)
            db.session.commit()

        # 🔹 Verificar si hay usuarios en la base de datos antes de agregar
        if not User.query.first():
            usuarios = [
                User(username="admin", email="admin@example.com", password="admin123", es_admin=True, es_empleado=True),
                User(username="empleado1", email="empleado1@example.com", password="empleado123", es_admin=False, es_empleado=True),
                User(username="cliente1", email="cliente1@example.com", password="cliente123", es_admin=False, es_empleado=False),
            ]
            db.session.bulk_save_objects(usuarios)
            db.session.commit()
            print("✅ Usuarios iniciales creados correctamente.")

        # 🔹 Relacionar ingredientes con productos
        productos = Producto.query.all()
        ingredientes_dict = {ing.nombre: ing for ing in Ingrediente.query.all()}

        producto_ingredientes = {
            "Copa Fresa": ["Fresa", "Leche"],
            "Copa Vainilla": ["Vainilla", "Leche"],
            "Malteada Choco": ["Chocolate", "Leche"],
            "Malteada Vainilla": ["Vainilla", "Leche"]
        }

        for producto in productos:
            if producto.nombre in producto_ingredientes:
                for ing_nombre in producto_ingredientes[producto.nombre]:
                    ingrediente = ingredientes_dict.get(ing_nombre)
                    if ingrediente and ingrediente not in producto.ingredientes:
                        producto.ingredientes.append(ingrediente)

        db.session.commit()
        print("✅ Carga de datos iniciales completada.")
