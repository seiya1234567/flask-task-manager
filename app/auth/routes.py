from flask import render_template, redirect, request, url_for,flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
#from .forms import LoginForm
from . import auth_bp
from app.models import User
from app.extensions import db

# ----------------------------------------
# ログイン処理
# ----------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
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
        return redirect(url_for("tasks.index"))

    # 認証失敗
    return render_template("auth/login.html", error="ユーザー名かパスワードが違います")

# ----------------------------------------
# ログアウト処理
# ----------------------------------------
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

# ----------------------------------------
# 新規登録画面
# GET → フォーム表示
# POST → 入力確認画面へ
# ----------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    # POST の場合、入力内容を確認画面へ渡す
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # ユーザー名の重複チェック
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("ユーザー名はすでに使われています", "username_error")

    # メールアドレスの重複チェック
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        flash("メールアドレスはすでに使われています", "email_error")

    # エラーがあれば登録画面へ戻す
    if existing_user or existing_email:
        return redirect(url_for("auth.register"))

    return render_template(
        "auth/confirm.html",
        username=username,
        email=email,
        password=password
    )

# ----------------------------------------
# 新規登録の確認 → 本登録処理
# ----------------------------------------
@auth_bp.route("/confirm", methods=["POST"])
def confirm():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # パスワードをハッシュ化して保存
    password_hash = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("tasks.index"))