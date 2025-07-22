from extensions import db  # Agrega esto

class Pagos(db.Model):
    __tablename__ = 'Pagos'
    id_pago = db.Column(db.Integer, primary_key=True)
    DNI_jugador = db.Column(db.String(20), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False)
    tipo_pago = db.Column(db.String(50))
    Serie = db.Column(db.String(100), nullable=False)
    NroRec = db.Column(db.Integer, nullable=False)
    NroCarton = db.Column(db.Integer, nullable=False)