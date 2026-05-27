from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Pedido, Cliente, Producto
from datetime import datetime

bp_pedidos = Blueprint('bp_pedidos', __name__)


@bp_pedidos.route('/')
def listar():
    pedidos = Pedido.query.all()
    return render_template('pedidos/listar.html', pedidos=pedidos)


@bp_pedidos.route('/crear', methods=['GET', 'POST'])
def crear():
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    if request.method == 'POST':
        cliente_id = int(request.form['cliente_id'])
        producto_id = int(request.form['producto_id'])
        monto = float(request.form['monto'])
        pedido = Pedido(
            fecha=datetime.utcnow(),
            monto=monto,
            cliente_id=cliente_id,
            producto_id=producto_id
        )
        db.session.add(pedido)
        db.session.commit()
        flash('Pedido creado exitosamente.', 'success')
        return redirect(url_for('bp_pedidos.listar'))
    return render_template('pedidos/form.html', pedido=None, clientes=clientes, productos=productos)


@bp_pedidos.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pedido = Pedido.query.get_or_404(id)
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    if request.method == 'POST':
        pedido.cliente_id = int(request.form['cliente_id'])
        pedido.producto_id = int(request.form['producto_id'])
        pedido.monto = float(request.form['monto'])
        db.session.commit()
        flash('Pedido actualizado exitosamente.', 'success')
        return redirect(url_for('bp_pedidos.listar'))
    return render_template('pedidos/form.html', pedido=pedido, clientes=clientes, productos=productos)


@bp_pedidos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    flash('Pedido eliminado exitosamente.', 'danger')
    return redirect(url_for('bp_pedidos.listar'))
