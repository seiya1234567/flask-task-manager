from flask import render_template, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
#from .forms import LoginForm
from . import auth_bp
from app.models import User

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
        return "OK"
        return redirect("/tasks")

    # 認証失敗
    return render_template("auth/login.html", error="ユーザー名かパスワードが違います")


# ----------------------------------------
# ログアウト処理
# ----------------------------------------
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect("/")

