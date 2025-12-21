from flask import Flask
from .config import BaseConfig
from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    # Flask アプリに DB を紐付け
    db.init_app(app)

    # Flask アプリと連携
    login_manager.init_app(app)

    # 未ログイン時にリダイレクトする先のビュー名
    login_manager.login_view = 'login'

    return app