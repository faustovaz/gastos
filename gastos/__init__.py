from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from os import path

database = SQLAlchemy()
DATABASE_NAME = "gastos.db"
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'

    database.init_app(app)
    migrate.init_app(app, database)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    @app.cli.command("seed")
    def seed():
        from werkzeug.security import generate_password_hash
        from .models import User, Settings
        passwd = generate_password_hash('gastos1234', method='scrypt')
        database.session.add(User(login='faustovaz', password=passwd))
        database.session.add(User(login='cris', password=passwd))
        database.session.add(Settings(show_only_my_expenses=True, user_id=1))
        database.session.add(Settings(show_only_my_expenses=True, user_id=2))
        database.session.commit()
        

    return app
