from app.models import User

def validate_register(*, username, email, password, password_confirm):

    errors = {}

    if not username:
        errors["username"] = "ユーザー名は必須です"
    # ユーザー名の重複チェック
    else:
        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            errors["username"] = "ユーザー名はすでに使われています"

    if not email:
        errors["email"] = "メールアドレスは必須です"
    # メールアドレスの重複チェック
    else:
        existing_email = User.query.filter_by(
            email=email
        ).first()
        
        if existing_email:
            errors["email"] = "メールアドレスはすでに使われています"

    if not password:
        errors["password"] = "パスワードは必須です"
    elif len(password) < 8:
        errors["password"] = "パスワードは8文字以上にしてください"
    
    if not password_confirm:
        errors["password_confirm"] = "確認用のパスワードは必須です"

    elif password != password_confirm:
        errors["password_confirm"] = "パスワードが一致しません"

    return errors