/**
 * Forms settings on the user page
 */
// 1. For edit user's profile
const editBtn = document.getElementById("btn-edit-profile");
const modalEdit = document.getElementById("user-edit-modal");
const closeBtn = document.getElementById("user-edit-close");
const cancelBtn = document.getElementById("user-edit-cancel");
const user_edit_form = document.getElementById("user-edit-form");

// 2. For upload the photos
const photoInput = document.getElementById("photos");
const selectBtn = document.getElementById("select-btn");
const dropArea = document.getElementById("drop-area");
const uploadForm = document.getElementById("upload-form");
const uploadStatus = document.getElementById("upload-status");
const previewContainer = document.getElementById("preview-container");
const clearBtn = document.getElementById("clear-imgs-btn");
// const detected = document.getElementById("detected");
// const show_detected_ingreds = document.getElementById("show-detected-ingreds");
// const show_recommend_recipes = document.getElementById("show-recommend-recipes");
const MAX_PHOTOS = 5;

let selectedFiles = [];


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

// ==============================================================================
// ==============================================================================

function renderPreview() {
    previewContainer.innerHTML = "";

    selectedFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = e => {
            const div = document.createElement("div");
            div.classList.add("preview-item");

            const img = document.createElement("img");
            img.src = e.target.result;

            const btn = document.createElement("button");
            btn.classList.add("remove-btn");
            btn.innerHTML = "✕";
            btn.addEventListener("click", () => removeImage(index));

            div.appendChild(img);
            div.appendChild(btn);
            previewContainer.appendChild(div);
        };
        reader.readAsDataURL(file);
    });

    updateFileInput();
}


function handleFiles(files) {
    const newFiles = files.filter(f => f.type.startsWith("image/"));
    console.log(selectedFiles.length + newFiles.length);

    if (selectedFiles.length + newFiles.length > MAX_PHOTOS) {
        alert(`最多只能上傳 ${MAX_PHOTOS} 張圖片！`);
        return;
    }
    selectedFiles = selectedFiles.concat(newFiles);
    renderPreview();
}


function removeImage(index) {
    selectedFiles.splice(index, 1);
    renderPreview();
}


function updateFileInput() {
    // 用 DataTransfer 重新建立 FileList
    const dataTransfer = new DataTransfer();
    selectedFiles.forEach(file => dataTransfer.items.add(file));
    photoInput.files = dataTransfer.files;
}

// ==============================================================================
// ==============================================================================

/* The edit form for the user's profile */
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

// ==============================================================================
// ==============================================================================

/* 貼上圖片 */
document.addEventListener("paste", (e) => {
    const items = e.clipboardData.items;
    const files = [];
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.type.startsWith("image/")) {
            files.push(item.getAsFile());
        }
    }
    if (files.length > 0) {
        handleFiles(files);
    }
});

selectBtn.addEventListener("click", () => photoInput.click());
photoInput.addEventListener("change", (e) => {
    handleFiles(Array.from(e.target.files));
});

/* 清除所有圖片 */
clearBtn.addEventListener("click", () => {
    selectedFiles = [];
    previewContainer.innerHTML = "";
    photoInput.value = "";
});

/* 拖曳圖片 */
["dragenter", "dragover"].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropArea.classList.add("dragover");
    });
});

["dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropArea.classList.remove("dragover");
    });
});

dropArea.addEventListener("drop", (e) => {
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
});

uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (selectedFiles.length === 0) {
        e.preventDefault();
        alert("請至少上傳一張圖片！");
        return;
    }

    uploadStatus.textContent = "上傳中，請稍候...";
    const formData = new FormData(uploadForm);

    try {
        const response = await fetch("/upload_ingred", {
            method: "POST", body: formData
        });
        const result = await response.json();

        // if (response.redirected) {
        if (result.success) {
            uploadStatus.textContent = "上傳成功！";
            selectedFiles = [];
            previewContainer.innerHTML = "";
            photoInput.value = "";

            let recommend_ids = result.detect_result["recommend_ids"];

            setTimeout(async () => {
                try {
                    if (recommend_ids.length === 0) {
                        alert("抱歉！目標的食材與食譜尚未收錄");
                    }

                    const response = await fetch("/search", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ q: recommend_ids })
                    });
 
                    const result = await response.json();
                    window.location.href = `/result?token=${encodeURIComponent(result.token)}`;
                } catch (err) {
                    console.error("搜尋失敗:", err);
                    alert("搜尋時發生錯誤，請稍後再試。");
                }
            }, 1500);

        } else {
            uploadStatus.textContent = "上傳失敗，請稍後再試。";
        }
    } catch (err) {
        console.error(err);
        uploadStatus.textContent = "上傳失敗，請稍後再試。";
    }
});

