from extensions import db  # Agrega esto

class Jugadores(db.Model):
    __tablename__ = 'Jugadores'
    DNI = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=True)
    fecha_nac = db.Column(db.Date, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(100), unique=True, nullable=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey('Equipos.id_equipo'), nullable=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('Categorias.id_categoria'), nullable=True)
