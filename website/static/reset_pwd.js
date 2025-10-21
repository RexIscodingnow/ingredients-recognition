const form = document.querySelector("form");

form.addEventListener("submit", (e) => {
    
    const newPwd = document.getElementById("new-password").value.trim();
    const confirmPwd = document.getElementById("confirm-password").value.trim();
    
    if (newPwd.value !== confirmPwd.value) {
        e.preventDefault();
        alert("新密碼與確認密碼不一致！");
        return;
    }
});

