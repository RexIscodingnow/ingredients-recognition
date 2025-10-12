const modal = document.getElementById('modal');
const btnLogin = document.getElementById('btn-login');
const btnRegister = document.getElementById('btn-register');
const modalClose = document.getElementById('modal-close');
const title = document.getElementById('modal-title');
const switchBtn = document.getElementById('switch-to-register');
const forgotPwdBtn = document.getElementById('switch-to-forgot-pwd');
const authForm = document.getElementById('auth-form');
const usernameGroup = document.getElementById('username-group');
const passwordForm = document.getElementById('password');

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

// 指定欄位顯示
function setModalContent(mode) {
    if (mode === 'login') {
        title.textContent = '登入';         // email + password
        usernameGroup.style.display = 'none';
        document.getElementById('password').parentElement.style.display = 'block';
        document.getElementById('email').parentElement.style.display = 'block';
        forgotPwdBtn.style.display = 'block';
        switchBtn.textContent = '前往註冊';
    } else if (mode === 'register') {       // all
        title.textContent = '註冊';
        usernameGroup.style.display = 'block';
        document.getElementById('password').parentElement.style.display = 'block';
        document.getElementById('email').parentElement.style.display = 'block';
        forgotPwdBtn.style.display = 'none';
        switchBtn.style.display = 'inline-block';
        switchBtn.textContent = '已有帳號？前往登入';
    } else if (mode === 'forgot-pwd') {     // only email
        title.textContent = '忘記密碼';
        usernameGroup.style.display = 'none';
        document.getElementById('password').parentElement.style.display = 'none';
        document.getElementById('email').parentElement.style.display = 'block';
        switchBtn.style.display = 'inline-block';
        switchBtn.textContent = '返回登入';
        forgotPwdBtn.style.display = 'none';
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


btnLogin.addEventListener('click', () => openModal('login'));
btnRegister.addEventListener('click', () => openModal('register'));
forgotPwdBtn.addEventListener('click', () => openModal('forgot-pwd'));
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

    if ((currentMode === 'register' && (!email|| !username || !password)) ||
        (currentMode === 'login' && (!email || !password)) ||
        (currentMode === 'forgot-pwd' && !email)) {
        showMessage('⚠️ 所有欄位皆為必填', false);
        return;
    }


    const data = {
        username: username,
        email: email,
        password: password
    };

    let endpoint;
    if (currentMode === 'login') {
        endpoint = '/login';
    } else if (currentMode === 'register') {
        endpoint = '/register';
    } else {
        endpoint = '/forgot-pwd';
    }

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        console.log(currentMode)

        const result = await response.json();

        if (result.success) {
            // modal.style.display = 'none';
            showMessage(result.message || '成功！', true);
            setTimeout(() => {
                clearFields();
                modal.style.display = 'none';
                if (result.redirect_url) {
                    window.location.href = result.redirect_url;
                }
            }, 2500);
        } else {
            showMessage(result.message || '操作失敗，請再試一次', false);
        }
    }

    catch (error) {
        console.error('登入請求失敗:', error);
        showMessage('伺服器錯誤，請稍後再試', false);
    }
});
