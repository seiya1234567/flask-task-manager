document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const password = document.getElementById('password');
    const passwordConfirm = document.getElementById('password_confirm');
    const passwordError = document.getElementById('passwordError');
    const togglePasswordMain = document.getElementById('togglePasswordMain');
    const eyeIconMain = document.getElementById('eyeIconMain');
    const togglePasswordConfirm = document.getElementById('togglePasswordConfirm');
    const eyeIconConfirm = document.getElementById('eyeIconConfirm');

    // 初期はパスワードエラー非表示
    if (passwordError) {
        passwordError.style.display = 'none';
    }

    // パスワード表示切替
    if (togglePasswordMain && password && eyeIconMain) {
        togglePasswordMain.addEventListener('click', () => {
            const type = password.type === 'password' ? 'text' : 'password';
            password.type = type;
            eyeIconMain.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
        });
    }

    // 再入力パスワード表示切替
    if (togglePasswordConfirm && passwordConfirm && eyeIconConfirm) {
        togglePasswordConfirm.addEventListener('click', () => {
            const type = passwordConfirm.type === 'password' ? 'text' : 'password';
            passwordConfirm.type = type;
            eyeIconConfirm.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
        });
    }
                
    // メールバリデーション関数
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // パスワードバリデーション関数
    function validatePassword(pwd) {
        return pwd.length >= 8;
    }

    // エラー表示切替
    function showError(fieldId, show = true) {
        const errorElement = document.getElementById(fieldId + 'Error');
        if (errorElement) {
            errorElement.style.display = show ? 'block' : 'none';
        }
    }

    // リアルタイムでパスワード長チェック
    if (password) {
        password.addEventListener('input', function() {
            if (!validatePassword(password.value)) {
                showError('password', true);
            } else {
                showError('password', false);
            }
        });
    }

    // メールアドレスリアルタイムチェック（blur時）
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const valid = validateEmail(emailInput.value);
            if (!valid && emailInput.value !== '') {
                emailInput.classList.add('border-red-500');
                emailInput.classList.remove('border-gray-300');
            } else {
                emailInput.classList.remove('border-red-500');
                emailInput.classList.add('border-gray-300');
            }
            showError('email', !valid && emailInput.value !== '');
        });
    }

    // フォーム送信時バリデーション
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const email = emailInput ? emailInput.value : '';
            const pwd = password ? password.value : '';
            const pwdConfirm = passwordConfirm ? passwordConfirm.value : '';
            const mismatchError = document.getElementById('passwordMismatchError');

            const emailValid = validateEmail(email);
            const passwordValid = validatePassword(pwd);

            showError('email', !emailValid);
            showError('password', !passwordValid);

            if (!emailValid || !passwordValid) {
                e.preventDefault();
                return;
            }

            if (pwd !== pwdConfirm) {
                e.preventDefault();
                if (mismatchError) {
                    mismatchError.style.display = 'block'; // エラー表示
                }
                if (passwordConfirm) {
                    passwordConfirm.focus();
                }
                return;
            }
        });
    }
});

