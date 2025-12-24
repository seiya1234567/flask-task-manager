from flask import render_template, redirect
from flask_login import current_user
from . import main_bp

@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect("/tasks")
    return render_template("auth/login.html")