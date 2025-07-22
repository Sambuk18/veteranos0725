from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Equipos import Equipos

equipos_bp = Blueprint('equipos_bp', __name__, template_folder='templates')

@equipos_bp.route('/equipos', methods=['GET', 'POST'])
def view_equipos():
    equipos = Equipos.query.all()
    return render_template('equipos/list_equipos.html', equipos=equipos)

@equipos_bp.route('/equipos/add', methods=['GET', 'POST'])
def add_equipo():
    if request.method == 'POST':
        nombre_equipo = request.form['nombre_equipo']
        fecha_creacion = request.form['fecha_creacion']

        new_equipo = Equipos(nombre_equipo=nombre_equipo, fecha_creacion=fecha_creacion)
        db.session.add(new_equipo)
        db.session.commit()
        flash('Equipo añadido exitosamente')
        return redirect(url_for('equipos_bp.view_equipos'))

    return render_template('equipos/add_equipo.html')

@equipos_bp.route('/equipos/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipo(id):
    equipo = Equipos.query.get_or_404(id)
    if request.method == 'POST':
        equipo.nombre_equipo = request.form['nombre_equipo']
        equipo.fecha_creacion = request.form['fecha_creacion']

        db.session.commit()
        flash('Equipo editado exitosamente')
        return redirect(url_for('equipos_bp.view_equipos'))

    return render_template('equipos/edit_equipo.html', equipo=equipo)

@equipos_bp.route('/equipos/delete/<int:id>', methods=['POST'])
def delete_equipo(id):
    equipo = Equipos.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash('Equipo eliminado exitosamente')
    return redirect(url_for('equipos_bp.view_equipos'))