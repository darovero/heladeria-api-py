from flask import Blueprint, jsonify, request
from models.db import db
from models.producto import Producto
from models.ingredientes import Ingrediente

api = Blueprint('api', __name__, url_prefix='/api')

# 📌 Obtener todos los productos
@api.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'precio': p.precio,
        'tipo': p.tipo
    } for p in productos]), 200

# 📌 Obtener un producto por ID
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

# 📌 Obtener un producto por nombre
@api.route('/producto/nombre/<string:nombre>', methods=['GET'])
def obtener_producto_por_nombre(nombre):
    producto = Producto.query.filter_by(nombre=nombre).first()
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'tipo': producto.tipo
    }), 200

# 📌 Obtener calorías de un producto
@api.route('/producto/<int:id>/calorias', methods=['GET'])
def obtener_calorias_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({
        'id': producto.id,
        'calorias': producto.calorias_totales()
    }), 200

# 📌 Obtener rentabilidad de un producto
@api.route('/producto/<int:id>/rentabilidad', methods=['GET'])
def obtener_rentabilidad_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({
        'id': producto.id,
        'rentabilidad': producto.calcular_rentabilidad()
    }), 200

# 📌 Obtener costo de producción de un producto
@api.route('/producto/<int:id>/costo', methods=['GET'])
def obtener_costo_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({
        'id': producto.id,
        'costo': producto.calcular_costo_produccion()
    }), 200

# 📌 Vender un producto
@api.route('/producto/<int:id>/vender', methods=['POST'])
def vender_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    try:
        resultado = producto.vender()
        return jsonify({'mensaje': resultado}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# 📌 Reabastecer un producto
@api.route('/producto/<int:id>/reabastecer', methods=['POST'])
def reabastecer_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    datos = request.get_json()
    cantidad = datos.get("cantidad", 5)  # Si no se especifica cantidad, se reabastecen 5 unidades

    if not isinstance(cantidad, int) or cantidad <= 0:
        return jsonify({'error': 'La cantidad debe ser un número entero positivo'}), 400

    try:
        for ingrediente in producto.ingredientes:
            ingrediente.stock += cantidad  # Aumentar el stock de los ingredientes
        db.session.commit()
        return jsonify({'mensaje': f'El inventario de {producto.nombre} ha sido reabastecido en {cantidad} unidades'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 📌 Renovar inventario de un producto
@api.route('/producto/<int:id>/renovar_inventario', methods=['POST'])
def renovar_inventario_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    datos = request.get_json()
    cantidad = datos.get("cantidad", 10)  # Si no se especifica cantidad, se restaurará el stock a 10

    if not isinstance(cantidad, int) or cantidad <= 0:
        return jsonify({'error': 'La cantidad debe ser un número entero positivo'}), 400

    try:
        for ingrediente in producto.ingredientes:
            ingrediente.stock = cantidad  # Restaurar el stock
        db.session.commit()
        return jsonify({'mensaje': f'El inventario de {producto.nombre} ha sido renovado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 📌 Obtener todos los ingredientes
@api.route('/ingredientes', methods=['GET'])
def obtener_ingredientes():
    ingredientes = Ingrediente.query.all()
    return jsonify([{
        'id': i.id,
        'nombre': i.nombre,
        'calorias': i.calorias,
        'stock': i.stock
    } for i in ingredientes]), 200

# 📌 Obtener un ingrediente por ID
@api.route('/ingrediente/<int:id>', methods=['GET'])
def obtener_ingrediente(id):
    ingrediente = Ingrediente.query.get(id)
    if not ingrediente:
        return jsonify({'error': 'Ingrediente no encontrado'}), 404
    return jsonify({
        'id': ingrediente.id,
        'nombre': ingrediente.nombre,
        'calorias': ingrediente.calorias,
        'stock': ingrediente.stock
    }), 200

# 📌 Obtener un ingrediente por nombre
@api.route('/ingrediente/nombre/<string:nombre>', methods=['GET'])
def obtener_ingrediente_por_nombre(nombre):
    ingrediente = Ingrediente.query.filter_by(nombre=nombre).first()
    if not ingrediente:
        return jsonify({'error': 'Ingrediente no encontrado'}), 404
    return jsonify({
        'id': ingrediente.id,
        'nombre': ingrediente.nombre,
        'calorias': ingrediente.calorias,
        'stock': ingrediente.stock
    }), 200

# 📌 Verificar si un ingrediente es saludable
@api.route('/ingrediente/<int:id>/es_saludable', methods=['GET'])
def es_saludable(id):
    ingrediente = Ingrediente.query.get(id)
    if not ingrediente:
        return jsonify({'error': 'Ingrediente no encontrado'}), 404
    return jsonify({
        'id': ingrediente.id,
        'saludable': ingrediente.es_sano()
    }), 200
