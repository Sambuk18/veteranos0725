from extensions import db  # Agrega esto

class Aportes(db.Model):
    __tablename__ = 'Aportes'
    id_aporte = db.Column(db.Integer, primary_key=True)
    DNI_dirigente = db.Column(db.String(20), db.ForeignKey('dirigentes.DNI'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_aporte = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.Text, nullable=True)
