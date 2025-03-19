from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models.db import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """Registra un nuevo usuario."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado correctamente"}), 201

@auth.route('/login', methods=['POST'])
def login():
    """Autentica un usuario."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    login_user(user)
    return jsonify({"message": "Inicio de sesión exitoso", "user": user.email}), 200

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    """Cierra la sesión del usuario."""
    logout_user()
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200

@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    """Retorna la información del usuario autenticado."""
    return jsonify({"email": current_user.email}), 200
