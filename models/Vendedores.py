from extensions import db  # Agrega esto

class Vendedores(db.Model):
    __tablename__ = 'Vendedores'
    DNI = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)