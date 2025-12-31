from . import profile_bp
from flask import render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_required, current_user
from app.extensions import db
from app.models import User

# ----------------------------------------
# プロフィールページ
# ----------------------------------------
@profile_bp.route('/profile', methods=["GET"])
@login_required
def index():
    if request.method == "GET":
        return render_template("profile/profile.html",user=current_user)

# ----------------------------------------
# 基本情報更新
# ----------------------------------------
@profile_bp.route('/update_profile', methods=["POST"])
@login_required
def update_profile():
    user=current_user
    new_username = request.form.get("username")
    new_email = request.form.get("email")

    existing_username = User.query.filter(User.username == new_username, User.id != user.id).first()
    existing_email = User.query.filter(User.email == new_email, User.id != user.id).first()

    if existing_username:
        flash("ユーザー名はすでに使われています", "error")
        return render_template("profile/profile.html", user=current_user)
    
    if existing_email:
        flash("メールアドレスはすでに使われています", "error")
        return render_template("profile/profile.html", user=current_user)

    user.username = new_username
    user.email = new_email

    db.session.commit()

    flash("更新が完了しました", "success")
    return redirect(url_for("profile.index"))

# ----------------------------------------
# パスワード変更
# ----------------------------------------
@profile_bp.route('/change_password', methods=["POST"])
@login_required
def change_password():
    # POST：認証処理
    user = current_user 
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    
    # 現在のパスワード照合
    if not check_password_hash(user.password_hash, current_password):
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
@profile_bp.route('/delete_account', methods=["POST"])
@login_required
def delete_account():
    user = current_user
    
    # 対象のアカウントを削除
    db.session.delete(user)
    db.session.commit()

    logout_user()

    return redirect(url_for("main.index"))