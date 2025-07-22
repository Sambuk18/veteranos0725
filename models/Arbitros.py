from extensions import db  # Agrega esto

class Arbitros(db.Model):
    __tablename__ = 'Arbitros'
    DNI = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=True)
    licencia = db.Column(db.String(50), unique=True, nullable=False)
