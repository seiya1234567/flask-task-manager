from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SQLAlchemy のインスタンス
# ・アプリ本体とは未紐付け
# ・create_app() 内で db.init_app(app) により初期化される
# ・models や routes から import して使用する
db = SQLAlchemy()

# Flask-Login の管理クラス
# ・ログイン状態管理、user_loader などを担当
# ・アプリ本体とは未紐付け
# ・create_app() 内で login_manager.init_app(app) により初期化される
login_manager = LoginManager()
