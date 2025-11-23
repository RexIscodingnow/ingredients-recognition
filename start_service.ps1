$ErrorActionPreference = "Continue"
$RedisConfigFile = "Redis-x64-3.2.100\redis.windows.conf" 
$RedisExecutionFile = "Redis-x64-3.2.100\redis-server.exe"
$PythonApplicationFile = "website\app.py"

Write-Host "Preparing to start services..." -ForegroundColor Cyan

if (Test-Path $RedisExecutionFile) {
    Write-Host "Starting Redis Server..." -ForegroundColor Green

    $redisProcess = Start-Process -FilePath $RedisExecutionFile -ArgumentList $RedisConfigFile -NoNewWindow -PassThru
} else {
    Write-Host "Error: '$($RedisExecutionFile)' not found in the current directory." -ForegroundColor Red
    Write-Host "Please ensure you are running this script in the Redis folder, or correct the path." -ForegroundColor Yellow
    exit
}

Write-Host "Waiting for Redis initialization (2s)..." -ForegroundColor Gray
Start-Sleep -Seconds 2

if (Test-Path $PythonApplicationFile) {
    Write-Host "Starting Python Application..." -ForegroundColor Green
    Write-Host "--------------------------------" -ForegroundColor Gray
    Write-Host "Hint: When stopping with CTRL+C, the script will attempt to auto-close Redis." -ForegroundColor Yellow

    try {
        python $PythonApplicationFile

        if ($LASTEXITCODE -ne 0) {
            throw "Python application exited with error code: $LASTEXITCODE"
        }
    } catch {
        Write-Host "`nPython Execution Error:" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    } finally {
        if ($redisProcess) {
            Write-Host "`nClosing Redis Server (PID: $($redisProcess.Id))..." -ForegroundColor Cyan
            Stop-Process -Id $redisProcess.Id -ErrorAction SilentlyContinue
        }
    }
} else {
    Write-Host "Error: $($PythonApplicationFile) not found." -ForegroundColor Red
}
