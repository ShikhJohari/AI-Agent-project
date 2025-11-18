#!/bin/bash

# Test script for the AI Agent
echo "=========================================="
echo "Testing AI Agent - Free Range Mode"
echo "=========================================="
echo ""

PROJECT_ROOT="/Users/shikhar/.cursor/worktrees/AI-Agent-project/93NSN"
cd "$PROJECT_ROOT"

echo "Test 1: List files in project root"
echo "-----------------------------------"
python3 main.py "What files are in the project root directory?"
echo ""
echo ""

echo "Test 2: List files in calculator/pkg directory"
echo "----------------------------------------------"
python3 main.py "What files are in the calculator/pkg directory?"
echo ""
echo ""

echo "Test 3: Read main.py from root"
echo "------------------------------"
python3 main.py "Show me the first 20 lines of main.py in the project root"
echo ""
echo ""

echo "Test 4: List files in functions directory"
echo "-----------------------------------------"
python3 main.py "What Python files are in the functions directory?"
echo ""
echo ""

echo "Test 5: Run calculator tests"
echo "----------------------------"
python3 main.py "Run the calculator/tests.py file"
echo ""
echo ""

echo "=========================================="
echo "All tests completed!"
echo "=========================================="

