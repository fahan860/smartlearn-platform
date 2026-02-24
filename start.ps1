# Quick Start Script for Windows PowerShell

Write-Host "🚀 Starting LearnHub Platform..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the workspace directory
if (-not (Test-Path ".\backend") -or -not (Test-Path ".\frontend")) {
    Write-Host "❌ Error: Please run this script from the workspace root directory" -ForegroundColor Red
    exit 1
}

# Check backend .env
if (-not (Test-Path ".\backend\.env")) {
    Write-Host "⚠️  Backend .env file not found. Creating from example..." -ForegroundColor Yellow
    Copy-Item ".\backend\.env.example" ".\backend\.env"
    Write-Host "📝 Please edit backend\.env and add your MONGODB_URI and JWT_SECRET" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter after configuring .env file"
}

# Check frontend .env
if (-not (Test-Path ".\frontend\.env")) {
    Write-Host "⚠️  Frontend .env file not found. Creating from example..." -ForegroundColor Yellow
    Copy-Item ".\frontend\.env.example" ".\frontend\.env"
}

Write-Host "✅ Configuration files ready" -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "🔧 Starting Backend Server (Port 4000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; npm.cmd run dev"
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "🎨 Starting Frontend Server (Port 3000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm.cmd run dev"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "📡 Backend:  http://localhost:4000" -ForegroundColor White
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "💡 Open your browser and navigate to http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "🛑 To stop servers, close the terminal windows or press Ctrl+C in each" -ForegroundColor Gray
