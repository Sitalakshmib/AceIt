# AceIt Manual Launch Script (Reliable)
# Usage: Right-click > Run with PowerShell

Write-Host "🚀 Starting AceIt System..." -ForegroundColor Green

# 1. Start Backend
Write-Host "Starting Backend on Port 8000..."
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "conda activate AceIt && cd aceit_backend && python -m uvicorn main:app --reload --port 8000" -WindowStyle Normal

# 2. Start Frontend
Write-Host "Starting Frontend on Port 5173..."
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "cd aceit-frontend && npm run dev" -WindowStyle Normal

Write-Host "✅ Launch commands sent! check the new windows." -ForegroundColor Cyan
Write-Host "Access at: http://localhost:5173" -ForegroundColor Yellow
Read-Host "Press Enter to exit..."
