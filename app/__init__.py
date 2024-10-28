from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configurations from the config.py file
    app.config.from_object('config.Config')

    # Import and register the routes blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app