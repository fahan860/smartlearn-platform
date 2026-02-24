@echo off
echo.
echo ========================================
echo   LearnHub Platform - Quick Start
echo ========================================
echo.

REM Check if in correct directory
if not exist "backend\" (
    echo Error: Please run this script from the workspace root directory
    pause
    exit /b 1
)

if not exist "frontend\" (
    echo Error: Please run this script from the workspace root directory
    pause
    exit /b 1
)

REM Check backend .env
if not exist "backend\.env" (
    echo Creating backend .env from example...
    copy "backend\.env.example" "backend\.env"
    echo.
    echo Please edit backend\.env and add your MONGODB_URI and JWT_SECRET
    echo.
    pause
)

REM Check frontend .env
if not exist "frontend\.env" (
    echo Creating frontend .env from example...
    copy "frontend\.env.example" "frontend\.env"
)

echo Starting Backend Server on Port 4000...
start "LearnHub Backend" cmd /k "cd backend && npm run dev"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server on Port 3000...
start "LearnHub Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Servers Starting!
echo ========================================
echo.
echo Backend:  http://localhost:4000
echo Frontend: http://localhost:3000
echo.
echo Open your browser and go to:
echo http://localhost:3000
echo.
echo Press any key to exit (servers will keep running)...
pause > nul
