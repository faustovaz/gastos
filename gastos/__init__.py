from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

database = SQLAlchemy()
DATABASE_NAME = "gastos.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'

    database.init_app(app)

    from .models import GastoMensal, GastoRecorrente
    with app.app_context():
        if not path.exists(f'gastos/{DATABASE_NAME}'):
            database.create_all()


    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app
