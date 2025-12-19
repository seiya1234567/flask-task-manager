import os

class BaseConfig:
    # --------------------------------------------------------
    # Flask アプリケーションの基本設定
    # --------------------------------------------------------
    
    # セッションや CSRF 保護で使う秘密鍵
    # 環境変数 SECRET_KEY が設定されていなければ 'default_key' を使用
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_key')
    
    # データベース接続文字列
    # 環境変数 DATABASE_URL が設定されていなければ SQLite のローカル DB を使用
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    
    # SQLAlchemy の変更追跡を無効化（パフォーマンス向上のため）
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --------------------------------------------------------
    # メール送信設定（将来追加予定）
    # --------------------------------------------------------
    # 環境変数 MAIL_USERNAME, MAIL_PASSWORD から取得予定
    #MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    #MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
