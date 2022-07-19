from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_moment import Moment

BASEDIR = path.abspath(path.dirname(__file__))
DB_NAME = 'database.db'

db = SQLAlchemy()
ckeditor=CKEditor()
moment=Moment()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Simon Yen'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
    app.config['MDEDITOR_FILE_UPLOADER'] = path.join(BASEDIR, 'uploads')
    db.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print('已创建数据库！')
