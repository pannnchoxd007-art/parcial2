from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'techbol-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///techbol.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    from app.blueprints.bp_clientes import bp_clientes
    from app.blueprints.bp_productos import bp_productos
    from app.blueprints.bp_pedidos import bp_pedidos

    app.register_blueprint(bp_clientes, url_prefix='/clientes')
    app.register_blueprint(bp_productos, url_prefix='/productos')
    app.register_blueprint(bp_pedidos, url_prefix='/pedidos')

    # Ruta principal
    from flask import redirect, url_for

    @app.route('/')
    def index():
        return redirect(url_for('bp_productos.listar'))

    return app
