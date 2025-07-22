from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Categorias import Categorias

categorias_bp = Blueprint('categorias_bp', __name__, template_folder='templates')

@categorias_bp.route('/categorias', methods=['GET', 'POST'])
def view_categorias():
    categorias = Categorias.query.all()
    return render_template('categorias/list_categorias.html', categorias=categorias)

@categorias_bp.route('/categorias/add', methods=['GET', 'POST'])
def add_categoria():
    if request.method == 'POST':
        nombre_categoria = request.form['nombre_categoria']
        descripcion = request.form['descripcion']

        new_categoria = Categorias(nombre_categoria=nombre_categoria, descripcion=descripcion)
        db.session.add(new_categoria)
        db.session.commit()
        flash('Categoría añadida exitosamente')
        return redirect(url_for('categorias_bp.view_categorias'))

    return render_template('categorias/add_categoria.html')

@categorias_bp.route('/categorias/edit/<int:id>', methods=['GET', 'POST'])
def edit_categoria(id):
    categoria = Categorias.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nombre_categoria = request.form['nombre_categoria']
        categoria.descripcion = request.form['descripcion']

        db.session.commit()
        flash('Categoría editada exitosamente')
        return redirect(url_for('categorias_bp.view_categorias'))

    return render_template('categorias/edit_categoria.html', categoria=categoria)

@categorias_bp.route('/categorias/delete/<int:id>', methods=['POST'])
def delete_categoria(id):
    categoria = Categorias.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada exitosamente')
    return redirect(url_for('categorias_bp.view_categorias'))