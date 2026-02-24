#!/bin/bash

# 🧪 SMARTLEARN - SCRIPT DE TEST DES ROUTES API
# Usage: bash test_api.sh

echo "🚀 SMARTLEARN API TEST SUITE"
echo "================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
BASE_URL="http://localhost:4000"
TIMEOUT=5

# Fonction pour tester une requête
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local name=$4
    local headers=$5

    echo -e "${YELLOW}Testing:${NC} $name"
    echo "  $method $endpoint"
    
    if [ "$method" == "GET" ]; then
        curl -s -X GET "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            $headers \
            --max-time $TIMEOUT \
            -w "\n"
    elif [ "$method" == "POST" ]; then
        curl -s -X POST "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            $headers \
            -d "$data" \
            --max-time $TIMEOUT \
            -w "\n"
    fi
    echo ""
}

# 1. TEST HEALTH CHECK
echo -e "${GREEN}=== HEALTH CHECK ===${NC}"
test_endpoint "GET" "/" "null" "Server Status"

test_endpoint "GET" "/health" "null" "Health Endpoint"

# 2. TEST AUTH
echo -e "${GREEN}=== AUTHENTICATION ===${NC}"

# Signup
SIGNUP_DATA='{
  "name": "Test User",
  "email": "test@example.com",
  "password": "TestPassword123"
}'

echo -e "${YELLOW}Testing:${NC} User Signup"
echo "  POST /api/auth/signup"
SIGNUP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/signup" \
    -H "Content-Type: application/json" \
    -d "$SIGNUP_DATA" \
    --max-time $TIMEOUT)

echo "$SIGNUP_RESPONSE"
echo ""

# Extract token from signup response
TOKEN=$(echo "$SIGNUP_RESPONSE" | grep -o '"token":"[^"]*' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✓ Signup successful!${NC}"
    echo "  Token: ${TOKEN:0:20}..."
    echo ""
    
    # 3. TEST AUTH /me
    echo -e "${GREEN}=== USER PROFILE ===${NC}"
    test_endpoint "GET" "/api/auth/me" "null" "Get Current User" "-H 'Authorization: Bearer $TOKEN'"
    
    # 4. TEST COURSES
    echo -e "${GREEN}=== COURSES ===${NC}"
    test_endpoint "GET" "/api/courses" "null" "List All Courses"
    
    test_endpoint "GET" "/api/courses/mysql" "null" "List MySQL Courses"
    
    # 5. TEST INTERACTIONS
    echo -e "${GREEN}=== INTERACTIONS ===${NC}"
    test_endpoint "GET" "/api/interactions/me" "null" "Get My Interactions" "-H 'Authorization: Bearer $TOKEN'"
    
    # 6. TEST RECOMMENDATIONS
    echo -e "${GREEN}=== RECOMMENDATIONS ===${NC}"
    test_endpoint "GET" "/api/recommendations" "null" "Get Recommendations" "-H 'Authorization: Bearer $TOKEN'"
    
    echo -e "${GREEN}✓ All basic tests completed!${NC}"
else
    echo -e "${RED}✗ Signup failed! Check if server is running.${NC}"
fi

echo ""
echo "================================"
echo "🎉 Test suite finished!"
echo ""
echo "Next steps:"
echo "1. Open http://localhost:5173 in your browser"
echo "2. Sign up with the test account"
echo "3. Navigate through the app"
echo "4. Check browser console for any errors"
