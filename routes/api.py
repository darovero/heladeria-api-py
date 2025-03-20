from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.db import db
from models.producto import Producto
from models.ingredientes import Ingrediente

api = Blueprint('api', __name__, url_prefix='/api')

# 📌 Obtener todos los productos (Accesible por todos)
@api.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'precio': p.precio,
        'tipo': p.tipo
    } for p in productos]), 200

# 📌 Obtener un producto por ID (Accesible por todos)
@api.route('/producto/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'tipo': producto.tipo
    }), 200

# 📌 Vender un producto (Solo Admins y Empleados)
@api.route('/producto/<int:id>/vender', methods=['POST'])
@login_required
def vender_producto(id):
    if not current_user.es_admin and not current_user.es_empleado:
        return jsonify({'error': 'Acceso no autorizado'}), 403

    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    try:
        resultado = producto.vender()
        return jsonify({'mensaje': resultado}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# 📌 Reabastecer un producto (Solo Admins)
@api.route('/producto/<int:id>/reabastecer', methods=['POST'])
@login_required
def reabastecer_producto(id):
    if not current_user.es_admin:
        return jsonify({'error': 'Acceso no autorizado'}), 403

    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    datos = request.get_json()
    cantidad = datos.get("cantidad", 5)

    if not isinstance(cantidad, int) or cantidad <= 0:
        return jsonify({'error': 'La cantidad debe ser un número entero positivo'}), 400

    try:
        for ingrediente in producto.ingredientes:
            ingrediente.stock += cantidad
        db.session.commit()
        return jsonify({'mensaje': f'El inventario de {producto.nombre} ha sido reabastecido en {cantidad} unidades'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 📌 Renovar inventario de un producto (Solo Admins)
@api.route('/producto/<int:id>/renovar_inventario', methods=['POST'])
@login_required
def renovar_inventario_producto(id):
    if not current_user.es_admin:
        return jsonify({'error': 'Acceso no autorizado'}), 403

    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    datos = request.get_json()
    cantidad = datos.get("cantidad", 10)

    if not isinstance(cantidad, int) or cantidad <= 0:
        return jsonify({'error': 'La cantidad debe ser un número entero positivo'}), 400

    try:
        for ingrediente in producto.ingredientes:
            ingrediente.stock = cantidad
        db.session.commit()
        return jsonify({'mensaje': f'El inventario de {producto.nombre} ha sido renovado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
