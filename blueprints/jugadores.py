# filepath: /home/sambu/Proyectos/Vete_001/routes/jugadores.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Jugadores import Jugadores
from models.Equipos import Equipos
from models.Categorias import Categorias
from flask_paginate import Pagination, get_page_parameter

jugadores_bp = Blueprint('jugadores_bp', __name__, template_folder='templates')

@jugadores_bp.route('/jugadores')
def view_jugadores():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = request.args.get('per_page', type=int, default=10)
    equipo_id = request.args.get('equipo_id', type=int)
    categoria_id = request.args.get('categoria_id', type=int)

    query = Jugadores.query
    if equipo_id:
        query = query.filter_by(id_equipo=equipo_id)
    if categoria_id:
        query = query.filter_by(id_categoria=categoria_id)

    jugadores = query.paginate(page, per_page, error_out=False)
    pagination = Pagination(page=page, total=jugadores.total, per_page=per_page, css_framework='bootstrap4')

    equipos = Equipos.query.all()
    categorias = Categorias.query.all()

    return render_template('jugadores/list_jugadores.html', jugadores=jugadores.items, pagination=pagination, per_page=per_page, equipos=equipos, categorias=categorias, equipo_id=equipo_id, categoria_id=categoria_id)

@jugadores_bp.route('/jugadores/add', methods=['GET', 'POST'])
def add_jugador():
    if request.method == 'POST':
        DNI = request.form['DNI']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nac = request.form['fecha_nac']
        telefono = request.form['telefono']
        correo = request.form['correo']
        id_equipo = request.form['id_equipo']
        id_categoria = request.form['id_categoria']

        new_jugador = Jugadores(DNI=DNI, nombre=nombre, apellido=apellido, fecha_nac=fecha_nac, telefono=telefono, correo=correo, id_equipo=id_equipo, id_categoria=id_categoria)
        db.session.add(new_jugador)
        db.session.commit()
        flash('Jugador añadido exitosamente')
        return redirect(url_for('jugadores_bp.view_jugadores'))
    
    equipos = Equipos.query.all()
    categorias = Categorias.query.all()
    return render_template('jugadores/add_jugador.html', equipos=equipos, categorias=categorias)

@jugadores_bp.route('/jugadores/edit/<string:DNI>', methods=['GET', 'POST'])
def edit_jugador(DNI):
    jugador = Jugadores.query.get_or_404(DNI)
    if request.method == 'POST':
        jugador.nombre = request.form['nombre']
        jugador.apellido = request.form['apellido']
        jugador.fecha_nac = request.form['fecha_nac']
        jugador.telefono = request.form['telefono']
        jugador.correo = request.form['correo']
        jugador.id_equipo = request.form['id_equipo']
        jugador.id_categoria = request.form['id_categoria']

        db.session.commit()
        flash('Jugador editado exitosamente')
        return redirect(url_for('jugadores_bp.view_jugadores'))
    
    equipos = Equipos.query.all()
    categorias = Categorias.query.all()
    return render_template('jugadores/edit_jugador.html', jugador=jugador, equipos=equipos, categorias=categorias)

@jugadores_bp.route('/jugadores/delete/<string:DNI>', methods=['POST'])
def delete_jugador(DNI):
    jugador = Jugadores.query.get_or_404(DNI)
    db.session.delete(jugador)
    db.session.commit()
    flash('Jugador eliminado exitosamente')
    return redirect(url_for('jugadores_bp.view_jugadores'))