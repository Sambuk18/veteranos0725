from extensions import db  # Agrega esto

class UserSistema(db.Model):
    __tablename__ = 'User_sistema'
    DNI = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=True)
