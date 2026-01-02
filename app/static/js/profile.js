document.addEventListener('DOMContentLoaded', function() {

    // -----------------------
    // DOM取得
    // -----------------------
    const profileForm = document.getElementById('profileForm');
    const passwordForm = document.getElementById('passwordForm');

    const emailInput = document.getElementById('email');

    const currentPassword = document.getElementById('current_password');
    const newPassword = document.getElementById('new_password');
    const newPasswordConfirm = document.getElementById('new_password_confirm');
    const mismatchError = document.getElementById('passwordMismatchError');

    const passwordError = document.getElementById('passwordError');

    // パスワード表示切替ボタン
    const toggleCurrentPassword = document.getElementById('toggleCurrentPassword');
    const toggleNewPassword = document.getElementById('toggleNewPassword');
    const toggleNewPasswordConfirm = document.getElementById('toggleNewPasswordConfirm');
    const currentPasswordEyeIcon = document.getElementById('currentPasswordEyeIcon');
    const newPasswordEyeIcon = document.getElementById('newPasswordEyeIcon');
    const newPasswordConfirmEyeIcon = document.getElementById('newPasswordConfirmEyeIcon');

    // -----------------------
    // バリデーション関数
    // -----------------------
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validatePassword(pwd) {
        return pwd.length >= 8;
    }

    // -----------------------
    // メールアドレスのリアルタイムバリデーション
    // -----------------------
    if (emailInput) {
        emailInput.addEventListener('blur', function () {
            const valid = validateEmail(emailInput.value);

            if (!valid && emailInput.value !== "") {
                emailInput.classList.add('border-red-500');
                emailInput.classList.remove('border-gray-300');
            } else {
                emailInput.classList.remove('border-red-500');
                emailInput.classList.add('border-gray-300');
            }
        });
    }

    // -----------------------
    // パスワード表示切替
    // -----------------------
    // 現在のパスワード表示切替
    if (toggleCurrentPassword && currentPassword && currentPasswordEyeIcon) {
        toggleCurrentPassword.addEventListener('click', function() {
            const type = currentPassword.getAttribute('type') === 'password' ? 'text' : 'password';
            currentPassword.setAttribute('type', type);
            
            if (type === 'password') {
                currentPasswordEyeIcon.className = 'fas fa-eye';
            } else {
                currentPasswordEyeIcon.className = 'fas fa-eye-slash';
            }
        });
    }

    // 新しいパスワード表示切替
    if (toggleNewPassword && newPassword && newPasswordEyeIcon) {
        toggleNewPassword.addEventListener('click', function() {
            const type = newPassword.getAttribute('type') === 'password' ? 'text' : 'password';
            newPassword.setAttribute('type', type);
            
            if (type === 'password') {
                newPasswordEyeIcon.className = 'fas fa-eye';
            } else {
                newPasswordEyeIcon.className = 'fas fa-eye-slash';
            }
        });
    }

    // 新しいパスワード（確認）表示切替
    if (toggleNewPasswordConfirm && newPasswordConfirm && newPasswordConfirmEyeIcon) {
        toggleNewPasswordConfirm.addEventListener('click', function() {
            const type = newPasswordConfirm.getAttribute('type') === 'password' ? 'text' : 'password';
            newPasswordConfirm.setAttribute('type', type);
            
            if (type === 'password') {
                newPasswordConfirmEyeIcon.className = 'fas fa-eye';
            } else {
                newPasswordConfirmEyeIcon.className = 'fas fa-eye-slash';
            }
        });
    }

    // -----------------------
    // パスワード長チェック
    // -----------------------
    if (passwordError) {
        passwordError.style.display = "none";
    }

    if (newPassword) {
        newPassword.addEventListener('input', function () {
            const valid = validatePassword(newPassword.value);
            if (!valid && newPassword.value.trim() !== '') {
                if (passwordError) {
                    passwordError.style.display = "block";
                }
                newPassword.classList.add('border-red-500');
                newPassword.classList.remove('border-gray-300');
            } else {
                if (passwordError) {
                    passwordError.style.display = "none";
                }
                newPassword.classList.remove('border-red-500');
                newPassword.classList.add('border-gray-300');
            }
            // パスワード一致チェックも実行
            checkPasswordMatch();
        });
    }

    // パスワード一致チェック（リアルタイム）
    function checkPasswordMatch() {
        if (!newPassword || !newPasswordConfirm) return;
        
        const pwd = newPassword.value;
        const pwdConfirm = newPasswordConfirm.value;
        const mismatchError = document.getElementById('passwordMismatchError');
        
        if (pwdConfirm.trim() === '') {
            if (mismatchError) {
                mismatchError.style.display = 'none';
            }
            newPasswordConfirm.classList.remove('border-red-500');
            newPasswordConfirm.classList.add('border-gray-300');
            return;
        }
        
        if (pwd !== pwdConfirm) {
            if (mismatchError) {
                mismatchError.style.display = 'block';
            }
            newPasswordConfirm.classList.add('border-red-500');
            newPasswordConfirm.classList.remove('border-gray-300');
        } else {
            if (mismatchError) {
                mismatchError.style.display = 'none';
            }
            newPasswordConfirm.classList.remove('border-red-500');
            newPasswordConfirm.classList.add('border-gray-300');
        }
    }

    if (newPasswordConfirm) {
        newPasswordConfirm.addEventListener('input', function() {
            checkPasswordMatch();
        });
    }

    // -----------------------
    // パスワードフォーム送信時チェック
    // -----------------------
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            const pwd = newPassword ? newPassword.value : '';
            const pwdConfirm = newPasswordConfirm ? newPasswordConfirm.value : '';

            if (!validatePassword(pwd)) {
                e.preventDefault();
                if (passwordError) {
                    passwordError.style.display = "block";
                }
                return;
            }

            if (pwd !== pwdConfirm) {
                e.preventDefault();
                if (mismatchError) {
                    mismatchError.style.display = 'block'; // エラー表示
                }
                if (newPasswordConfirm) {
                    newPasswordConfirm.focus();
                }
                return;
            }
        });
    }

    // -----------------------------
    // アカウント削除モーダル制御
    // -----------------------------

    // モーダルを開く
    function openDeleteModal() {
        const modal = document.getElementById('deleteModal');
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
    }

    // モーダルを閉じる
    function closeDeleteModal() {
        const modal = document.getElementById('deleteModal');
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    }

    // アカウント削除実行
    async function executeAccountDelete() {
        try {
            const res = await fetch('/delete_account', {
                method: 'POST',
                credentials: 'include'
            });

            closeDeleteModal();

            if (res.ok) {
                const modal = document.getElementById('deleteSuccessModal');
                if (modal) {
                    modal.classList.remove('hidden');
                    modal.classList.add('flex');
                }
            } else {
                alert('アカウント削除に失敗しました');
            }
        } catch {
            alert('通信エラーが発生しました');
        }
    }

    // 完了モーダルを閉じてログイン画面へ
    function closeSuccessModal() {
        const modal = document.getElementById('deleteSuccessModal');
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
        location.href = '/login';
    }

    // ボタン押下イベント
    const accountDeleteBtn = document.getElementById('accountDeleteBtn');
    if (accountDeleteBtn) {
        accountDeleteBtn.addEventListener('click', openDeleteModal);
    }

    window.showModal = showModal;
    window.openDeleteModal = openDeleteModal;
    window.closeDeleteModal = closeDeleteModal;
    window.executeAccountDelete = executeAccountDelete;
    window.closeSuccessModal = closeSuccessModal;
});

