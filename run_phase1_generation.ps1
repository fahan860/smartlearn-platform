# Smart Learning Platform - Phase 1 Data Generation
# PowerShell Script

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Smart Learning Platform - Phase 1: Data Generation" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "[2/4] Installing dependencies..." -ForegroundColor Yellow
Push-Location simulator
try {
    pip install -r requirements.txt --quiet 2>&1 | Out-Null
    Write-Host "  Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Failed to install dependencies" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location

# Generate data
Write-Host ""
Write-Host "[3/4] Generating synthetic data..." -ForegroundColor Yellow
try {
    python simulator/src/data_generator.py
    if ($LASTEXITCODE -ne 0) {
        throw "Generation failed"
    }
} catch {
    Write-Host "  ERROR: Data generation failed - $_" -ForegroundColor Red
    exit 1
}

# Verify files
Write-Host ""
Write-Host "[4/4] Verifying generated files..." -ForegroundColor Yellow

$usersFiles = Get-ChildItem -Path "data/raw/users/users_*.json" -ErrorAction SilentlyContinue
$coursesFiles = Get-ChildItem -Path "data/raw/courses/courses_*.json" -ErrorAction SilentlyContinue
$interactionsFiles = Get-ChildItem -Path "data/raw/interactions/interactions_*.json" -ErrorAction SilentlyContinue

if ($usersFiles) {
    Write-Host "  [OK] Users data generated: $($usersFiles.Name)" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Users data missing" -ForegroundColor Red
}

if ($coursesFiles) {
    Write-Host "  [OK] Courses data generated: $($coursesFiles.Name)" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Courses data missing" -ForegroundColor Red
}

if ($interactionsFiles) {
    Write-Host "  [OK] Interactions data generated: $($interactionsFiles.Name)" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Interactions data missing" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Phase 1 Generation Complete!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: Import to MongoDB" -ForegroundColor Yellow
Write-Host "  python simulator/scripts/import_to_mongodb.py --clear" -ForegroundColor White
Write-Host ""
