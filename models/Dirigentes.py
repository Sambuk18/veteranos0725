from extensions import db  # Agrega esto

class Dirigentes(db.Model):
    __tablename__ = 'Dirigentes'
    DNI = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=True)
    cargo = db.Column(db.String(50), nullable=True)
