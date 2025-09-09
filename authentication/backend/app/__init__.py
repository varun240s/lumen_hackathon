from flask import Flask
from dotenv import load_dotenv
import os
from .extensions import db, bcrypt, jwt
from .api import api
from .blueprints.auth import auth_ns
from .blueprints.profile import profile_ns
from flask_cors import CORS

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI='sqlite:///yourdb.db',
    )

    # No need to create instance_path if db is in root

    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(profile_ns, path='/profile')

    with app.app_context():
        db.create_all()

    return app
