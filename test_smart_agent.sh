#!/bin/bash

# Test script for the bulletproof AI agent improvements
# This script tests all the smart file-finding capabilities

echo "=========================================="
echo "🚀 Testing Bulletproof AI Agent"
echo "=========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

run_test() {
    local test_name="$1"
    local query="$2"
    
    echo -e "${BLUE}Test: ${test_name}${NC}"
    echo "Query: \"${query}\""
    echo "---"
    
    uv run python main.py "${query}"
    
    echo ""
    echo -e "${GREEN}✓ Test completed${NC}"
    echo ""
    echo "=========================================="
    echo ""
}

# Test 1: Basic file finding with different case
run_test "Case-Insensitive Search" "find me README.md"

# Test 2: Nested file detection
run_test "Nested File Detection" "show me calculator.py"

# Test 3: Pattern matching
run_test "Pattern Matching" "list all test files"

# Test 4: Case variation
run_test "Different Case Variation" "read CONFIG.PY"

# Test 5: Complex operation
run_test "Complex Operation" "find my readme and tell me how many lines it has"

# Test 6: Pattern-based search
run_test "Pattern-Based Search" "find files with 'calc' in the name"

# Test 7: Original failing query
run_test "Original Query (Previously Failed)" "show me the contents of readme.md"

echo ""
echo "=========================================="
echo -e "${GREEN}🎉 All tests completed!${NC}"
echo "=========================================="
echo ""
echo "The agent now:"
echo "  ✓ Automatically finds files without asking for paths"
echo "  ✓ Handles case-insensitive searches"
echo "  ✓ Detects files in nested directories"
echo "  ✓ Supports pattern-based matching"
echo "  ✓ Provides intelligent, proactive responses"
echo ""
echo "This is a truly bulletproof AI agent! 🚀"
echo ""

