# 設置錯誤動作為繼續，以防個別指令出錯直接跳出
$ErrorActionPreference = "Continue"
$RedisConfigFile = "Redis-x64-3.2.100\redis.windows.conf" 
$RedisExecutionFile = "Redis-x64-3.2.100\redis-server.exe"
$PythonApplicationFile = "website\app.py"


Write-Host "正在準備啟動服務..." -ForegroundColor Cyan

# 1. 檢查 Redis 執行檔是否存在
if (Test-Path $RedisExecutionFile) {
    Write-Host "正在啟動 Redis Server (同一視窗)..." -ForegroundColor Green

    # 1. 使用 -NoNewWindow 讓它不跳出新視窗
    # 2. 使用 -PassThru 把 Redis 的程序物件存入變數 $redisProcess，以便稍後關閉
    $redisProcess = Start-Process -FilePath $RedisExecutionFile -ArgumentList $RedisConfigFile -NoNewWindow -PassThru
} else {
    Write-Host "錯誤: 在當前目錄找不到 '$($RedisExecutionFile)'。" -ForegroundColor Red
    Write-Host "請確保您在 Redis 的資料夾中執行此腳本，或者修正路徑。" -ForegroundColor Yellow
    exit
}

# 2. 等待幾秒鐘，確保 Redis 已經完全啟動並準備好接受連線
Write-Host "等待 Redis 初始化 (等待 2 秒)..." -ForegroundColor Gray
Start-Sleep -Seconds 2

# 3. 檢查 app.py 是否存在並執行
if (Test-Path $PythonApplicationFile) {
    Write-Host "正在啟動 Python Application..." -ForegroundColor Green
    Write-Host "--------------------------------" -ForegroundColor Gray
    Write-Host "提示：按下 CTRL+C 停止時，腳本會嘗試自動關閉 Redis" -ForegroundColor Yellow
    
    # 使用 try...finally 確保 Python 結束後會執行關閉 Redis 的動作
    try {
        python $PythonApplicationFile
    } finally {
        # 當 Python 結束 (或出錯) 時執行這裡
        if ($redisProcess) {
            Write-Host "`n正在關閉 Redis Server (PID: $($redisProcess.Id))..." -ForegroundColor Cyan
            Stop-Process -Id $redisProcess.Id -ErrorAction SilentlyContinue
        }
    }
} else {
    # 修正：移除中文句號與單引號，避免編碼誤判導致語法錯誤
    Write-Host "Error: 找不到 $($PythonApplicationFile) (File not found)" -ForegroundColor Red
}
