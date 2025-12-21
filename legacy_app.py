from flask import Flask, render_template, redirect, request, flash
from models import db, Task, User
from datetime import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from zoneinfo import ZoneInfo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager, UserMixin, login_user,
    logout_user, login_required, current_user
)
import os

# ----------------------------------------
# データベース接続設定
# docker-compose.yml の db コンテナを参照
# ----------------------------------------
#DATABASE_URL = 'postgresql://myuser:mysecretpassword@db:5432/mydatabase'
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///default.db')


# ----------------------------------------
# DBコンテナの起動を待つユーティリティ関数
# （Postgres起動前にアプリが動くとエラーになるため）
# ----------------------------------------
def wait_for_db():
    engine = create_engine(DATABASE_URL)
    while True:
        try:
            # 実際に接続して成功するまでループ
            with engine.connect() as conn:
                print("DB connection succeeded!")
                break
        except OperationalError:
            # DB がまだ起動していない → 2 秒待って再試行
            time.sleep(2)


wait_for_db()

# ----------------------------------------
# Flask アプリケーションの初期化
# ----------------------------------------
app = Flask(__name__)

# セッション暗号化キー
# デプロイ時は環境変数で設定すべき
SECRET_KEY = os.getenv('SECRET_KEY', 'default_key')
#app.secret_key = 'your_secret_key_here_12345'
app.secret_key = SECRET_KEY

# ----------------------------------------
# SQLAlchemy の設定
# ----------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask アプリに DB を紐付け
db.init_app(app)

# DB テーブル作成（必要な場合のみ）
with app.app_context():
    db.create_all()


# ----------------------------------------
# Flask-Login の設定
# ----------------------------------------
login_manager = LoginManager()

# Flask アプリと連携
login_manager.init_app(app)

# 未ログイン時にリダイレクトする先のビュー名
login_manager.login_view = 'login'


# ----------------------------------------
# ログイン中ユーザーの読み込み処理
# Flask-Login が内部的に実行する
# ----------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# ----------------------------------------
# TOPページ → ログイン済みならタスク一覧、未ログインならログイン画面
# ----------------------------------------
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect("/tasks")
    return render_template("auth/login.html")


# ----------------------------------------
# 新規登録画面
# GET → フォーム表示
# POST → 入力確認画面へ
# ----------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    # POST の場合、入力内容を確認画面へ渡す
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    return render_template(
        "auth/confirm.html",
        username=username,
        email=email,
        password=password
    )


# ----------------------------------------
# 新規登録の確認 → 本登録処理
# ----------------------------------------
@app.route("/confirm", methods=["POST"])
def confirm():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    errors = {}

    # ユーザー名の重複チェック
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        errors["username"] = "ユーザー名はすでに使われています"

    # メールアドレスの重複チェック
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        errors["email"] = "メールアドレスはすでに使われています"

    # エラーがあれば登録画面へ戻す
    if errors:
        return render_template("auth/register.html", errors=errors)

    # パスワードをハッシュ化して保存
    password_hash = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/tasks")


# ----------------------------------------
# タスク一覧／検索／新規作成ページ
# GET → 一覧・検索
# POST → 新規作成
# ----------------------------------------
@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    # ------------------------------------
    # GET：タスク一覧表示 & 絞り込み処理
    # ------------------------------------
    if request.method == "GET":
        tasks_query = Task.query.filter(Task.user_id == current_user.id)

        # フィルタ条件（ステータス・優先度・キーワード）
        status_filter = request.args.get("status") or ""
        priority_filter = request.args.get("priority") or ""
        keyword = request.args.get("keyword") or ""

        if status_filter:
            tasks_query = tasks_query.filter(Task.status == status_filter)
        if priority_filter:
            tasks_query = tasks_query.filter(Task.priority == priority_filter)
        if keyword:
            tasks_query = tasks_query.filter(Task.title.ilike(f"%{keyword}%"))

        # 表示データの取得（新しい順）
        tasks_data = tasks_query.order_by(Task.created_at.desc()).all()

        # 統計情報（ダッシュボード部）
        total_count = tasks_query.count()
        high_priority_count = tasks_query.filter(Task.priority == '高').count()
        in_progress_count = tasks_query.filter(Task.status == '進行中').count()
        completed_count = tasks_query.filter(Task.status == '完了').count()

        return render_template(
            "tasks/tasks.html",
            tasks=tasks_data,
            total_count=total_count,
            high_priority_count=high_priority_count,
            in_progress_count=in_progress_count,
            completed_count=completed_count,
            status_filter=status_filter,
            priority_filter=priority_filter,
            keyword=keyword,
        )

    # ------------------------------------
    # POST：新しいタスクを登録
    # ------------------------------------
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        due_date_str = request.form.get("due_date")
        status = request.form.get("status")
        priority = request.form.get("priority")
        category = request.form.get("category")

        # 日付の文字列を date 型に変換
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None

        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            priority=priority,
            category=category,
            user_id=current_user.id
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect("/tasks")


# ----------------------------------------
# タスク削除
# ----------------------------------------
@app.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    task_data = Task.query.get(id)

    if task_data:
        db.session.delete(task_data)
        db.session.commit()
        return f'Task {id} deleted', 200
    else:
        return 'Task not found', 404


# ----------------------------------------
# 新規作成フォーム表示
# ----------------------------------------
@app.route("/tasks/new", methods=["GET"])
@login_required
def form():
    return render_template("tasks/form.html")


# ----------------------------------------
# 編集フォーム表示
# ----------------------------------------
@app.route("/tasks/<int:id>/edit", methods=["GET"])
@login_required
def edit(id):
    task_data = Task.query.get_or_404(id)
    return render_template("tasks/edit.html", task=task_data)

# ----------------------------------------
# 編集内容の反映
# ----------------------------------------
@app.route("/tasks/<int:id>/", methods=["POST"])
@login_required
def apply(id):
    task_data = Task.query.get_or_404(id)

    title = request.form.get("title")
    description = request.form.get("description")
    due_date_str = request.form.get("due_date")
    status = request.form.get("status")
    priority = request.form.get("priority")
    category = request.form.get("category")

    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None

    # 更新
    task_data.title = title
    task_data.description = description
    task_data.due_date = due_date
    task_data.status = status
    task_data.priority = priority
    task_data.category = category

    db.session.commit()

    return redirect("/tasks")


# ----------------------------------------
# プロフィールページ
# ----------------------------------------
@app.route('/profile', methods=["GET"])
@login_required
def profile():
    if request.method == "GET":
        return render_template("profile/profile.html",user=current_user)

# ----------------------------------------
# 基本情報更新
# ----------------------------------------
@app.route('/update_profile', methods=["POST"])
@login_required
def update_profile():
    user=current_user
    new_username = request.form.get("username")
    new_email = request.form.get("email")

    existing_email = User.query.filter(User.email == new_email, User.id != user.id).first()

    if existing_email:
        flash("メールアドレスはすでに使われています", "error")
        return render_template("profile/profile.html", user=current_user)

    user.username = new_username
    user.email = new_email

    db.session.commit()

    flash("更新が完了しました", "success")
    return redirect("/profile")

# ----------------------------------------
# パスワード変更
# ----------------------------------------
@app.route('/change_password', methods=["POST"])
@login_required
def change_password():
    # POST：認証処理
    user = current_user 
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    
    # 現在のパスワード照合
    if not check_password_hash(user.password_hash, current_password):
        #errors["password"] = "パスワードが違います"
        flash("パスワードが違います", "error")
        return render_template("profile/profile.html", user=current_user)
        
    # パスワード更新
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    flash("パスワードの更新が完了しました", "success")
    return redirect("/profile")

# ----------------------------------------
# アカウント削除
# ----------------------------------------
@app.route('/delete_account', methods=["POST"])
@login_required
def delete_account():
    user = current_user
    
    # 対象のアカウントを削除
    db.session.delete(user)
    db.session.commit()

    logout_user()

    return redirect("/")

# ----------------------------------------
# JST（日本時間）フォーマットのフィルタ
# テンプレート内で |to_jst のように使用
# ----------------------------------------
@app.template_filter('to_jst')
def to_jst_filter(dt):
    if dt is None:
        return ''
    jst = dt.astimezone(ZoneInfo("Asia/Tokyo"))
    return jst.strftime("%Y-%m-%d %H:%M")


# ----------------------------------------
# ログイン処理
# ----------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    # 既にログインしている場合はタスク一覧にリダイレクト
    if current_user.is_authenticated:
        return redirect("/tasks")
    
    if request.method == "GET":
        return render_template("auth/login.html")

    # POST：認証処理
    username = request.form.get("username")
    password = request.form.get("password")
    remember_me = request.form.get("remember-me") == "on"

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=remember_me)
        return redirect("/tasks")

    # 認証失敗
    return render_template("auth/login.html", error="ユーザー名かパスワードが違います")


# ----------------------------------------
# ログアウト処理
# ----------------------------------------
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect("/")


# ----------------------------------------
# アプリ起動設定
# docker-compose では flask run が使われるため基本未使用
# ----------------------------------------
if __name__ == '__main__':
    app.run(debug=True)