from flask import Flask, render_template  # Asegúrate de importar render_template
from extensions import db
from config import Config

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Rutas básicas
    @app.route('/')
    def index():
        return render_template('index.html')  # Ahora render_template está disponible
    
    return app

def register_blueprints(app):
    """Función para registrar todos los blueprints"""
    # Importar blueprints (no modelos aquí)
    from blueprints.aportes import aportes_bp
    from blueprints.arbitros import arbitros_bp
    from blueprints.bingos import bingos_bp
    from modulos.bingo_control.routes import bingo_bp
    from blueprints.categorias import categorias_bp
    from blueprints.dirigentes import dirigentes_bp
    from blueprints.equipos import equipos_bp
    from blueprints.jugadores import jugadores_bp
    from blueprints.pagos import pagos_bp
    from blueprints.vendedores import vendedores_bp
    
    # Registrar blueprints
    app.register_blueprint(aportes_bp)
    app.register_blueprint(arbitros_bp)
    app.register_blueprint(bingos_bp)
    app.register_blueprint(bingo_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(dirigentes_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(jugadores_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(vendedores_bp)

# Crear la aplicación
app = create_app()

# Configuración para ejecución directa y con Gunicorn
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # print("Rutas disponibles:")
        # for rule in app.url_map.iter_rules():
        #     print(f"{rule.endpoint}: {rule.rule}")
    app.run(debug=True)
else:
    # Para Gunicorn
    application = app