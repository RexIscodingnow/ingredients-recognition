const modal = document.getElementById('modal');
const btnLogin = document.getElementById('btn-login');
const btnRegister = document.getElementById('btn-register');
const modalClose = document.getElementById('modal-close');
const title = document.getElementById('modal-title');
const switchBtn = document.getElementById('switch-to-register');
const authForm = document.getElementById('auth-form');
const logoutForm = document.getElementById('logout-form');
const usernameGroup = document.getElementById('username-group');

let currentMode = 'login';


function clearFields() {
    document.getElementById('username').value = '';
    document.getElementById('email').value = '';
    document.getElementById('password').value = '';
}

function showMessage(message, isSuccess = true) {
    let msgBox = document.getElementById('form-message');

    if (!msgBox) {
        msgBox = document.createElement('p');
        msgBox.id = 'form-message';
        msgBox.style.marginTop = '10px';
        msgBox.style.fontSize = '0.9rem';
        authForm.appendChild(msgBox);
    }
    msgBox.textContent = message;
    msgBox.style.color = isSuccess ? 'green' : 'red';
}

function setModalContent(mode) {
    if (mode === 'login') {
        title.textContent = '登入';
        usernameGroup.style.display = 'none';
        switchBtn.textContent = '前往註冊';
    } else {
        title.textContent = '註冊';
        usernameGroup.style.display = 'block';
        switchBtn.textContent = '已有帳號？前往登入';
    }

    showMessage("");
}

// 開啟對話框並設定模式
function openModal(mode) {
    modal.style.display = 'flex';
    currentMode = mode;
    setModalContent(mode);
    clearFields(); // 每次開啟或切換模式時，清除欄位保持乾淨
}


/*
function openModal(mode) {
    modal.style.display = 'flex';
    currentMode = mode;

    if (mode === 'login') {
        title.textContent = '登入';
        usernameGroup.style.display = 'none';
        switchBtn.textContent = '前往註冊';
        authForm.onsubmit = (e) => {
            e.preventDefault();
            // alert('登入成功：' + document.getElementById('email').value);
            clearFields();
            modal.style.display = 'none';
        }
    } else {
        title.textContent = '註冊';
        usernameGroup.style.display = 'block';
        switchBtn.textContent = '已有帳號？前往登入';
        authForm.onsubmit = (e) => {
            e.preventDefault();
            // alert('註冊完成：' + document.getElementById('username').value);
            clearFields();
            modal.style.display = 'none';
        }
    }
}
*/

btnLogin.addEventListener('click', () => openModal('login'));
btnRegister.addEventListener('click', () => openModal('register'));
modalClose.addEventListener('click', () => modal.style.display='none');
switchBtn.addEventListener('click', () => {
    openModal(currentMode === 'login' ? 'register' : 'login');
});
modal.addEventListener('click', e => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

authForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!email || !password || (currentMode === 'register' && !username)) {
        showMessage('⚠️ 所有欄位皆為必填', false);
        return;
    }

    const data = {
        username: username,
        email: email,
        password: password
    };

    const endpoint = currentMode === 'login' ? '/login' : '/register';
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        console.log(currentMode)

        const result = await response.json();
        // alert(result.message);

        if (result.success) {
            // modal.style.display = 'none';
            showMessage(result.message || '成功！', true);
            setTimeout(() => {
                clearFields();
                modal.style.display = 'none';
                if (result.redirect_url) {
                    window.location.href = result.redirect_url;
                }
            }, 800);
        } else {
            showMessage(result.message || '操作失敗，請再試一次', false);
        }
    }

    catch (error) {
        console.error('登入請求失敗:', error);
        showMessage('伺服器錯誤，請稍後再試', false);
    }
});
