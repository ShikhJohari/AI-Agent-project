import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from functions.run_python_file import run_python_file


def run_tests():
    project_root = os.path.dirname(os.path.abspath(__file__))
    calculator_path = os.path.join(project_root, "calculator")
    
    print("=" * 70)
    print("Testing run_python_file function")
    print("=" * 70)
    print()
    
    print("Test 1: run_python_file(\"calculator\", \"main.py\")")
    print("-" * 70)
    result = run_python_file(calculator_path, "main.py")
    print(result)
    print()
    
    print("=" * 70)
    print("Test 2: run_python_file(\"calculator\", \"main.py\", [\"3 + 5\"])")
    print("-" * 70)
    result = run_python_file(calculator_path, "main.py", ["3 + 5"])
    print(result)
    print()
    
    print("=" * 70)
    print("Test 3: run_python_file(\"calculator\", \"tests.py\")")
    print("-" * 70)
    result = run_python_file(calculator_path, "tests.py")
    print(result)
    print()
    
    print("=" * 70)
    print("Test 4: run_python_file(\"calculator\", \"../main.py\")")
    print("-" * 70)
    result = run_python_file(calculator_path, "../main.py")
    print(result)
    print()
    
    print("=" * 70)
    print("Test 5: run_python_file(\"calculator\", \"nonexistent.py\")")
    print("-" * 70)
    result = run_python_file(calculator_path, "nonexistent.py")
    print(result)
    print()
    
    print("=" * 70)
    print("Test 6: run_python_file(\"calculator\", \"lorem.txt\")")
    print("-" * 70)
    result = run_python_file(calculator_path, "lorem.txt")
    print(result)
    print()


if __name__ == "__main__":
    run_tests()
