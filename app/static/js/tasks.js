//idを渡すグローバル変数を定義
let currentDeleteTaskId = null;

// 簡単なインタラクティブ機能
document.addEventListener('DOMContentLoaded', function () {
    // タスクカードのホバー効果
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach((card) => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-4px)';
        });
        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // ボタンクリックイベント
    const buttons = document.querySelectorAll('.action-btn');
    buttons.forEach((button) => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const action = this.dataset.action;
            const taskId = this.dataset.taskId;

            if (!action || !taskId) return;

            if (action === 'edit')
            {
                location.href = `/tasks/${taskId}/edit`;
            } 
            else if (action === 'delete') {
            // 削除モーダルを開くなど
            confirmDelete(taskId);
            }
            else if (action === 'description')
            {
                const desc = document.getElementById('desc-' + taskId);
                if (desc) {
                    desc.classList.toggle('hidden');
                    // ボタンのテキストを切り替えたい場合は以下を使う
                    const icon = this.querySelector('i');
                    if (desc.classList.contains('hidden')) {
                        this.innerHTML = '<i class="fas fa-eye mr-1"></i>詳細';
                    } else {
                        this.innerHTML = '<i class="fas fa-eye-slash mr-1"></i>閉じる';
                    }
                }
            }
        });
    });

    // 期限日の色付け
    document.querySelectorAll('.task-status').forEach(elem => {
        const status = elem.dataset.status;  // 例: '進行中', '完了' など
        const dueDateElem = document.getElementById('deadline-' + elem.dataset.taskId);
        if (!dueDateElem) return;

        const dueDateStr = dueDateElem.textContent.trim();
        const now = new Date();
        const deadline = new Date(dueDateStr);
        const diffDays = (deadline - now) / (1000 * 60 * 60 * 24);

        // 完了タスクはスキップ
        if (status === '完了') return;

        if (diffDays >= 0 && diffDays <= 7) {
            // 今日から7日以内の期限は赤くする
            dueDateElem.classList.add('text-red-600');
        } else if (diffDays < 0) {
            // 期限過ぎも赤くする（任意）
            dueDateElem.classList.add('text-red-600');
        }
    });

    // ESCキーでモーダルを閉じる
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeDeleteModal();
        }
    });
});

// 削除確認モーダル表示
function confirmDelete(taskId) {
    currentDeleteTaskId = taskId; // タスクIDを保存
    const deleteModal = document.getElementById('deleteModal');
    if (deleteModal) {
        deleteModal.classList.remove('hidden');
        deleteModal.classList.add('flex');
    }
}

// タスク削除モーダル非表示
function closeDeleteModal() {
    currentDeleteTaskId =  null; // タスクIDを削除
    const deleteModal = document.getElementById('deleteModal');
    if (deleteModal) {
        deleteModal.classList.add('hidden');
        deleteModal.classList.remove('flex');
    }
}

// 成功通知モーダル非表示
function closeSuccessModal() {
    const deleteSuccessModal = document.getElementById('deleteSuccessModal');
    if (deleteSuccessModal) {
        deleteSuccessModal.classList.add('hidden');
        deleteSuccessModal.classList.remove('flex');
    }
    location.reload(); // 画面を更新する
}

// タスク削除実行
async function executeDelete(){
    if (!currentDeleteTaskId) {
        alert("削除するタスクが選択されていません。");
        return;
    }
    try
    {
        const response = await fetch(`/tasks/${currentDeleteTaskId}/delete`,
        {
            method:"POST",
            credentials: 'include'
        });
        if (response.ok)
        {
            // 削除確認モーダルを閉じる
            closeDeleteModal();

            // 成功モーダルを開く
            const deleteSuccessModal = document.getElementById('deleteSuccessModal');
            if (deleteSuccessModal) {
                deleteSuccessModal.classList.remove('hidden');
                deleteSuccessModal.classList.add('flex');
            }
        }
        else
        {
            alert('削除に失敗しました');
        }
    }
    catch
    {
        alert('通信エラーが発生しました');
    }
}

