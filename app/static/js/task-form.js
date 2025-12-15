document.addEventListener('DOMContentLoaded', function () {
    // フォーム要素にフォーカス効果を追加
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
        });
    });

    // フォーム送信時の確認
    function openRegisterConfirmModal() {
        const modal = document.getElementById('registerConfirmModal');
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
    }

    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // フォーム送信停止
            openRegisterConfirmModal(); // モーダルを表示
        });
    }

    // タイトル入力時のリアルタイムバリデーション
    const titleInput = document.getElementById('title');
    if (titleInput) {
        titleInput.addEventListener('input', function() {
            if (this.value.trim().length > 0) {
                this.style.borderColor = '#10b981';
            } else {
                this.style.borderColor = '#d1d5db';
            }
        });
    }
});

async function executeRegister() {
    const form = document.querySelector('form');
    if (!form) return;

    const actionUrl = form.getAttribute('action');
    const formData = new FormData(form);

    try {
        const response = await fetch(actionUrl, {
            method: "POST",
            body: formData,
            credentials: 'include'
        });

        if (response.ok) {
            closeRegisterConfirmModal();

            // 更新完了モーダルを表示
            const registerSuccessModal = document.getElementById('registerSuccessModal');
            if (registerSuccessModal) {
                registerSuccessModal.classList.remove('hidden');
                registerSuccessModal.classList.add('flex');
            }
        } else {
            alert("更新に失敗しました");
        }
    } catch (err) {
        alert("通信エラーが発生しました");
    }
}

// 確認モーダル非表示
function closeRegisterConfirmModal() {
    const modal = document.getElementById('registerConfirmModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// 成功モーダル非表示
function closeSuccessModal() {
    const registerSuccessModal = document.getElementById('registerSuccessModal');
    if (registerSuccessModal) {
        registerSuccessModal.classList.add('hidden');
        registerSuccessModal.classList.remove('flex');
    }
    window.location.href = "/tasks";
}

