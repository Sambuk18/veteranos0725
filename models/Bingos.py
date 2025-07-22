from extensions import db  # Agrega esto

class Bingos(db.Model):
    __tablename__ = 'Bingos'
    id_bingo = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    DNI_comprador = db.Column(db.String(20), nullable=False) # Nuevo campo
    anocarton = db.Column(db.Integer, nullable=False)  # Nuevo campo
    Nrocarton = db.Column(db.Integer, nullable=False)  # Nuevo campo
    DNI_vendedor = db.Column(db.String(20), db.ForeignKey('vendedores.DNI'), nullable=False)   
    
    