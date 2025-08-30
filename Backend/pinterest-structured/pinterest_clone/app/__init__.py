from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"

    # --- Database Config ---
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pinclone.db'

    # --- File Upload Config ---
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app/static/uploads")
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Init DB
    db.init_app(app)

    # Import models
    from app.models import user, pin  

    # Register blueprints
    from app.controllers.user import user_bp
    from app.controllers.pin import pin_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(pin_bp)

    with app.app_context():
        db.create_all()

    return app
