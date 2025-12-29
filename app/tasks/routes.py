from flask import render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
#from .forms import LoginForm
from . import tasks_bp
from app.models import Task
from app.extensions import db


@tasks_bp.route("/tasks", methods=["GET", "POST"])
@login_required
def index():
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
@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
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
@tasks_bp.route("/tasks/new", methods=["GET"])
@login_required
def form():
    return render_template("tasks/form.html")


# ----------------------------------------
# 編集フォーム表示
# ----------------------------------------
@tasks_bp.route("/tasks/<int:id>/edit", methods=["GET"])
@login_required
def edit(id):
    task_data = Task.query.get_or_404(id)
    return render_template("tasks/edit.html", task=task_data)

# ----------------------------------------
# 編集内容の反映
# ----------------------------------------
@tasks_bp.route("/tasks/<int:id>/", methods=["POST"])
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
