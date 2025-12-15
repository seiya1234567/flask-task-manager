document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.getElementById('loginBtn');

    // パスワード表示切替
    if (togglePassword && password && eyeIcon) {
        togglePassword.addEventListener('click', function() {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);

            if (type === 'password') {
                eyeIcon.className = 'fas fa-eye';
            } else {
                eyeIcon.className = 'fas fa-eye-slash';
            }
        });
    }

    if (loginForm && loginBtn) {
        loginForm.addEventListener('submit', () => {
            const loginSpinner = document.getElementById('loginSpinner');
            if (loginSpinner) {
                loginSpinner.classList.remove('hidden');
            }
            loginBtn.disabled = true;  
        });

        window.addEventListener("pageshow", function (event) {
            if (event.persisted) {
                const loginSpinner = document.getElementById('loginSpinner');
                if (loginSpinner) {
                    loginSpinner.classList.add('hidden');
                }
                loginBtn.disabled = false;  
            }
        });
    }
});

