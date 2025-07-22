from extensions import db  # O de donde traigas tu `db`

class RecibosProcesados(db.Model):
    __tablename__ = 'RecibosProcesados'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bingo_numero = db.Column(db.String(255), nullable=True)
    apellido_y_nombre = db.Column(db.String(255), nullable=True)
    dni_numero = db.Column(db.String(255), nullable=True)
    celular = db.Column(db.String(255), nullable=True)
    fecha = db.Column(db.Date, nullable=True)
    cuota = db.Column(db.String(255), nullable=True)
    recibo = db.Column(db.String(255), nullable=True)
    monto = db.Column(db.String(255), nullable=True)
    serie = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<RecibosProcesados id={self.id} recibo={self.recibo}>'
