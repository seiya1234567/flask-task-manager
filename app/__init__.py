from flask import Flask
from .config import BaseConfig
from .extensions import db, login_manager


def create_app():
    """
    Flask アプリケーションファクトリ

    - Flask アプリインスタンスの生成
    - 設定の読み込み
    - 拡張機能（SQLAlchemy / Flask-Login）の初期化
    - user_loader の登録
    - Blueprint の登録

    Flask CLI / Gunicorn から呼び出される起点関数
    """

    # --------------------------------------------------
    # Flask アプリケーション生成
    # --------------------------------------------------
    app = Flask(__name__)

    # --------------------------------------------------
    # アプリ設定の読み込み
    # config.py に定義した設定クラスを使用
    # --------------------------------------------------
    app.config.from_object(BaseConfig)

    # --------------------------------------------------
    # 拡張機能の初期化
    # --------------------------------------------------

    # SQLAlchemy を Flask アプリに紐付け
    # models から db を import して利用可能になる
    db.init_app(app)

    # Flask-Login を Flask アプリに紐付け
    # ログイン状態管理・current_user を有効化
    login_manager.init_app(app)

    # 未ログイン状態で @login_required にアクセスした場合の
    # リダイレクト先エンドポイント
    login_manager.login_view = 'auth.login'

    # --------------------------------------------------
    # Flask-Login user_loader の定義
    # --------------------------------------------------
    # セッションに保存された user_id から
    # 対応する User モデルを取得するための関数
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # --------------------------------------------------
    # Blueprint の登録
    # --------------------------------------------------
    # 循環 import を避けるため遅延 import
    from .main import main_bp

    # main Blueprint をアプリに登録
    app.register_blueprint(main_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app
