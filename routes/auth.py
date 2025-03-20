from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models.db import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """Registra un nuevo usuario."""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Username, email y contraseña son obligatorios"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El email ya está registrado"}), 409

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado correctamente"}), 201

@auth.route('/login', methods=['POST'])
def login():
    """Autentica un usuario y redirige a la página de bienvenida."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    login_user(user)

    return redirect(url_for('app_routes.welcome'))  # Redirige a la página de bienvenida

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    """Cierra la sesión del usuario y redirige al login."""
    logout_user()
    return redirect(url_for('auth.login'))  # Redirige al login después de cerrar sesión

@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    """Retorna la información del usuario autenticado."""
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }), 200
