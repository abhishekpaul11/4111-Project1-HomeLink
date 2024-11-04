# flask_app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configurations if any
    app.config.from_object("flask_app.config")
    
    # Import and register routes
    from .routes import main
    app.register_blueprint(main)
    
    return app