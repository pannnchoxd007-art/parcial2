from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Cliente

bp_clientes = Blueprint('bp_clientes', __name__)


@bp_clientes.route('/')
def listar():
    clientes = Cliente.query.all()
    return render_template('clientes/listar.html', clientes=clientes)


@bp_clientes.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        cliente = Cliente(nombre=nombre, telefono=telefono)
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente creado exitosamente.', 'success')
        return redirect(url_for('bp_clientes.listar'))
    return render_template('clientes/form.html', cliente=None)


@bp_clientes.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.telefono = request.form['telefono']
        db.session.commit()
        flash('Cliente actualizado exitosamente.', 'success')
        return redirect(url_for('bp_clientes.listar'))
    return render_template('clientes/form.html', cliente=cliente)


@bp_clientes.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente eliminado exitosamente.', 'danger')
    return redirect(url_for('bp_clientes.listar'))
