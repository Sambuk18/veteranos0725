from extensions import db  # Agrega esto

    
class Categorias(db.Model):
    __tablename__ = 'Categorias'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    jugadores = db.relationship('Jugadores', backref='categoria', lazy=True)
