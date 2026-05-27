from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Producto

bp_productos = Blueprint('bp_productos', __name__)


@bp_productos.route('/')
def listar():
    productos = Producto.query.all()
    return render_template('productos/listar.html', productos=productos)


@bp_productos.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        producto = Producto(nombre=nombre, precio=precio, stock=stock)
        db.session.add(producto)
        db.session.commit()
        flash('Producto creado exitosamente.', 'success')
        return redirect(url_for('bp_productos.listar'))
    return render_template('productos/form.html', producto=None)


@bp_productos.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = float(request.form['precio'])
        producto.stock = int(request.form['stock'])
        db.session.commit()
        flash('Producto actualizado exitosamente.', 'success')
        return redirect(url_for('bp_productos.listar'))
    return render_template('productos/form.html', producto=producto)


@bp_productos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente.', 'danger')
    return redirect(url_for('bp_productos.listar'))
