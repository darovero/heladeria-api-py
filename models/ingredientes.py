from models.db import db

class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=10)
    heladeria_id = db.Column(db.Integer, db.ForeignKey('heladeria.id'), nullable=False)

    def __init__(self, nombre, precio, calorias, stock, heladeria_id):
        self.nombre = nombre
        self.precio = precio
        self.calorias = calorias
        self.stock = stock
        self.heladeria_id = heladeria_id
