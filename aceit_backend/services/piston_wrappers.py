"""
Working test runner wrappers for Piston API
Handles Java, C++, C, and R code execution with test cases
"""

import json
import re
import requests


def wrap_java_for_piston(user_code: str, test_cases: list, function_name: str) -> str:
    """Create Java code with test runner - generic version for all problem types"""
    
    def java_format_value(val, is_nested=False):
        """Convert Python value to Java syntax"""
        if isinstance(val, list):
            if len(val) == 0:
                return "new String[0]"  # Changed default to String for safety
            elif isinstance(val[0], list):
                # 2D array - check element type
                if val[0] and isinstance(val[0][0], str):
                    # 2D String array
                    rows = [java_format_value(row, True) for row in val]
                    return "new String[][] {" + ", ".join(rows) + "}"
                else:
                    # 2D int array
                    rows = [java_format_value(row, True) for row in val]
                    return "new int[][] {" + ", ".join(rows) + "}"
            elif isinstance(val[0], str):
                # 1D String array
                str_items = [f'"{s}"' for s in val]
                if is_nested:
                    return "{" + ", ".join(str_items) + "}"
                else:
                    return "new String[] {" + ", ".join(str_items) + "}"
            else:
                # 1D int array
                if is_nested:
                    return "{" + ", ".join(map(str, val)) + "}"
                else:
                    return "new int[] {" + ", ".join(map(str, val)) + "}"
        elif isinstance(val, str):
            return f'"{val}"'
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif val is None:
            return "null"
        else:
            return str(val)
    
    # Remove any import statements from user code (we add them at the top)
    import re
    user_code_no_imports = re.sub(r'^\s*import\s+.*?;', '', user_code, flags=re.MULTILINE)
    
    # Ensure user's Solution class is not public
    user_code_fixed = user_code_no_imports.replace("public class Solution", "class Solution")
    
    test_code = []
    for i, tc in enumerate(test_cases):
        inp = tc['input']
        expected = tc['output']
        
        # Build function call arguments
        if isinstance(inp, list):
            args = [java_format_value(arg) for arg in inp]
            call = f"solution.{function_name}({', '.join(args)})"
        else:
            call = f"solution.{function_name}({java_format_value(inp)})"
        
        # Generate comparison code based on expected output type
        if isinstance(expected, list):
            # Check types
            is_2d = len(expected) > 0 and isinstance(expected[0], list)
            has_strings = False
            
            if is_2d and len(expected[0]) > 0:
                has_strings = isinstance(expected[0][0], str)
            elif len(expected) > 0:
                has_strings = isinstance(expected[0], str)
            
            expected_java = java_format_value(expected)
            
            if has_strings:
                # String-based output - use toString() comparison for Lists
                # This handles both String[] and List<List<String>>
                test_code.append(f"""
        total++;
        Object result{i} = {call};
        String resultStr{i} = result{i}.toString();
        String expectedStr{i} = java.util.Arrays.deepToString({expected_java});
        if (resultStr{i}.equals(expectedStr{i})) {{
            passed++;
        }}""")
            elif is_2d:
                # 2D int array - use deepEquals
                test_code.append(f"""
        total++;
        int[][] result{i} = {call};
        int[][] expected{i} = {expected_java};
        if (java.util.Arrays.deepEquals(result{i}, expected{i})) {{
            passed++;
        }}""")
            else:
                # 1D int array - use equals
                test_code.append(f"""
        total++;
        int[] result{i} = {call};
        int[] expected{i} = {expected_java};
        if (java.util.Arrays.equals(result{i}, expected{i})) {{
            passed++;
        }}""")
        else:
            # Scalar output
            test_code.append(f"""
        total++;
        Object result{i} = {call};
        if (result{i} != null && result{i}.equals({expected})) {{
            passed++;
        }}""")
    
    # Put Main class FIRST so Piston executes it
    return f"""
import java.util.*;

public class Main {{
    public static void main(String[] args) {{
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;
{chr(10).join(test_code)}
        
        System.out.println("{{\\\"passed\\\":" + passed + ",\\\"total\\\":" + total + ",\\\"results\\\":[]}}");
    }}
}}

{user_code_fixed}
"""


def wrap_cpp_for_piston(user_code: str, test_cases: list, function_name: str) -> str:
    """Create C++ code with test runner - generic version for all problem types"""
    
    def cpp_format_value(val, is_nested=False):
        """Convert Python value to C++ syntax"""
        if isinstance(val, list):
            if len(val) == 0:
                return "vector<int>{}"
            elif isinstance(val[0], list):
                # 2D vector: {{1,2},{3,4}}
                rows = [cpp_format_value(row, True) for row in val]
                if is_nested:
                    return "{" + ", ".join(rows) + "}"
                else:
                    return "vector<vector<int>>{" + ", ".join(rows) + "}"
            else:
                # 1D vector: {1,2,3}
                vals = ", ".join(map(str, val))
                if is_nested:
                    return "{" + vals + "}"
                else:
                    return "vector<int>{" + vals + "}"
        elif isinstance(val, str):
            return f'"{val}"'
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif val is None:
            return "nullptr"
        else:
            return str(val)
    
    test_code = []
    for i, tc in enumerate(test_cases):
        inp = tc['input']
        expected = tc['output']
        
        # Build function call arguments
        # For vectors/arrays, create variables first to avoid rvalue binding issues
        arg_setup = []
        arg_names = []
        
        if isinstance(inp, list):
            for j, arg in enumerate(inp):
                if isinstance(arg, list):
                    # Vector argument - create variable
                    is_2d = len(arg) > 0 and isinstance(arg[0], list)
                    arg_type = "vector<vector<int>>" if is_2d else "vector<int>"
                    arg_name = f"input{i}_{j}"
                    arg_setup.append(f"    {arg_type} {arg_name} = {cpp_format_value(arg)};")
                    arg_names.append(arg_name)
                else:
                    # Scalar argument - pass directly
                    arg_names.append(cpp_format_value(arg))
            call = f"solution.{function_name}({', '.join(arg_names)})"
        else:
            call = f"solution.{function_name}({cpp_format_value(inp)})"
        
        # Format expected output
        expected_cpp = cpp_format_value(expected)
        
        # Generate test code based on output type
        if isinstance(expected, list):
            # Check if it's a 2D vector
            is_2d = len(expected) > 0 and isinstance(expected[0], list)
            
            if is_2d:
                # 2D vector comparison
                test_code.append(f"""
{chr(10).join(arg_setup)}
    total++;
    vector<vector<int>> result{i} = {call};
    vector<vector<int>> expected{i} = {expected_cpp};
    if (result{i} == expected{i}) {{
        passed++;
    }}""")
            else:
                # 1D vector comparison
                test_code.append(f"""
{chr(10).join(arg_setup)}
    total++;
    vector<int> result{i} = {call};
    vector<int> expected{i} = {expected_cpp};
    if (result{i} == expected{i}) {{
        passed++;
    }}""")
        else:
            # Scalar output comparison
            test_code.append(f"""
{chr(10).join(arg_setup)}
    total++;
    auto result{i} = {call};
    if (result{i} == {expected}) {{
        passed++;
    }}""")
    
    # Check if user uses bits/stdc++.h (comprehensive header)
    import re
    uses_bits_stdc = 'bits/stdc++.h' in user_code
    
    if uses_bits_stdc:
        # Keep user's includes, just ensure using namespace std
        user_code_clean = user_code
        headers = "#include <bits/stdc++.h>"
    else:
        # Strip user's includes and use our comprehensive headers
        user_code_clean = re.sub(r'^\s*#include\s+<[^>]+>', '', user_code, flags=re.MULTILINE)
        headers = """#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>
#include <tuple>
#include <algorithm>"""
    
    return f"""
{headers}

using namespace std;

{user_code_clean}

int main() {{
    Solution solution;
    int passed = 0;
    int total = 0;
{chr(10).join(test_code)}
    
    cout << "{{\\\"passed\\\":" << passed << ",\\\"total\\\":" << total << ",\\\"results\\\":[]}}";
    return 0;
}}
"""


def wrap_c_for_piston(user_code: str, test_cases: list, function_name: str) -> dict:
    """
    C wrapper with ISOLATED execution - each test case runs independently
    This prevents global state contamination between tests
    Returns a dict with aggregated results from individual executions
    """
    import requests
    import json
    
    # Remove any user main function
    user_code_no_main = re.sub(r'int\s+main\s*\([^)]*\)\s*\{.*?\}', '', user_code, flags=re.DOTALL)
    
    results = {"passed": 0, "total": len(test_cases), "results": [], "error": False}
    
    for i, tc in enumerate(test_cases):
        inp = tc['input']
        expected = tc['output']
        
        # Build test code for THIS test case only
        test_code = build_c_test_case(user_code_no_main, function_name, i, inp, expected)
        
        # Execute this single test via Piston
        try:
            response = requests.post(
                "https://emkc.org/api/v2/piston/execute",
                json={
                    "language": "c",
                    "version": "10.2.0",
                    "files": [{"name": "main.c", "content": test_code}]
                },
                timeout=10
            )
            
            if response.status_code != 200:
                results["error"] = True
                results["message"] = f"Test {i+1}: Piston API error"
                continue
                
            data = response.json()
            
            if data.get("compile") and data["compile"].get("code") != 0:
                results["error"] = True
                results["message"] = f"Test {i+1} Compilation Error:\n{data['compile'].get('stderr', '')}"
                continue
                
            if data.get("run", {}).get("code") != 0:
                results["error"] = True
                results["message"] = f"Test {i+1} Runtime Error:\n{data['run'].get('stderr', '')}"
                continue
            
            # Parse output (should be "1" for pass, "0" for fail)
            output = data.get("run", {}).get("stdout", "").strip()
            if output == "1":
                results["passed"] += 1
            
        except Exception as e:
            results["error"] = True
            results["message"] = f"Test {i+1}: {str(e)}"
            continue
    
    return results


def build_c_test_case(user_code: str, function_name: str, test_idx: int, inp: any, expected: any) -> str:
    """Build a complete C program for a single test case"""
    
    def c_format_value(val, is_nested=False):
        """Convert Python value to C syntax"""
        if isinstance(val, list):
            if len(val) == 0:
                return "NULL"
            elif isinstance(val[0], list):
                # 2D array: {{1,2},{3,4}}
                rows = [c_format_value(row, True) for row in val]
                return "{" + ", ".join(rows) + "}"
            else:
                # 1D array: {1,2,3}
                return "{" + ", ".join(map(str, val)) + "}"
        elif isinstance(val, str):
            return f'"{val}"'
        elif isinstance(val, bool):
            return "1" if val else "0"
        elif val is None:
            return "NULL"
        else:
            return str(val)
    
    # Detect problem pattern
    test_code_main = ""
    
    # Pattern 1: 2D array input (Merge K Sorted Lists)
    if isinstance(inp, list) and len(inp) == 1 and isinstance(inp[0], list) and len(inp[0]) > 0 and isinstance(inp[0][0], list):
        lists = inp[0]
        k = len(lists)
        col_sizes = [len(l) for l in lists]
        
        list_data = []
        if k > 0:
            for j, l in enumerate(lists):
                if len(l) == 0:
                    list_data.append(f"    int* l_{j} = NULL;")
                else:
                    list_data.append(f"    int l_{j}_arr[] = {c_format_value(l)};")
                    list_data.append(f"    int* l_{j} = l_{j}_arr;")
            ptrs_str = ", ".join([f"l_{j}" for j in range(k)])
            list_data.append(f"    int* ptrs[] = {{{ptrs_str}}};")
        else:
            list_data.append(f"    int** ptrs = NULL;")
        
        col_sizes_block = ""
        if k > 0:
            col_sizes_block = f"""
    static int colSizes_arr[] = {c_format_value(col_sizes)};
    int* colSizes = colSizes_arr;"""
        else:
            col_sizes_block = "\n    int* colSizes = NULL;"

        expected_block = ""
        if len(expected) > 0:
            expected_block = f"""
    static int expected_arr[] = {c_format_value(expected)};
    int* expected = expected_arr;"""
        else:
            expected_block = "\n    int* expected = NULL;"

        test_code_main = f"""
int main() {{
{chr(10).join(list_data)}
{col_sizes_block}
    int returnSize = 0;
    int* result = {function_name}({'ptrs' if k > 0 else 'NULL'}, {k}, colSizes, &returnSize);
{expected_block}
    int expected_size = {len(expected)};
    
    int match = (returnSize == expected_size);
    for(int j=0; j<returnSize && match; j++) {{
        if(result[j] != expected[j]) match = 0;
    }}
    
    printf("%d\\n", match ? 1 : 0);
    if (result) free(result);
    return 0;
}}"""
    
    # Pattern 2: General 1D with multiple arguments
    elif isinstance(inp, list):
        arg_names = []
        arg_setup = []
        
        for j, arg in enumerate(inp):
            if isinstance(arg, list):
                # Check if it's a 2D array
                is_2d = len(arg) > 0 and isinstance(arg[0], list)
                arg_name = f"arg_{j}"
                
                if is_2d:
                    # 2D array - create int** with row pointers
                    rows = len(arg)
                    cols = len(arg[0]) if rows > 0 else 0
                    
                    # Create each row array
                    row_setup = []
                    for row_idx, row in enumerate(arg):
                        if len(row) > 0:
                            row_setup.append(f"    static int {arg_name}_row{row_idx}[] = {c_format_value(row)};")
                        else:
                            row_setup.append(f"    static int* {arg_name}_row{row_idx} = NULL;")
                    
                    # Create array of row pointers
                    row_ptrs = ", ".join([f"{arg_name}_row{row_idx}" for row_idx in range(rows)])
                    row_setup.append(f"    static int* {arg_name}_rows[] = {{{row_ptrs}}};")
                    row_setup.append(f"    int** {arg_name} = {arg_name}_rows;")
                    
                    arg_setup.append("\n".join(row_setup))
                    arg_names.append(arg_name)
                    arg_names.append(str(rows))  # imageSize
                    
                    # Add column size array
                    col_sizes = [len(row) for row in arg]
                    arg_setup.append(f"    static int {arg_name}_colSizes[] = {c_format_value(col_sizes)};")
                    arg_names.append(f"{arg_name}_colSizes")  # imageColSize
                    
                elif len(arg) > 0:
                    # 1D array
                    arg_setup.append(f"""
    static int {arg_name}_arr[] = {c_format_value(arg)};
    int* {arg_name} = {arg_name}_arr;""")
                    arg_names.append(arg_name)
                    arg_names.append(str(len(arg)))
                else:
                    # Empty array
                    arg_setup.append(f"\n    int* {arg_name} = NULL;")
                    arg_names.append(arg_name)
                    arg_names.append("0")
                    
            elif isinstance(arg, str):
                # Handle string arguments
                arg_name = f"str_{j}"
                arg_setup.append(f"""
    char* {arg_name} = {c_format_value(arg)};""")
                arg_names.append(arg_name)
            else:
                arg_names.append(c_format_value(arg))
        
        if isinstance(expected, list):
            # Check if expected is 2D array
            is_2d_output = len(expected) > 0 and isinstance(expected[0], list)
            
            if is_2d_output:
                # 2D array return (e.g., Flood Fill)
                arg_names.append("&returnSize")
                arg_names.append("&returnColumnSizes")
                call = f"{function_name}({', '.join(arg_names)})"
                
                # Build expected 2D array
                rows = len(expected)
                expected_setup = []
                for row_idx, row in enumerate(expected):
                    if len(row) > 0:
                        expected_setup.append(f"    static int expected_row{row_idx}[] = {c_format_value(row)};")
                    else:
                        expected_setup.append(f"    static int* expected_row{row_idx} = NULL;")
                
                row_ptrs = ", ".join([f"expected_row{row_idx}" for row_idx in range(rows)])
                expected_setup.append(f"    static int* expected_rows[] = {{{row_ptrs}}};")
                expected_setup.append(f"    int** expected = expected_rows;")
                expected_block = "\n".join(expected_setup)
                
                # Get column sizes from expected
                col_sizes = [len(row) for row in expected]
                
                test_code_main = f"""
int main() {{
{chr(10).join(arg_setup)}
    int returnSize = 0;
    int* returnColumnSizes = NULL;
    int** result = {call};
{expected_block}
    int expected_size = {rows};
    
    // Compare dimensions
    int match = (returnSize == expected_size);
    
    // Compare each row
    for(int i = 0; i < returnSize && match; i++) {{
        int expected_col_size = {col_sizes[0] if len(col_sizes) > 0 else 0};
        for(int j = 0; j < expected_col_size && match; j++) {{
            if(result[i][j] != expected[i][j]) match = 0;
        }}
    }}
    
    printf("%d\\n", match ? 1 : 0);
    return 0;
}}"""
            else:
                # 1D array return
                arg_names.append("&returnSize")
                call = f"{function_name}({', '.join(arg_names)})"
                
                expected_block = ""
                if len(expected) > 0:
                    expected_block = f"""
    static int expected_arr[] = {c_format_value(expected)};
    int* expected = expected_arr;"""
                else:
                    expected_block = "\n    int* expected = NULL;"

                test_code_main = f"""
int main() {{
{chr(10).join(arg_setup)}
    int returnSize = 0;
    int* result = {call};
{expected_block}
    int expected_size = {len(expected)};
    int match = (returnSize == expected_size);
    for(int j=0; j<returnSize && match; j++) {{
        if(result[j] != expected[j]) match = 0;
    }}
    printf("%d\\n", match ? 1 : 0);
    if (result) free(result);
    return 0;
}}"""
        elif isinstance(expected, bool):
            # Boolean return (like isAnagram)
            call = f"{function_name}({', '.join(arg_names)})"
            test_code_main = f"""
int main() {{
{chr(10).join(arg_setup)}
    bool result = {call};
    printf("%d\\n", result == {c_format_value(expected)} ? 1 : 0);
    return 0;
}}"""
        else:
            # Scalar return (int, etc.)
            call = f"{function_name}({', '.join(arg_names)})"
            test_code_main = f"""
int main() {{
{chr(10).join(arg_setup)}
    int result = {call};
    printf("%d\\n", result == {c_format_value(expected)} ? 1 : 0);
    return 0;
}}"""
    
    else:
        # Scalar input
        test_code_main = f"""
int main() {{
    auto result = {function_name}({c_format_value(inp)});
    printf("%d\\n", result == {c_format_value(expected)} ? 1 : 0);
    return 0;
}}"""
    
    return f"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

{user_code}

{test_code_main}
"""


def wrap_r_for_piston(user_code: str, test_cases: list, function_name: str) -> str:
    """Create R code with test runner - generic version for all problem types"""
    
    def r_format_value(val):
        """Convert Python value to R syntax"""
        if isinstance(val, list):
            if len(val) == 0:
                return "c()"
            elif isinstance(val[0], list):
                # Nested list (matrix) - convert to R matrix properly
                # Flatten all values and create matrix with proper dimensions
                rows = len(val)
                cols = len(val[0]) if rows > 0 else 0
                
                # Flatten the 2D list
                flat_values = []
                for row in val:
                    flat_values.extend(row)
                
                # Create R matrix: matrix(c(values...), nrow=rows, ncol=cols, byrow=TRUE)
                values_str = ", ".join(map(str, flat_values))
                return f"matrix(c({values_str}), nrow={rows}, ncol={cols}, byrow=TRUE)"
            else:
                # Simple vector
                return "c(" + ", ".join(map(str, val)) + ")"
        elif isinstance(val, str):
            return f'"{val}"'
        elif isinstance(val, bool):
            return "TRUE" if val else "FALSE"
        elif val is None:
            return "NULL"
        else:
            return str(val)
    
    test_code = []
    for i, tc in enumerate(test_cases):
        inp = tc['input']
        expected = tc['output']
        
        # Build function call with all inputs
        if isinstance(inp, list):
            args = [r_format_value(arg) for arg in inp]
            call = f"{function_name}({', '.join(args)})"
        else:
            call = f"{function_name}({r_format_value(inp)})"
        
        # Format expected output
        expected_r = r_format_value(expected)
        
        # Generate test code with proper comparison
        if isinstance(expected, list):
            # Check if it's a 2D array (matrix)
            is_matrix = isinstance(expected[0], list) if expected else False
            
            if is_matrix:
                # For matrix outputs, use all.equal() which handles matrices properly
                test_code.append(f"""
total <- total + 1
result{i} <- {call}
expected{i} <- {expected_r}
if (!is.null(result{i}) && is.matrix(result{i}) && is.matrix(expected{i}) && isTRUE(all.equal(result{i}, expected{i}))) {{
  passed <- passed + 1
}}""")
            else:
                # For vector outputs, use all() for element-wise comparison
                test_code.append(f"""
total <- total + 1
result{i} <- {call}
expected{i} <- {expected_r}
if (!is.null(result{i}) && !any(is.na(result{i})) && length(result{i}) == length(expected{i}) && all(result{i} == expected{i})) {{
  passed <- passed + 1
}}""")
        else:
            # For scalar outputs
            test_code.append(f"""
total <- total + 1
result{i} <- {call}
expected{i} <- {expected_r}
if (!is.null(result{i}) && !is.na(result{i}) && result{i} == expected{i}) {{
  passed <- passed + 1
}}""")
    
    return f"""
{user_code}

# Test runner
passed <- 0
total <- 0
{chr(10).join(test_code)}

cat(paste0('{{"passed":', passed, ',"total":', total, ',"results":[]}}'))
"""
