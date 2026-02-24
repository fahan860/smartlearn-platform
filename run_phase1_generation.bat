@echo off
REM Smart Learning Platform - Phase 1 Data Generation
REM Windows Batch Script

echo ======================================================================
echo Smart Learning Platform - Phase 1: Data Generation
echo ======================================================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
cd simulator
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
cd ..

echo.
echo [3/4] Generating synthetic data...
python simulator/src/data_generator.py
if %errorlevel% neq 0 (
    echo ERROR: Data generation failed
    exit /b 1
)

echo.
echo [4/4] Verifying generated files...
if exist "data\raw\users\users_*.json" (
    echo   [OK] Users data generated
) else (
    echo   [ERROR] Users data missing
)

if exist "data\raw\courses\courses_*.json" (
    echo   [OK] Courses data generated
) else (
    echo   [ERROR] Courses data missing
)

if exist "data\raw\interactions\interactions_*.json" (
    echo   [OK] Interactions data generated
) else (
    echo   [ERROR] Interactions data missing
)

echo.
echo ======================================================================
echo Phase 1 Generation Complete!
echo ======================================================================
echo.
echo Next step: Import to MongoDB
echo   python simulator/scripts/import_to_mongodb.py --clear
echo.

pause
