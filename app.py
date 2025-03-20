from flask import Flask, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models.db import db
from models.user import User
from routes.auth import auth
from routes.routes import app_routes, cargar_datos_iniciales
from routes.api import api  # Importar las rutas del API

app = Flask(__name__, template_folder="views")
app.config.from_object(Config)

# Configuración de sesión
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db.init_app(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario por ID en la sesión de Flask-Login"""
    return User.query.get(int(user_id))

# 📌 Configurar respuesta para accesos no autorizados (en lugar de redirección)
@login_manager.unauthorized_handler
def unauthorized():
    """Devuelve un JSON con error 401 en lugar de redirigir al login."""
    return jsonify({"error": "No autorizado. Inicia sesión primero."}), 401

# Registrar blueprints de autenticación, rutas principales y API
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(app_routes)
app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos si no existen
        cargar_datos_iniciales()  # Carga datos iniciales en la DB
    app.run(debug=True)
