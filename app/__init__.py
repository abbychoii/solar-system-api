from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if test_config:
        app.config['TESTING']= True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.planet import Planet

    from .routes import planets_bp
    app.register_blueprint(planets_bp)

    return app

    # if not test_config:
    #     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    #         "SQLALCHEMY_DATABASE_URI")
    # else:
    #     app.config["TESTING"] = True
    #     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #         "SQLALCHEMY_TEST_DATABASE_URI")

    # db.init_app(app)
    # migrate.init_app(app, db)

    # from app.models.planet import Planet

    # from app.routes import planets_bp
    # app.register_blueprint(planets_bp)

    # return app
