from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

class FilterForm(FlaskForm):
    recibo_nro = StringField('Número de Recibo')
    carton_nro = StringField('Número de Cartón')
    fecha = DateField('Fecha', validators=[Optional()])
    nombre_apellido = StringField('Nombre/Apellido')
    forma_de_pago = SelectField('Forma de Pago', choices=[
        ('', 'Todas'), 
        ('MERCADO PAGO', 'Mercado Pago'),
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia')
    ])
    tipo = SelectField('Tipo', choices=[
        ('', 'Todos'), 
        ('JUGADOR', 'Jugador'),
        ('DIRIGENTE', 'Dirigente'),
        ('APORTANTE', 'Aportante')
    ])
    vendedor = StringField('Vendedor')
    submit = SubmitField('Filtrar')

class EditForm(FlaskForm):
    fecha = DateField('Fecha', validators=[Optional()])
    nombre_apellido = StringField('Nombre/Apellido', validators=[DataRequired()])
    pesos = StringField('Pesos')
    carton_nro = StringField('Número de Cartón', validators=[DataRequired()])
    serie = StringField('Serie')
    recibo_nro = StringField('Número de Recibo', validators=[DataRequired()])
    forma_de_pago = SelectField('Forma de Pago', choices=[
        ('MERCADO PAGO', 'Mercado Pago'),
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('OTRO', 'Otro')
    ])
    tipo = SelectField('Tipo', choices=[
        ('JUGADOR', 'Jugador'),
        ('DIRIGENTE', 'Dirigente'),
        ('APORTANTE', 'Aportante'),
        ('SOCIO', 'Socio'),
        ('CLIENTE', 'Cliente')
    ])
    comision = StringField('Comisión')
    cobro = StringField('Cobro')
    vendedor = StringField('Vendedor')
    cancelado = StringField('Cancelado')
    varios = StringField('Varios')
    submit = SubmitField('Guardar Cambios')