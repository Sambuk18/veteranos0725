from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Bingos import Bingos
from models.Vendedores import Vendedores

bingos_bp = Blueprint('bingos_bp', __name__, template_folder='templates')

@bingos_bp.route('/bingos', methods=['GET', 'POST'])
def view_bingos():
    bingos = Bingos.query.all()
    return render_template('bingos/list_bingos.html', bingos=bingos)

@bingos_bp.route('/bingos/add', methods=['GET', 'POST'])
def add_bingo():
    if request.method == 'POST':
        fecha = request.form['fecha']
        ubicacion = request.form['ubicacion']
        DNI_vendedor = request.form['DNI_vendedor']
        DNI_comprador = request.form['DNI_comprador']  # Nuevo campo
        anocarton = request.form.get('anocarton')  # Usamos get() porque es nullable
        Nrocarton = request.form.get('Nrocarton')  # Usamos get() porque es nullable

        new_bingo = Bingos(
            fecha=fecha,
            ubicacion=ubicacion,
            DNI_vendedor=DNI_vendedor,
            DNI_comprador=DNI_comprador,  # Nuevo campo
            anocarton=anocarton if anocarton else None,  # Manejo de campo nullable
            Nrocarton=Nrocarton if Nrocarton else None    # Manejo de campo nullable
        )
        db.session.add(new_bingo)
        db.session.commit()
        flash('Bingo añadido exitosamente')
        return redirect(url_for('bingos_bp.view_bingos'))
    
    vendedores = Vendedores.query.all()
    return render_template('bingos/add_bingo.html', vendedores=vendedores)

@bingos_bp.route('/bingos/edit/<int:id>', methods=['GET', 'POST'])
def edit_bingo(id):
    bingo = Bingos.query.get_or_404(id)
    if request.method == 'POST':
        bingo.fecha = request.form['fecha']
        bingo.ubicacion = request.form['ubicacion']
        bingo.DNI_vendedor = request.form['DNI_vendedor']
        bingo.DNI_comprador = request.form['DNI_comprador']  # Nuevo campo
        bingo.anocarton = request.form.get('anocarton') or None  # Nuevo campo
        bingo.Nrocarton = request.form.get('Nrocarton') or None  # Nuevo campo

        db.session.commit()
        flash('Bingo editado exitosamente')
        return redirect(url_for('bingos_bp.view_bingos'))
    
    vendedores = Vendedores.query.all()
    return render_template('bingos/edit_bingo.html', bingo=bingo, vendedores=vendedores)

@bingos_bp.route('/bingos/delete/<int:id>', methods=['POST'])
def delete_bingo(id):
    bingo = Bingos.query.get_or_404(id)
    db.session.delete(bingo)
    db.session.commit()
    flash('Bingo eliminado exitosamente')
    return redirect(url_for('bingos_bp.view_bingos'))