// フォームのインタラクティブ機能
document.addEventListener('DOMContentLoaded', function() {

    // 優先度の色表示
    const prioritySelect = document.getElementById('priority');
    if (prioritySelect) {
        prioritySelect.addEventListener('change', function() {
            this.classList.remove('priority-high', 'priority-medium', 'priority-low');
            if (this.value === '高') {
                this.classList.add('priority-high');
            } else if (this.value === '中') {
                this.classList.add('priority-medium');
            } else if (this.value === '低') {
                this.classList.add('priority-low');
            }
        });

        // 初期状態で優先度の色を設定
        if (prioritySelect.value === '高') {
            prioritySelect.classList.add('priority-high');
        } else if (prioritySelect.value === '中') {
            prioritySelect.classList.add('priority-medium');
        } else if (prioritySelect.value === '低') {
            prioritySelect.classList.add('priority-low');
        }
    }

    // フォーム送信時の確認
    function openUpdateConfirmModal() {
        const modal = document.getElementById('updateConfirmModal');
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
    }

    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // フォーム送信停止
            openUpdateConfirmModal(); // モーダルを表示
        });
    }
});

function closeUpdateConfirmModal() {
    const modal = document.getElementById('updateConfirmModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// 更新実行
async function executeUpdate() {
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
            closeUpdateConfirmModal();

            // 更新完了モーダルを表示
            const updateSuccessModal = document.getElementById('updateSuccessModal');
            if (updateSuccessModal) {
                updateSuccessModal.classList.remove('hidden');
                updateSuccessModal.classList.add('flex');
            }
        } else {
            alert("更新に失敗しました");
        }
    } catch (err) {
        alert("通信エラーが発生しました");
    }
}

// 成功モーダル非表示
function closeSuccessModal() {
    const updateSuccessModal = document.getElementById('updateSuccessModal');
    if (updateSuccessModal) {
        updateSuccessModal.classList.add('hidden');
        updateSuccessModal.classList.remove('flex');
    }
    window.location.href = "/tasks";
}

