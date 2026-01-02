from app.models import User

def validate_register(*, username, email, password, password_confirm):
    """
    新規ユーザー登録時の入力値検証を行う

    - username / email / password の必須チェック
    - username / email の重複チェック
    - パスワードの最低文字数チェック
    - パスワードと確認用パスワードの一致確認
    - エラーは {field: error_code} の形式で返却する
    """
    errors = {}

    # --- username validation ---
    if not username:
        # ユーザー名未入力
        errors["username"] = "required"
    else:
        # 既に同じユーザー名が存在するかチェック
        existing_user = User.query.filter_by(
            username=username
        ).first()
        if existing_user:
            errors["username"] = "duplicate"

    # --- email validation ---
    if not email:
        # メールアドレス未入力
        errors["email"] = "required"
    else:
        # 既に同じメールアドレスが存在するかチェック
        existing_email = User.query.filter_by(
            email=email
        ).first()
        if existing_email:
            errors["email"] = "duplicate"

    # --- password validation ---
    if not password:
        # パスワード未入力
        errors["password"] = "required"
    elif len(password) < 8:
        # 最低文字数未満
        errors["password"] = "too_short"

    # --- password confirm validation ---
    if not password_confirm:
        # 確認用パスワード未入力
        errors["password_confirm"] = "required"
    elif password != password_confirm:
        # パスワードと確認用パスワードが一致しない
        errors["password_confirm"] = "mismatch"

    return errors
