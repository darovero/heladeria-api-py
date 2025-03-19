from models.db import db

producto_ingrediente = db.Table('producto_ingrediente',
    db.Column('producto_id', db.Integer, db.ForeignKey('producto.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
)

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    ingredientes = db.relationship('Ingrediente', secondary=producto_ingrediente, backref='productos_relacion')

    heladeria_id = db.Column(db.Integer, db.ForeignKey('heladeria.id'), nullable=False)

    def __init__(self, nombre, precio, tipo, heladeria_id):
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo
        self.heladeria_id = heladeria_id
