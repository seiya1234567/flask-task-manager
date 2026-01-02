from flask import render_template, redirect, request, url_for,flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from . import auth_bp
from app.models import User
from app.extensions import db
from .validator import validate_register

# --------------------------------
# Validation Error Messages
# --------------------------------
ERROR_MESSAGES = {
    "username": {
        "required": "ユーザー名は必須です",
        "duplicate": "ユーザー名はすでに使われています",
    },
    "email": {
        "required": "メールアドレスは必須です",
        "duplicate": "メールアドレスはすでに使われています",
    },
    "password": {
        "required": "パスワードは必須です",
        "too_short": "パスワードは8文字以上にしてください",
    },
    "password_confirm": {
        "required": "確認用のパスワードは必須です",
        "mismatch": "パスワードが一致しません",
    },
}

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
# ----------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    # POST の場合、入力内容を確認 → バリデーション → 登録処理
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    password_confirm = request.form.get("password_confirm")

    errors = validate_register(
        username=username,
        email=email,
        password=password,
        password_confirm=password_confirm,
    )

    if errors:
        for field, key in errors.items():
            msg = ERROR_MESSAGES[field][key]
            flash(msg, f"{field}_error")
        return redirect(url_for("auth.register"))

    # パスワードをハッシュ化して保存
    password_hash = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("このユーザーは既に登録されています", "error")
        return redirect(url_for("auth.register"))

    flash("ユーザー登録が完了しました", "success")
    return redirect(url_for("auth.register"))