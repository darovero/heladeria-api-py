from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from routes.routes import app_routes, cargar_datos_iniciales
from models.db import db
from config import Config  

# Inicialización de la aplicación Flask
app = Flask(__name__, template_folder="views")
app.config.from_object(Config)

# Inicializar Base de Datos
db.init_app(app)

# Configurar el Login Manager para autenticación
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Importar modelos después de inicializar `db`
from models.user import User

# Función de carga de usuarios en sesión
@login_manager.user_loader
def load_user(user_id):
    """Carga un usuario desde la base de datos por su ID."""
    return User.query.get(int(user_id))

# Importar y registrar Blueprints
from routes.auth import auth  
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(app_routes)

# Crear las tablas en la base de datos si no existen
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Asegura que las tablas sean creadas
        cargar_datos_iniciales()  # Carga datos iniciales en la BD
    app.run(debug=True)
