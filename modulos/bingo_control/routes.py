from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
##from flask_login import login_required
from models.DataBingo import DataBingo
from modulos.bingo_control.forms import FilterForm, EditForm
from sqlalchemy import func

bingo_bp = Blueprint('bingo_control', __name__, url_prefix='/bingo_control')

@bingo_bp.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    form = FilterForm()
    
    # Construir consulta base
    query = DataBingo.query
    
    # Aplicar filtros si se envió el formulario
    if form.validate_on_submit() or request.method == 'POST':
        if form.recibo_nro.data:
            query = query.filter(DataBingo.recibo_nro.ilike(f'%{form.recibo_nro.data}%'))
        if form.carton_nro.data:
            query = query.filter(DataBingo.carton_nro.ilike(f'%{form.carton_nro.data}%'))
        if form.fecha.data:
            query = query.filter(DataBingo.fecha == form.fecha.data)
        if form.nombre_apellido.data:
            query = query.filter(DataBingo.nombre_apellido.ilike(f'%{form.nombre_apellido.data}%'))
        if form.forma_de_pago.data:
            query = query.filter(DataBingo.forma_de_pago == form.forma_de_pago.data)
        if form.tipo.data:
            query = query.filter(DataBingo.tipo == form.tipo.data)
        if form.vendedor.data:
            query = query.filter(DataBingo.vendedor.ilike(f'%{form.vendedor.data}%'))
    
    # Obtener datos paginados
    page = request.args.get('page', 1, type=int)
    per_page = 50
    registros = query.order_by(DataBingo.fecha.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('bingo_control/index.html', 
                          form=form, 
                          registros=registros,
                          active_page='bingo_control')

@bingo_bp.route('/duplicates')
#@login_required
def duplicates():
    # Encontrar recibos duplicados
    recibo_duplicates = db.session.query(
        DataBingo.recibo_nro,
        func.count(DataBingo.recibo_nro).label('count')
    ).group_by(DataBingo.recibo_nro
    ).having(func.count(DataBingo.recibo_nro) > 1).all()
    
    # Encontrar cartones duplicados
    carton_duplicates = db.session.query(
        DataBingo.carton_nro,
        func.count(DataBingo.carton_nro).label('count')
    ).group_by(DataBingo.carton_nro
    ).having(func.count(DataBingo.carton_nro) > 1).all()
    
    return render_template('bingo_control/duplicates.html', 
                          recibo_duplicates=recibo_duplicates,
                          carton_duplicates=carton_duplicates,
                          active_page='bingo_control')

@bingo_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
#@login_required
def edit(id):
    registro = DataBingo.query.get_or_404(id)
    form = EditForm(obj=registro)
    
    if form.validate_on_submit():
        form.populate_obj(registro)
        db.session.commit()
        flash('Registro actualizado correctamente', 'success')
        return redirect(url_for('bingo_control.index'))
    
    return render_template('bingo_control/edit.html', 
                          form=form, 
                          registro=registro,
                          active_page='bingo_control')

@bingo_bp.route('/delete/<int:id>')
#@login_required
def delete(id):
    registro = DataBingo.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    flash('Registro eliminado correctamente', 'success')
    return redirect(url_for('bingo_control.index'))

@bingo_bp.route('/export')
#@login_required
def export():
    # Obtener todos los registros
    registros = DataBingo.query.all()
    
    # Convertir a formato CSV
    csv_data = "id,fecha,nombre_apellido,pesos,carton_nro,serie,recibo_nro,forma_de_pago,tipo,comision,cobro,vendedor,cancelado,varios\n"
    for r in registros:
        csv_data += f"{r.id},{r.fecha},{r.nombre_apellido},{r.pesos},{r.carton_nro},{r.serie},{r.recibo_nro},{r.forma_de_pago},{r.tipo},{r.comision},{r.cobro},{r.vendedor},{r.cancelado},{r.varios}\n"
    
    # Crear respuesta para descarga
    response = Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=registros_bingo.csv"}
    )
    
    return response