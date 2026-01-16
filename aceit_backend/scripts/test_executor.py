"""
Test script for the code executor.
Run this to verify the LeetCode-like execution works correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.code_executor import execute_code

def test_correct_solution():
    """Test with a correct Two Sum solution"""
    print("\n=== Test 1: Correct Solution ===")
    code = """
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
"""
    test_cases = [
        {"input": [[2,7,11,15], 9], "output": [0, 1]},
        {"input": [[3,2,4], 6], "output": [1, 2]},
        {"input": [[3,3], 6], "output": [0, 1]},
    ]
    
    result = execute_code("python", code, test_cases, "twoSum")
    print(f"Passed: {result.get('passed')}/{result.get('total')}")
    print(f"Results: {result.get('results')}")
    assert result.get('passed') == 3, f"Expected 3 passed, got {result.get('passed')}"
    print("✓ Test 1 PASSED")


def test_wrong_solution():
    """Test with a wrong solution"""
    print("\n=== Test 2: Wrong Solution ===")
    code = """
class Solution:
    def twoSum(self, nums, target):
        return [0, 0]  # Always wrong
"""
    test_cases = [
        {"input": [[2,7,11,15], 9], "output": [0, 1]},
        {"input": [[3,2,4], 6], "output": [1, 2]},
    ]
    
    result = execute_code("python", code, test_cases, "twoSum")
    print(f"Passed: {result.get('passed')}/{result.get('total')}")
    assert result.get('passed') == 0, f"Expected 0 passed, got {result.get('passed')}"
    print("✓ Test 2 PASSED")


def test_syntax_error():
    """Test with syntax error"""
    print("\n=== Test 3: Syntax Error ===")
    code = """
class Solution:
    def twoSum(self, nums, target)
        return [0, 1]  # Missing colon
"""
    test_cases = [{"input": [[2,7,11,15], 9], "output": [0, 1]}]
    
    result = execute_code("python", code, test_cases, "twoSum")
    print(f"Result: {result}")
    assert "error" in result or result.get('passed') == 0, "Should have error"
    print("✓ Test 3 PASSED")


def test_runtime_error():
    """Test with runtime error"""
    print("\n=== Test 4: Runtime Error ===")
    code = """
class Solution:
    def twoSum(self, nums, target):
        return nums[999999]  # Index out of range
"""
    test_cases = [{"input": [[2,7,11,15], 9], "output": [0, 1]}]
    
    result = execute_code("python", code, test_cases, "twoSum")
    print(f"Result: {result}")
    assert result.get('results', [{}])[0].get('status') == 'error', "Should have error status"
    print("✓ Test 4 PASSED")


def test_standalone_function():
    """Test with standalone function (not class-based)"""
    print("\n=== Test 5: Standalone Function ===")
    code = """
def isPalindrome(x):
    if x < 0:
        return False
    return str(x) == str(x)[::-1]
"""
    test_cases = [
        {"input": [121], "output": True},
        {"input": [-121], "output": False},
        {"input": [10], "output": False},
    ]
    
    result = execute_code("python", code, test_cases, "isPalindrome")
    print(f"Passed: {result.get('passed')}/{result.get('total')}")
    assert result.get('passed') == 3, f"Expected 3 passed, got {result.get('passed')}"
    print("✓ Test 5 PASSED")


def test_timeout():
    """Test with infinite loop (should timeout)"""
    print("\n=== Test 6: Timeout (Infinite Loop) ===")
    code = """
class Solution:
    def twoSum(self, nums, target):
        while True:
            pass  # Infinite loop
"""
    test_cases = [{"input": [[2,7,11,15], 9], "output": [0, 1]}]
    
    result = execute_code("python", code, test_cases, "twoSum")
    print(f"Result: {result}")
    assert "Time Limit" in result.get('error', '') or "Timeout" in result.get('error', ''), "Should timeout"
    print("✓ Test 6 PASSED")


if __name__ == "__main__":
    print("=" * 50)
    print("  Code Executor Test Suite")
    print("=" * 50)
    
    try:
        test_correct_solution()
        test_wrong_solution()
        test_syntax_error()
        test_runtime_error()
        test_standalone_function()
        test_timeout()
        
        print("\n" + "=" * 50)
        print("  ALL TESTS PASSED ✓")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)
