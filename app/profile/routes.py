from . import profile_bp
from flask import render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_required, current_user
from app.extensions import db
from .validator import validate_profile, validate_password_change
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

    new_username = request.form.get("username")
    new_email = request.form.get("email")

    errors = validate_profile(
        username = new_username,
        email=new_email,
        user_id = current_user.id
    )

    if errors:
        for msg in errors.values():
            flash(msg, "error")
        return render_template("profile/profile.html",  user=current_user, errors=errors)
    
    current_user.username = new_username
    current_user.email = new_email

    db.session.commit()

    flash("更新が完了しました", "success")
    return redirect(url_for("profile.index"))

# ----------------------------------------
# パスワード変更
# ----------------------------------------
@profile_bp.route('/change_password', methods=["POST"])
@login_required
def change_password():
    current_password=request.form.get("current_password")
    new_password=request.form.get("new_password")
    confirm_password=request.form.get("new_password_confirm")

    # POST：認証処理
    errors = validate_password_change(
        current_password=current_password,
        new_password=new_password,
        confirm_password=confirm_password,
        user = current_user
    )
    
    if errors:
        for msg in errors.values():
            flash(msg, "error")
        return render_template("profile/profile.html", user=current_user, errors=errors)
             
    # パスワード更新
    current_user.password_hash = generate_password_hash(new_password)
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