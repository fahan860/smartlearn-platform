# 🧪 SMARTLEARN - SCRIPT DE TEST DES ROUTES API (Windows PowerShell)
# Usage: .\test_api.ps1

Write-Host "🚀 SMARTLEARN API TEST SUITE" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$BASE_URL = "http://localhost:4000"
$TIMEOUT = 5

# Fonction pour tester une requête
function Test-Endpoint {
    param(
        [string]$Method,
        [string]$Endpoint,
        [string]$Data,
        [string]$Name,
        [hashtable]$Headers = @{}
    )
    
    Write-Host "Testing: $Name" -ForegroundColor Yellow
    Write-Host "  $Method $Endpoint" -ForegroundColor Gray
    
    try {
        $params = @{
            Uri             = "$BASE_URL$Endpoint"
            Method          = $Method
            ContentType     = "application/json"
            TimeoutSec      = $TIMEOUT
        }
        
        if ($Data) {
            $params.Body = $Data
        }
        
        if ($Headers.Count -gt 0) {
            $params.Headers = $Headers
        }
        
        $response = Invoke-RestMethod @params
        $response | ConvertTo-Json | Write-Host -ForegroundColor Green
    }
    catch {
        Write-Host "  Error: $_" -ForegroundColor Red
    }
    
    Write-Host ""
}

# 1. TEST HEALTH CHECK
Write-Host "=== HEALTH CHECK ===" -ForegroundColor Green

Test-Endpoint -Method "GET" -Endpoint "/" -Name "Server Status"
Test-Endpoint -Method "GET" -Endpoint "/health" -Name "Health Endpoint"

# 2. TEST AUTH
Write-Host "=== AUTHENTICATION ===" -ForegroundColor Green

# Signup
$signupData = @{
    name     = "Test User"
    email    = "test@example.com"
    password = "TestPassword123"
} | ConvertTo-Json

Write-Host "Testing: User Signup" -ForegroundColor Yellow
Write-Host "  POST /api/auth/signup" -ForegroundColor Gray

try {
    $signupResponse = Invoke-RestMethod `
        -Uri "$BASE_URL/api/auth/signup" `
        -Method "POST" `
        -ContentType "application/json" `
        -Body $signupData `
        -TimeoutSec $TIMEOUT
    
    Write-Host ($signupResponse | ConvertTo-Json) -ForegroundColor Green
    $token = $signupResponse.token
    
    if ($token) {
        Write-Host "✓ Signup successful!" -ForegroundColor Green
        Write-Host "  Token: $($token.Substring(0, 20))..."
        Write-Host ""
        
        # 3. TEST AUTH /me
        Write-Host "=== USER PROFILE ===" -ForegroundColor Green
        
        $authHeaders = @{
            Authorization = "Bearer $token"
        }
        
        Test-Endpoint -Method "GET" -Endpoint "/api/auth/me" `
            -Name "Get Current User" -Headers $authHeaders
        
        # 4. TEST COURSES
        Write-Host "=== COURSES ===" -ForegroundColor Green
        
        Test-Endpoint -Method "GET" -Endpoint "/api/courses" `
            -Name "List All Courses"
        
        Test-Endpoint -Method "GET" -Endpoint "/api/courses/mysql" `
            -Name "List MySQL Courses"
        
        # 5. TEST INTERACTIONS
        Write-Host "=== INTERACTIONS ===" -ForegroundColor Green
        
        Test-Endpoint -Method "GET" -Endpoint "/api/interactions/me" `
            -Name "Get My Interactions" -Headers $authHeaders
        
        # 6. TEST RECOMMENDATIONS
        Write-Host "=== RECOMMENDATIONS ===" -ForegroundColor Green
        
        Test-Endpoint -Method "GET" -Endpoint "/api/recommendations" `
            -Name "Get Recommendations" -Headers $authHeaders
        
        Write-Host "✓ All basic tests completed!" -ForegroundColor Green
    }
    else {
        Write-Host "✗ No token in response!" -ForegroundColor Red
    }
}
catch {
    Write-Host "✗ Signup failed!" -ForegroundColor Red
    Write-Host "  Make sure the server is running on $BASE_URL" -ForegroundColor Yellow
    Write-Host "  Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "🎉 Test suite finished!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Open http://localhost:5173 in your browser" -ForegroundColor White
Write-Host "2. Sign up with the test account" -ForegroundColor White
Write-Host "3. Navigate through the app" -ForegroundColor White
Write-Host "4. Check browser console for any errors (F12)" -ForegroundColor White
