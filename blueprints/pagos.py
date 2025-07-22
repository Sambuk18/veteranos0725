from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.Pagos import Pagos
from models.Jugadores import Jugadores
from extensions import db

pagos_bp = Blueprint('pagos_bp', __name__, template_folder='templates')

@pagos_bp.route('/pagos', methods=['GET', 'POST'])
def view_pagos():
    if request.method == 'POST':
        if 'agregar' in request.form:
            nuevo_pago = Pagos(
                DNI_jugador=request.form['DNI_jugador'],
                monto=request.form['monto'],
                fecha_pago=request.form['fecha_pago'],
                tipo_pago=request.form['tipo_pago'],
                Serie=request.form['Serie'],
                NroRec=request.form['NroRec'],
                NroCarton=request.form['NroCarton']
            )
            db.session.add(nuevo_pago)
            db.session.commit()
        elif 'editar' in request.form:
            pago = Pagos.query.get(request.form['id_pago'])
            if pago:
                pago.DNI_jugador = request.form['DNI_jugador']
                pago.monto = request.form['monto']
                pago.fecha_pago = request.form['fecha_pago']
                pago.tipo_pago = request.form['tipo_pago']
                pago.Serie = request.form['Serie']
                pago.NroRec = request.form['NroRec']
                pago.NroCarton = request.form['NroCarton']
                db.session.commit()
        elif 'borrar' in request.form:
            pago = Pagos.query.get(request.form['id_pago'])
            if pago:
                db.session.delete(pago)
                db.session.commit()
        elif 'buscar' in request.form:
            filtro = request.form['filtro']
            resultados = Pagos.query.filter_by(DNI_jugador=filtro).all()
            return render_template('pagos/list_pagos.html', pagos=resultados)
    pagos = Pagos.query.all()
    return render_template('pagos/list_pagos.html', pagos=pagos)

@pagos_bp.route('/buscar_jugador', methods=['POST'])
def buscar_jugador():
    filtro = request.form.get('filtro_jugador')
    if not filtro:
        return jsonify({'error': 'Debe ingresar un valor'})

    resultados = Jugadores.query.filter(
        (Jugadores.DNI.like(f"%{filtro}%")) |
        (Jugadores.nombre.like(f"%{filtro}%")) |
        (Jugadores.apellido.like(f"%{filtro}%"))
    ).limit(10).all()

    if not resultados:
        return jsonify({'error': 'No se encontraron jugadores'})

    jugadores = []
    for j in resultados:
        jugadores.append({
            'DNI': j.DNI,
            'nombre': j.nombre,
            'apellido': j.apellido,
            'telefono': j.telefono,
            'correo': j.correo,
            'fecha_nac': j.fecha_nac.strftime('%Y-%m-%d') if j.fecha_nac else ''
        })

    return jsonify({'jugadores': jugadores})

