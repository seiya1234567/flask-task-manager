from app.models import User

def validate_profile(*, username, email, user_id):
    """
    プロフィール編集時の入力値検証を行う

    - username / email の必須チェック
    - 他ユーザーとの重複チェック（自分自身は除外）
    - エラーは {field: error_code} の形式で返却する
    """
    errors = {}

    # --- username validation ---
    if not username:
        # 未入力
        errors["username"] = "required"
    else:
        # 自分以外で同じユーザー名が存在するかチェック
        existing_username = User.query.filter(
            User.username == username,
            User.id != user_id
        ).first()
        if existing_username:
            errors["username"] = "duplicate"

    # --- email validation ---
    if not email:
        # 未入力
        errors["email"] = "required"
    else:
        # 自分以外で同じメールアドレスが存在するかチェック
        existing_email = User.query.filter(
            User.email == email,
            User.id != user_id
        ).first()
        if existing_email:
            errors["email"] = "duplicate"

    return errors


def validate_password_change(*, current_password, new_password, new_password_confirm, user):
    """
    パスワード変更時の入力値検証を行う

    - 現在のパスワード一致確認
    - 新パスワードの必須・長さチェック
    - 過去（現在）パスワードとの同一チェック
    - 確認用パスワードとの一致確認
    """
    errors = {}

    # --- current password validation ---
    if not current_password:
        # 未入力
        errors["current_password"] = "required"
    elif not user.check_password(current_password):
        # 現在のパスワードが一致しない
        errors["current_password"] = "mismatch"

    # --- new password validation ---
    if not new_password:
        # 未入力
        errors["new_password"] = "required"
    elif len(new_password) < 8:
        # 文字数不足
        errors["new_password"] = "too_short"
    elif user.check_password(new_password):
        # 現在のパスワードと同一
        errors["new_password"] = "already_used"

    # --- new password confirm validation ---
    if not new_password_confirm:
        # 未入力
        errors["new_password_confirm"] = "required"
    elif new_password != new_password_confirm:
        # 新パスワードと不一致
        errors["new_password_confirm"] = "mismatch"

    return errors
