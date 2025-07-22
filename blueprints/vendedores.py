from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Vendedores import Vendedores

vendedores_bp = Blueprint('vendedores_bp', __name__, template_folder='templates')

@vendedores_bp.route('/vendedores', methods=['GET', 'POST'])
def view_vendedores():
    vendedores = Vendedores.query.all()
    return render_template('vendedores/list_vendedores.html', vendedores=vendedores)

@vendedores_bp.route('/vendedores/add', methods=['GET', 'POST'])
def add_vendedor():
    if request.method == 'POST':
        DNI = request.form['DNI']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']

        new_vendedor = Vendedores(DNI=DNI, nombre=nombre, apellido=apellido, telefono=telefono)
        db.session.add(new_vendedor)
        db.session.commit()
        flash('Vendedor añadido exitosamente')
        return redirect(url_for('vendedores_bp.view_vendedores'))

    return render_template('vendedores/add_vendedor.html')

@vendedores_bp.route('/vendedores/edit/<string:DNI>', methods=['GET', 'POST'])
def edit_vendedor(DNI):
    vendedor = Vendedores.query.get_or_404(DNI)
    if request.method == 'POST':
        vendedor.nombre = request.form['nombre']
        vendedor.apellido = request.form['apellido']
        vendedor.telefono = request.form['telefono']

        db.session.commit()
        flash('Vendedor editado exitosamente')
        return redirect(url_for('vendedores_bp.view_vendedores'))

    return render_template('vendedores/edit_vendedor.html', vendedor=vendedor)

@vendedores_bp.route('/vendedores/delete/<string:DNI>', methods=['POST'])
def delete_vendedor(DNI):
    vendedor = Vendedores.query.get_or_404(DNI)
    db.session.delete(vendedor)
    db.session.commit()
    flash('Vendedor eliminado exitosamente')
    return redirect(url_for('vendedores_bp.view_vendedores'))