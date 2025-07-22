from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Arbitros import Arbitros

arbitros_bp = Blueprint('arbitros_bp', __name__, template_folder='templates')

@arbitros_bp.route('/arbitros', methods=['GET', 'POST'])
def view_arbitros():
    arbitros = Arbitros.query.all()
    return render_template('arbitros/list_arbitros.html', arbitros=arbitros)

@arbitros_bp.route('/arbitros/add', methods=['GET', 'POST'])
def add_arbitro():
    if request.method == 'POST':
        DNI = request.form['DNI']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        licencia = request.form['licencia']

        new_arbitro = Arbitros(DNI=DNI, nombre=nombre, apellido=apellido, licencia=licencia)
        db.session.add(new_arbitro)
        db.session.commit()
        flash('Árbitro añadido exitosamente')
        return redirect(url_for('arbitros_bp.view_arbitros'))

    return render_template('arbitros/add_arbitro.html')

@arbitros_bp.route('/arbitros/edit/<string:DNI>', methods=['GET', 'POST'])
def edit_arbitro(DNI):
    arbitro = Arbitros.query.get_or_404(DNI)
    if request.method == 'POST':
        arbitro.nombre = request.form['nombre']
        arbitro.apellido = request.form['apellido']
        arbitro.licencia = request.form['licencia']

        db.session.commit()
        flash('Árbitro editado exitosamente')
        return redirect(url_for('arbitros_bp.view_arbitros'))

    return render_template('arbitros/edit_arbitro.html', arbitro=arbitro)

@arbitros_bp.route('/arbitros/delete/<string:DNI>', methods=['POST'])
def delete_arbitro(DNI):
    arbitro = Arbitros.query.get_or_404(DNI)
    db.session.delete(arbitro)
    db.session.commit()
    flash('Árbitro eliminado exitosamente')
    return redirect(url_for('arbitros_bp.view_arbitros'))