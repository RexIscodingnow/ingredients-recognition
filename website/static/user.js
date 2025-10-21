const editBtn = document.getElementById("btn-edit-profile");
const modalEdit = document.getElementById("user-edit-modal");
const closeBtn = document.getElementById("user-edit-close");
const cancelBtn = document.getElementById("user-edit-cancel");
const user_edit_form = document.getElementById("user-edit-form");

function showMessageOnEditForm(message, isSuccess = true) {
    let msgBox = document.getElementById('form-message');

    if (!msgBox) {
        msgBox = document.createElement('p');
        msgBox.id = 'form-message';
        msgBox.style.marginTop = '10px';
        msgBox.style.fontSize = '0.9rem';
        user_edit_form.appendChild(msgBox);
    }
    msgBox.textContent = message;
    msgBox.style.color = isSuccess ? 'green' : 'red';
}

document.addEventListener("DOMContentLoaded", () => {
    const openModal = () => modalEdit.classList.add("active");
    const closeModal = () => {
        modalEdit.classList.remove("active");
        showMessageOnEditForm("");
    };

    editBtn?.addEventListener("click", openModal);
    closeBtn?.addEventListener("click", closeModal);
    cancelBtn?.addEventListener("click", closeModal);

    modalEdit?.addEventListener("click", (e) => {
        if (e.target === modalEdit) closeModal();
    });

    user_edit_form?.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        const new_password = document.getElementById('new-password').value.trim();

        if (!password) {
            showMessageOnEditForm('⚠️ 請輸入密碼才能進行更改', false);
            return;
        }
        const data = {
            username: username,
            email: email,
            password: password,
            new_password: new_password
        };

        try {
            const endpoint = '/update_profile';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                // modal.style.display = 'none';
                showMessageOnEditForm(result.message || '成功！', true);
                setTimeout(() => {
                    closeModal();
                }, 800);
            } else {
                showMessageOnEditForm(result.message || '操作失敗，請再試一次', false);
            }
        }

        catch (error) {
            console.error('登入請求失敗:', error);
            showMessageOnEditForm('伺服器錯誤，請稍後再試', false);
        }
    });
});

