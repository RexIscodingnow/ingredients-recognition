const searchInput = document.getElementById("q");
const searchBtn = document.getElementById("search-btn")

searchBtn.addEventListener("click", async () => {
    const query = document.getElementById("q").value.trim();

    try {
        const response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ q: query })
        });

        const result = await response.json();

        window.location.href = `/result?token=${encodeURIComponent(result.token)}`;
    } catch (err) {
        console.error("搜尋失敗:", err);
        alert("搜尋時發生錯誤，請稍後再試。");
    }
});

searchInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();   // 防止表單提交或重新整理
        searchBtn.click();
    }
});

