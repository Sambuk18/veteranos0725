from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import Blueprint
from models.aportes import Aportes
from models.Dirigentes import Dirigentes

aportes_bp = Blueprint('aportes_bp', __name__, template_folder='templates')

@aportes_bp.route('/aportes', methods=['GET', 'POST'])
def view_aportes():
    aportes = Aportes.query.all()
    return render_template('aportes/list_aportes.html', aportes=aportes)

@aportes_bp.route('/aportes/add', methods=['GET', 'POST'])
def add_aporte():
    if request.method == 'POST':
        DNI_dirigente = request.form['DNI_dirigente']
        monto = request.form['monto']
        fecha_aporte = request.form['fecha_aporte']
        motivo = request.form['motivo']

        new_aporte = Aportes(DNI_dirigente=DNI_dirigente, monto=monto, fecha_aporte=fecha_aporte, motivo=motivo)
        db.session.add(new_aporte)
        db.session.commit()
        flash('Aporte añadido exitosamente')
        return redirect(url_for('aportes_bp.view_aportes'))
    
    dirigentes = Dirigentes.query.all()
    return render_template('aportes/add_aporte.html', dirigentes=dirigentes)

@aportes_bp.route('/aportes/edit/<int:id>', methods=['GET', 'POST'])
def edit_aporte(id):
    aporte = Aportes.query.get_or_404(id)
    if request.method == 'POST':
        aporte.DNI_dirigente = request.form['DNI_dirigente']
        aporte.monto = request.form['monto']
        aporte.fecha_aporte = request.form['fecha_aporte']
        aporte.motivo = request.form['motivo']

        db.session.commit()
        flash('Aporte editado exitosamente')
        return redirect(url_for('aportes_bp.view_aportes'))
    
    dirigentes = Dirigentes.query.all()
    return render_template('aportes/edit_aporte.html', aporte=aporte, dirigentes=dirigentes)

@aportes_bp.route('/aportes/delete/<int:id>', methods=['POST'])
def delete_aporte(id):
    aporte = Aportes.query.get_or_404(id)
    db.session.delete(aporte)
    db.session.commit()
    flash('Aporte eliminado exitosamente')
    return redirect(url_for('aportes_bp.view_aportes'))