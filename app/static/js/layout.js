// 共通のヘッダーボタン処理
document.addEventListener('DOMContentLoaded', function () {
    // タスク一覧ボタン
    const tasksBtn = document.getElementById('tasksBtn');
    if (tasksBtn) {
        tasksBtn.addEventListener('click', function () {
            location.href = "/tasks";
        });
    }

    // 新規タスク作成ボタン
    const newTaskBtn = document.getElementById('newTaskBtn');
    if (newTaskBtn) {
        newTaskBtn.addEventListener('click', function () {
            location.href = "/tasks/new";
        });
    }

    // プロフィールボタン
    const profileBtn = document.getElementById('profileBtn');
    if(profileBtn) {
        profileBtn.addEventListener('click', function() {
            location.href = "/profile";
        });
    }

    // ログアウトボタン
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            openLogoutConfirmModal();
        });
    }
});

// ログアウト確認モーダルを開く
function openLogoutConfirmModal() {
    const modal = document.getElementById('confirmModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

// ログアウト確認モーダルを閉じる
function closeConfirmModal() {
    const modal = document.getElementById('confirmModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// ログアウト実行
async function executeLogout() {
    try {
        const res = await fetch('/logout', { 
            method: 'POST',
            credentials: 'include'
        });

        closeConfirmModal();

        if (res.ok) {
            // 完了モーダル表示
            const modal = document.getElementById('logoutSuccessModal');
            if (modal) {
                modal.classList.remove('hidden');
                modal.classList.add('flex');
            }
        } else {
            alert('ログアウトに失敗しました');
        }
    } catch {
        alert('通信エラーが発生しました');
    }
}

// 完了モーダルを閉じてログインへ
function closeLogOutSuccessModal() {
    const modal = document.getElementById('logoutSuccessModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
    location.href = '/login';
}

