from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from routes.routes import app_routes, cargar_datos_iniciales
from models.db import db
from config import Config  

app = Flask(__name__, template_folder="views")
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()  
login_manager.init_app(app)
login_manager.login_view = "auth.login"

from routes.auth import auth 

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(app_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        cargar_datos_iniciales()
    app.run(debug=True)
