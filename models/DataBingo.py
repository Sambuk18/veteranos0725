from extensions import db  # Agrega esto

class DataBingo(db.Model):
    __tablename__ = 'data_bingo'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=True)
    nombre_apellido = db.Column(db.String(255), nullable=True)
    pesos = db.Column(db.String(255), nullable=True)
    carton_nro = db.Column(db.String(255), nullable=True, index=True)
    serie = db.Column(db.String(255), nullable=True)
    recibo_nro = db.Column(db.String(255), nullable=True, index=True)
    forma_de_pago = db.Column(db.String(255), nullable=True)
    tipo = db.Column(db.String(255), nullable=True)
    comision = db.Column(db.String(255), nullable=True)
    cobro = db.Column(db.String(255), nullable=True)
    vendedor = db.Column(db.String(255), nullable=True)
    cancelado = db.Column(db.String(255), nullable=True)
    varios = db.Column(db.String(255), nullable=True)
