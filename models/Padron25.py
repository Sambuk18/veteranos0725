from ..extensions import db

class Padron25(db.Model):
    __tablename__ = 'padron25'
    
    id_25 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DTO_N = db.Column(db.Text)
    DTO = db.Column(db.Text)
    LOC_N = db.Column(db.Text)
    LOCALIDAD = db.Column(db.Text)
    LOCALIDAD2 = db.Column(db.Text)
    CIR_NUM = db.Column(db.Text)
    CIR_LET = db.Column(db.Text)
    ESCUELA = db.Column(db.Text)
    DOMICILIO_ESCUELA = db.Column(db.Text)
    MESA = db.Column(db.Text)
    ORDEN = db.Column(db.Text)
    MATRICULA = db.Column(db.Text, index=True)  # Este es el DNI
    VOTO = db.Column(db.Text)
    CLASE = db.Column(db.Text)  # Contiene el año de nacimiento
    APELLIDO_NOMBRE = db.Column(db.Text, index=True)  # Contiene "APELLIDO NOMBRE"
    DOMICILIO = db.Column(db.Text)
    TIPO_MATRICULA = db.Column(db.Text)
    id_padron = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Padron25 {self.MATRICULA}>'

    @property
    def dni(self):
        """Alias para MATRICULA (DNI)"""
        return self.MATRICULA

    @property
    def apellido(self):
        """Extrae el apellido de APELLIDO_NOMBRE (primera parte)"""
        if self.APELLIDO_NOMBRE:
            return self.APELLIDO_NOMBRE.split(' ', 1)[0]
        return None

    @property
    def nombre(self):
        """Extrae el nombre de APELLIDO_NOMBRE (segunda parte)"""
        if self.APELLIDO_NOMBRE and ' ' in self.APELLIDO_NOMBRE:
            return self.APELLIDO_NOMBRE.split(' ', 1)[1]
        return None

    @property
    def fecha_nacimiento_estimada(self):
        """Construye fecha de nacimiento con CLASE (año) + mes 06 + día 30"""
        if self.CLASE and self.CLASE.isdigit():
            try:
                from datetime import datetime
                return datetime(int(self.CLASE), 6, 30).date()
            except ValueError:
                return None
        return None