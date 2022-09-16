from apps.config import config
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
login_master = LoginManager()
login_master.login_view = 'auth.signup'
login_master.login_message = ''

def create_app(config_key):
    # Flaskのインスタンス化と諸設定
    app = Flask(__name__)
    app.config.from_object(config[config_key])
    csrf.init_app(app)
    login_master.init_app(app)

    # DB設定
    db.init_app(app)
    Migrate(app, db)

    # カスタムエラー画面
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    # Blueprint登録
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix='/crud')

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix='/auth')

    from apps.detector import views as dt_views
    app.register_blueprint(dt_views.dt)

    return app

def page_not_found(e):
    """404 Not Found"""
    return render_template('404.html'), 404

def internal_server_error(e):
    """500 Internal Server Error"""
    return render_template('500.html'), 500
