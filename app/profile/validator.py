from app.models import User

def validate_profile(*, username, email, user_id):
    errors = {}

    if not username:
        errors["username"] = "ユーザー名は必須です"
    else:
        existing_username = User.query.filter(
            User.username == username,
            User.id != user_id
        ).first()
        if existing_username:
            errors["username"] = "ユーザー名はすでに使われています"

    if not email:
        errors["email"] = "メールアドレスは必須です"
    else:
        existing_email = User.query.filter(
            User.email == email,
            User.id != user_id
        ).first()
        if existing_email:
            errors["email"] = "メールアドレスはすでに使われています"

    return errors

def validate_password_change(*, current_password, new_password, confirm_password, user):
    errors = {}

    if not user.check_password(current_password):
        errors["current_password"] = "現在のパスワードが正しくありません"

    if not new_password:
        errors["new_password"] = "新しいパスワードを入力してください"
    elif len(new_password) < 8:
        errors["new_password"] = "パスワードは8文字以上にしてください"
    elif user.check_password(new_password):
        errors["new_password"] = "現在のパスワードと同じものは使用できません"

    if not confirm_password:
        errors["confirm_password"] = "確認用パスワードを入力してください"
    elif new_password != confirm_password:
        errors["confirm_password"] = "パスワードが一致しません"

    return errors
