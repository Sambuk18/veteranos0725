from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Dirigentes import Dirigentes

dirigentes_bp = Blueprint('dirigentes_bp', __name__, template_folder='templates')

@dirigentes_bp.route('/dirigentes', methods=['GET', 'POST'])
def view_dirigentes():
    dirigentes = Dirigentes.query.all()
    return render_template('dirigentes/list_dirigentes.html', dirigentes=dirigentes)

@dirigentes_bp.route('/dirigentes/add', methods=['GET', 'POST'])
def add_dirigente():
    if request.method == 'POST':
        DNI = request.form['DNI']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cargo = request.form['cargo']

        new_dirigente = Dirigentes(DNI=DNI, nombre=nombre, apellido=apellido, cargo=cargo)
        db.session.add(new_dirigente)
        db.session.commit()
        flash('Dirigente añadido exitosamente')
        return redirect(url_for('dirigentes_bp.view_dirigentes'))

    return render_template('dirigentes/add_dirigente.html')

@dirigentes_bp.route('/dirigentes/edit/<string:DNI>', methods=['GET', 'POST'])
def edit_dirigente(DNI):
    dirigente = Dirigentes.query.get_or_404(DNI)
    if request.method == 'POST':
        dirigente.nombre = request.form['nombre']
        dirigente.apellido = request.form['apellido']
        dirigente.cargo = request.form['cargo']

        db.session.commit()
        flash('Dirigente editado exitosamente')
        return redirect(url_for('dirigentes_bp.view_dirigentes'))

    return render_template('dirigentes/edit_dirigente.html', dirigente=dirigente)

@dirigentes_bp.route('/dirigentes/delete/<string:DNI>', methods=['POST'])
def delete_dirigente(DNI):
    dirigente = Dirigentes.query.get_or_404(DNI)
    db.session.delete(dirgente)
    db.session.commit()
    flash('Dirigente eliminado exitosamente')
    return redirect(url_for('dirigentes_bp.view_dirigentes'))