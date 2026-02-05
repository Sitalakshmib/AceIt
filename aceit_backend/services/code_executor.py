import subprocess
import sys
import tempfile
import os
import json
import logging
import re
import shutil
import requests

logger = logging.getLogger(__name__)

# Timeout for code execution (seconds)
EXECUTION_TIMEOUT = 10


def _find_gcc() -> str:
    """Find GCC compiler on the system."""
    # First check if gcc is in PATH
    gcc_in_path = shutil.which('gcc')
    if gcc_in_path:
        return gcc_in_path
    
    # Common GCC locations on Windows
    common_paths = [
        # Anaconda
        os.path.expanduser('~/anaconda3/Library/mingw-w64/bin/gcc.exe'),
        os.path.expanduser('~/miniconda3/Library/mingw-w64/bin/gcc.exe'),
        'C:/Users/USER/anaconda3/Library/mingw-w64/bin/gcc.exe',
        # MinGW
        'C:/MinGW/bin/gcc.exe',
        'C:/MinGW64/bin/gcc.exe',
        'C:/mingw-w64/bin/gcc.exe',
        # TDM-GCC
        'C:/TDM-GCC-64/bin/gcc.exe',
        'C:/TDM-GCC-32/bin/gcc.exe',
        # MSYS2
        'C:/msys64/mingw64/bin/gcc.exe',
        'C:/msys64/mingw32/bin/gcc.exe',
        # Program Files
        'C:/Program Files/mingw-w64/bin/gcc.exe',
        'C:/Program Files (x86)/mingw-w64/bin/gcc.exe',
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None


# Piston API for remote code execution
PISTON_API_URL = "https://emkc.org/api/v2/piston/execute"


def execute_code(language: str, code: str, test_cases: list = None, function_name: str = None):
    """
    Execute code using local execution (Python) or Piston API (other languages).
    Supports Python, JavaScript, Java, C++, C.
    
    Args:
        language: Programming language
        code: User submitted code
        test_cases: List of test cases with 'input' and 'output' keys
        function_name: Name of the function/method to call
    
    Returns:
        dict with passed, total, results, and any error information
    """
    language = language.lower()
    
    # Python: Local execution (fastest)
    if language == "python":
        return _execute_python(code, test_cases, function_name)
    
    # JavaScript: Piston API
    elif language == "javascript":
        return _execute_with_piston("javascript", "18.15.0", code, test_cases, function_name)
    
    # Java: Piston API
    elif language == "java":
        return _execute_with_piston("java", "15.0.2", code, test_cases, function_name)
    
    # C++: Piston API
    elif language in ["cpp", "c++"]:
        return _execute_with_piston("cpp", "10.2.0", code, test_cases, function_name)
    
    # C: Isolated execution (each test run independently to prevent global state issues)
    elif language == "c":
        from services.piston_wrappers import wrap_c_for_piston
        return wrap_c_for_piston(code, test_cases, function_name)
    
    # R: Piston API
    elif language == "r":
        return _execute_with_piston("r", "4.1.1", code, test_cases, function_name)
    
    else:
        return {
            "error": f"Language '{language}' is not supported. Available: Python, R, Java, C++, C",
            "passed": 0,
            "total": 0,
            "results": []
        }


def _execute_python(code: str, test_cases: list, function_name: str = None):
    """Execute Python code with test cases."""
    if not test_cases:
        return {
            "error": "No test cases provided",
            "passed": 0,
            "total": 0,
            "results": []
        }
    
    # Auto-detect function name from code
    if function_name is None:
        function_name = _detect_function_name(code)
    
    if not function_name:
        return {
            "error": "Could not detect function name. Please define a function like 'def twoSum(...)' or 'class Solution'.",
            "passed": 0,
            "total": 0,
            "results": []
        }
    
    # Check if it's a class-based solution
    is_class_based = "class Solution" in code
    
    # Build the test runner script
    runner_code = _build_python_runner(code, test_cases, function_name, is_class_based)
    
    # Execute in subprocess
    return _run_python_code(runner_code)


def _execute_with_piston(language: str, version: str, code: str, test_cases: list, function_name: str = None):
    """Execute code using Piston API (for JS, Java, C++, C)."""
    if not test_cases:
        return {
            "error": "No test cases provided",
            "passed": 0,
            "total": 0,
            "results": []
        }
    
    if not function_name:
        return {
            "error": "Function name is required",
            "passed": 0,
            "total": 0,
            "results": []
        }
    
    # Build wrapped code with test runner based on language
    wrapped_code = _wrap_code_for_piston(language, code, test_cases, function_name)
    
    # Call Piston API
    try:
        # For Java, specify filename to match public class name
        filename = "Main.java" if language == "java" else ""
        
        payload = {
            "language": language,
            "version": version,
            "files": [{
                "name": filename,
                "content": wrapped_code
            }] if filename else [{"content": wrapped_code}]
        }
        
        response = requests.post(PISTON_API_URL, json=payload, timeout=30)
        result = response.json()
        
        # Parse output
        stdout = result.get('run', {}).get('stdout', '')
        stderr = result.get('run', {}).get('stderr', '')
        
        if stderr and not stdout:
            return {
                "error": "Runtime Error",
                "message": stderr[:500],
                "passed": 0,
                "total": 0,
                "results": []
            }
        
        # Try to parse JSON output from our test runner
        try:
            output = json.loads(stdout.strip())
            return output
        except json.JSONDecodeError:
            return {
                "error": "Output Parse Error",
                "message": f"Could not parse output: {stdout[:200]}",
                "stderr": stderr[:200] if stderr else "",
                "passed": 0,
                "total": 0,
                "results": []
            }
            
    except requests.exceptions.Timeout:
        return {
            "error": "Time Limit Exceeded",
            "message": "Code execution exceeded time limit",
            "passed": 0,
            "total": 0,
            "results": []
        }
    except Exception as e:
        logger.error(f"Piston API error: {e}")
        return {
            "error": "Execution Error",
            "message": str(e),
            "passed": 0,
            "total": 0,
            "results": []
        }


def _wrap_code_for_piston(language: str, user_code: str, test_cases: list, function_name: str) -> str:
    """Wrap user code with test runner for Piston execution."""
    from services.piston_wrappers import (
        wrap_java_for_piston, 
        wrap_cpp_for_piston, 
        wrap_c_for_piston, 
        wrap_r_for_piston
    )
    
    if language == "java":
        return wrap_java_for_piston(user_code, test_cases, function_name)
    elif language == "cpp":
        return wrap_cpp_for_piston(user_code, test_cases, function_name)
    elif language == "c":
        return wrap_c_for_piston(user_code, test_cases, function_name)
    elif language == "r":
        return wrap_r_for_piston(user_code, test_cases, function_name)
    else:
        return user_code


def _wrap_javascript(user_code: str, test_cases: list, function_name: str) -> str:
    """Wrap JavaScript code with test runner."""
    return f'''
{user_code}

// Test runner
const testCases = {json.dumps(test_cases)};
let passed = 0;
let total = 0;
const results = [];

for (const tc of testCases) {{
    total++;
    const input = tc.input;
    const expected = tc.output;
    
    try {{
        let actual;
        if (Array.isArray(input)) {{
            actual = {function_name}(...input);
        }} else {{
            actual = {function_name}(input);
        }}
        
        const isEqual = JSON.stringify(actual) === JSON.stringify(expected) || 
                       (Array.isArray(actual) && Array.isArray(expected) && 
                        JSON.stringify(actual.sort()) === JSON.stringify(expected.sort()));
        
        if (isEqual) {{
            passed++;
            results.push({{status: "passed", input, expected, actual}});
        }} else {{
            results.push({{status: "failed", input, expected, actual}});
        }}
    }} catch (e) {{
        results.push({{status: "error", input, expected, error: e.message}});
    }}
}}

console.log(JSON.stringify({{passed, total, results}}));
'''


def _wrap_java(user_code: str, test_cases: list, function_name: str) -> str:
    """
    Wrap Java Solution class with Main class and test runner.
    User submits: class Solution { method() {...} }
    We wrap with: public class Main with test harness
    """
    
    # Build test execution code for each test case
    test_execution_code = []
    
    for i, test_case in enumerate(test_cases):
        input_data = test_case.get("input", {})
        expected = test_case.get("expected")
        
        # Simple test harness - works for basic types
        # For more complex types, would need type introspection
        test_execution_code.append(f'''
        // Test case {i + 1}
        try {{
            Object result = null;
            Object expected = null;
            boolean passed = false;
            
            // This is a simplified test harness
            // In production, you'd parse input types dynamically
            passed = true;  // Placeholder - actual test logic would go here
            
            if (passed) {{
                System.out.println("PASS");
            }} else {{
                System.out.println("FAIL");
            }}
        }} catch (Exception e) {{
            System.out.println("ERROR: " + e.getMessage());
        }}
        ''')
    
    wrapped_code = f'''
import java.util.*;

{user_code}

public class Main {{
    public static void main(String[] args) {{
        Solution solution = new Solution();
        
        // Run test cases
        {"".join(test_execution_code)}
    }}
}}
'''
    
    return wrapped_code



def _wrap_cpp(user_code: str, test_cases: list, function_name: str) -> str:
    """Wrap C++ code with test runner."""
    return f'''
#include <iostream>
#include <vector>
#include <string>
using namespace std;

{user_code}

int main() {{
    // Simplified C++ test runner
    cout << "{{\\"passed\\":0,\\"total\\":0,\\"results\\":[],\\"error\\":\\"C++ test runner needs implementation\\"}}" << endl;
    return 0;
}}
'''


def _execute_c(code: str, test_cases: list, function_name: str = None):
    """Execute C code with test cases using GCC."""
    if not test_cases:
        return {
            "error": "No test cases provided",
            "passed": 0,
            "total": 0,
            "results": []
        }
    
    if not function_name:
        return {
            "error": "Function name is required for C execution.",
            "passed": 0,
            "total": 0,
            "results": []
        }
    
    # Build complete C program with test runner
    c_program = _build_c_runner(code, test_cases, function_name)
    
    # Compile and run
    return _run_c_code(c_program)


def _detect_function_name(code: str) -> str:
    """
    Detect the main function name from user code.
    Supports both 'def functionName' and 'class Solution' with method inside.
    """
    # Check for class Solution pattern (LeetCode style)
    if "class Solution" in code:
        # Find method inside Solution class
        # Look for 'def methodName(self, ...)' after 'class Solution'
        class_match = re.search(r'class\s+Solution.*?:\s*\n(.*?)(?=\nclass|\Z)', code, re.DOTALL)
        if class_match:
            method_match = re.search(r'def\s+(\w+)\s*\(\s*self', class_match.group(1))
            if method_match:
                return method_match.group(1)
    
    # Check for standalone function
    func_match = re.search(r'def\s+(\w+)\s*\(', code)
    if func_match:
        return func_match.group(1)
    
    return None


def _build_python_runner(user_code: str, test_cases: list, function_name: str, is_class_based: bool) -> str:
    """
    Build a complete Python script that runs user code against test cases.
    """
    # Common imports that LeetCode problems often need
    imports = """
from typing import List, Optional, Dict, Set, Tuple
import collections
import heapq
import math
import bisect
import functools
import itertools
import json
import sys
"""
    
    # Test runner template
    if is_class_based:
        runner = f'''
{imports}

# --- User Code Start ---
{user_code}
# --- User Code End ---

def run_tests():
    results = []
    passed = 0
    total = 0
    
    test_cases = json.loads('{json.dumps(test_cases)}')
    
    solution = Solution()
    
    for i, test in enumerate(test_cases):
        total += 1
        input_val = test['input']
        expected = test['output']
        
        try:
            # Call the method with unpacked arguments
            if isinstance(input_val, list):
                actual = solution.{function_name}(*input_val)
            else:
                actual = solution.{function_name}(input_val)
            
            # Compare results
            if _compare_results(actual, expected):
                passed += 1
                results.append({{"status": "passed", "input": input_val, "expected": expected, "actual": actual}})
            else:
                results.append({{"status": "failed", "input": input_val, "expected": expected, "actual": actual}})
        except Exception as e:
            results.append({{"status": "error", "input": input_val, "expected": expected, "error": str(e)}})
    
    print(json.dumps({{"passed": passed, "total": total, "results": results}}))

def _compare_results(actual, expected):
    """Compare results, handling list order for some problems"""
    if isinstance(actual, list) and isinstance(expected, list):
        # For problems where order doesn't matter, sort both
        # But first try direct comparison
        if actual == expected:
            return True
        # Try sorted comparison if both are lists of comparable items
        try:
            return sorted(actual) == sorted(expected)
        except TypeError:
            return False
    return actual == expected

if __name__ == "__main__":
    run_tests()
'''
    else:
        # Standalone function
        runner = f'''
{imports}

# --- User Code Start ---
{user_code}
# --- User Code End ---

def run_tests():
    results = []
    passed = 0
    total = 0
    
    test_cases = json.loads('{json.dumps(test_cases)}')
    
    for i, test in enumerate(test_cases):
        total += 1
        input_val = test['input']
        expected = test['output']
        
        try:
            # Call the function with unpacked arguments
            if isinstance(input_val, list):
                actual = {function_name}(*input_val)
            else:
                actual = {function_name}(input_val)
            
            # Compare results
            if _compare_results(actual, expected):
                passed += 1
                results.append({{"status": "passed", "input": input_val, "expected": expected, "actual": actual}})
            else:
                results.append({{"status": "failed", "input": input_val, "expected": expected, "actual": actual}})
        except Exception as e:
            results.append({{"status": "error", "input": input_val, "expected": expected, "error": str(e)}})
    
    print(json.dumps({{"passed": passed, "total": total, "results": results}}))

def _compare_results(actual, expected):
    """Compare results, handling list order for some problems"""
    if isinstance(actual, list) and isinstance(expected, list):
        if actual == expected:
            return True
        try:
            return sorted(actual) == sorted(expected)
        except TypeError:
            return False
    return actual == expected

if __name__ == "__main__":
    run_tests()
'''
    return runner


def _run_python_code(code: str) -> dict:
    """
    Execute Python code in a subprocess and return results.
    """
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Run the code with timeout
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT,
                cwd=os.path.dirname(temp_file)
            )
            
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            
            # Check for errors
            if result.returncode != 0:
                return {
                    "error": "Runtime Error",
                    "message": stderr or "Unknown error occurred",
                    "passed": 0,
                    "total": 0,
                    "results": []
                }
            
            # Parse JSON output
            try:
                output = json.loads(stdout)
                return output
            except json.JSONDecodeError:
                return {
                    "error": "Output Parse Error",
                    "message": f"Could not parse output: {stdout}",
                    "stderr": stderr,
                    "passed": 0,
                    "total": 0,
                    "results": []
                }
                
        except subprocess.TimeoutExpired:
            return {
                "error": "Time Limit Exceeded",
                "message": f"Code execution exceeded {EXECUTION_TIMEOUT} seconds",
                "passed": 0,
                "total": 0,
                "results": []
            }
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
                
    except Exception as e:
        logger.error(f"Code execution error: {e}")
        return {
            "error": "Execution Error",
            "message": str(e),
            "passed": 0,
            "total": 0,
            "results": []
        }


def _build_c_runner(user_code: str, test_cases: list, function_name: str) -> str:
    """Build a complete C program with test harness."""
    
    # C test runner template
    c_template = '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// User code starts here
{user_code}
// User code ends here

// Test runner
int main() {{
    int passed = 0;
    int total = 0;
    
    printf("{{\\\"results\\\":[");
    
{test_code}
    
    printf("],\\\"passed\\\":%d,\\\"total\\\":%d}}", passed, total);
    return 0;
}}
'''
    
    # Generate test code based on function name
    test_code_lines = []
    
    for i, tc in enumerate(test_cases):
        inp = tc.get("input", [])
        expected = tc.get("output")
        
        # Handle different problem types
        if function_name == "isPalindrome":
            x_val = inp[0] if isinstance(inp, list) else inp
            exp_str = "true" if expected else "false"
            test_code_lines.append(f'''
    // Test {i+1}
    total++;
    if ({i} > 0) printf(",");
    {{
        bool result = isPalindrome({x_val});
        bool expected = {'true' if expected else 'false'};
        if (result == expected) {{
            passed++;
            printf("{{\\"status\\":\\"passed\\",\\"input\\":{x_val},\\"expected\\":{exp_str},\\"actual\\":%s}}", result ? "true" : "false");
        }} else {{
            printf("{{\\"status\\":\\"failed\\",\\"input\\":{x_val},\\"expected\\":{exp_str},\\"actual\\":%s}}", result ? "true" : "false");
        }}
    }}''')
        elif function_name == "reverse":
            x_val = inp[0] if isinstance(inp, list) else inp
            test_code_lines.append(f'''
    // Test {i+1}
    total++;
    if ({i} > 0) printf(",");
    {{
        int result = reverse({x_val});
        int expected = {expected};
        if (result == expected) {{
            passed++;
            printf("{{\\"status\\":\\"passed\\",\\"input\\":{x_val},\\"expected\\":%d,\\"actual\\":%d}}", expected, result);
        }} else {{
            printf("{{\\"status\\":\\"failed\\",\\"input\\":{x_val},\\"expected\\":%d,\\"actual\\":%d}}", expected, result);
        }}
    }}''')
        elif function_name == "isValid":
            s_val = inp[0] if isinstance(inp, list) else inp
            exp_str = "true" if expected else "false"
            test_code_lines.append(f'''
    // Test {i+1}
    total++;
    if ({i} > 0) printf(",");
    {{
        bool result = isValid("{s_val}");
        bool expected = {'true' if expected else 'false'};
        if (result == expected) {{
            passed++;
            printf("{{\\"status\\":\\"passed\\",\\"input\\":\\"{s_val}\\",\\"expected\\":{exp_str},\\"actual\\":%s}}", result ? "true" : "false");
        }} else {{
            printf("{{\\"status\\":\\"failed\\",\\"input\\":\\"{s_val}\\",\\"expected\\":{exp_str},\\"actual\\":%s}}", result ? "true" : "false");
        }}
    }}''')
        else:
            # Generic case - skip for now
            test_code_lines.append(f'''
    // Test {i+1} - skipped (unsupported function type)
    total++;
    if ({i} > 0) printf(",");
    printf("{{\\"status\\":\\"error\\",\\"error\\":\\"C execution for {function_name} not implemented\\"}}");''')
    
    test_code = "\\n".join(test_code_lines)
    
    return c_template.format(user_code=user_code, test_code=test_code)


def _run_c_code(code: str) -> dict:
    """Compile and run C code."""
    try:
        # Find GCC - check common locations on Windows
        gcc_path = _find_gcc()
        if not gcc_path:
            return {
                "error": "GCC Not Found",
                "message": "GCC compiler is not installed or not in PATH. Please install MinGW or add GCC to PATH.",
                "passed": 0,
                "total": 0,
                "results": []
            }
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False, encoding='utf-8') as f:
            f.write(code)
            source_file = f.name
        
        exe_file = source_file.replace('.c', '.exe' if os.name == 'nt' else '')
        
        try:
            # Compile with GCC
            compile_result = subprocess.run(
                [gcc_path, source_file, '-o', exe_file, '-lm'],
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
            )
            
            if compile_result.returncode != 0:
                return {
                    "error": "Compilation Error",
                    "message": compile_result.stderr or "Failed to compile C code",
                    "passed": 0,
                    "total": 0,
                    "results": []
                }
            
            # Run the executable
            run_result = subprocess.run(
                [exe_file],
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
            )
            
            stdout = run_result.stdout.strip()
            stderr = run_result.stderr.strip()
            
            if run_result.returncode != 0:
                return {
                    "error": "Runtime Error",
                    "message": stderr or "Program crashed",
                    "passed": 0,
                    "total": 0,
                    "results": []
                }
            
            # Parse JSON output
            try:
                output = json.loads(stdout)
                return output
            except json.JSONDecodeError:
                return {
                    "error": "Output Parse Error",
                    "message": f"Could not parse output: {stdout}",
                    "passed": 0,
                    "total": 0,
                    "results": []
                }
                
        except subprocess.TimeoutExpired:
            return {
                "error": "Time Limit Exceeded",
                "message": f"Code execution exceeded {EXECUTION_TIMEOUT} seconds",
                "passed": 0,
                "total": 0,
                "results": []
            }
        except FileNotFoundError:
            return {
                "error": "GCC Not Found",
                "message": "GCC compiler is not installed. Please install MinGW or GCC.",
                "passed": 0,
                "total": 0,
                "results": []
            }
        finally:
            # Clean up temp files
            try:
                os.unlink(source_file)
            except:
                pass
            try:
                os.unlink(exe_file)
            except:
                pass
                
    except Exception as e:
        logger.error(f"C code execution error: {e}")
        return {
            "error": "Execution Error",
            "message": str(e),
            "passed": 0,
            "total": 0,
            "results": []
        }
