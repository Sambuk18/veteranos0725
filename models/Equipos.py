from extensions import db  # Agrega esto

class Equipos(db.Model):
    __tablename__ = 'Equipos'
    id_equipo = db.Column(db.Integer, primary_key=True)
    nombre_equipo = db.Column(db.String(100), unique=True, nullable=False)
    fecha_creacion = db.Column(db.Date, nullable=False)
    jugadores = db.relationship('Jugadores', backref='equipo', lazy=True)
