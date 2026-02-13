# Full dataset fetched from Neon DB

FULL_PROBLEM_DATA = [   {   'description': '\n'
                       '<p>You are given an <code>m x n</code> grid where each '
                       'cell is either:</p>\n'
                       '<ul>\n'
                       '<li><code>0</code> → empty cell</li>\n'
                       '<li><code>1</code> → obstacle</li>\n'
                       '</ul>\n'
                       '\n'
                       '<p>You start at the <strong>top-left corner</strong> '
                       '<code>(0,0)</code> and want to reach the '
                       '<strong>bottom-right corner</strong> '
                       '<code>(m-1,n-1)</code>.</p>\n'
                       '\n'
                       '<p>You can move <strong>up, down, left, or '
                       'right</strong>.</p>\n'
                       '\n'
                       '<p>You are also given an integer <code>k</code>, '
                       'representing the <strong>maximum number of obstacles '
                       'you can eliminate</strong>.</p>\n'
                       '\n'
                       '<p>Return <em>the minimum number of steps required to '
                       'reach the destination</em>. If it is not possible, '
                       'return <code>-1</code>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong>\n'
                       'grid = [[0,0,0],\n'
                       '        [1,1,0],\n'
                       '        [0,0,0],\n'
                       '        [0,1,1],\n'
                       '        [0,0,0]]\n'
                       'k = 1\n'
                       '\n'
                       '<strong>Output:</strong> 6\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong>\n'
                       'grid = [[0,1,1],\n'
                       '        [1,1,1],\n'
                       '        [1,0,0]]\n'
                       'k = 1\n'
                       '\n'
                       '<strong>Output:</strong> -1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>m == grid.length</code></li>\n'
                       '<li><code>n == grid[0].length</code></li>\n'
                       '<li><code>1 <= m, n <= 40</code></li>\n'
                       '<li><code>0 <= k <= m × n</code></li>\n'
                       '<li><code>grid[i][j]</code> is either <code>0</code> '
                       'or <code>1</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'shortestPath',
        'id': 'premium-29',
        'starter_code': {   'c': 'void shortestPath() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int shortestPath(vector<vector<int>>& '
                                   'grid, int k) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int shortestPath(int[][] grid, '
                                    'int k) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def shortestPath(grid, k):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'shortestPath <- function(grid, k) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Graph', 'BFS', 'Matrix', 'State Space Search'],
        'test_cases': [   {   'input': [   [   [0, 0, 0],
                                               [1, 1, 0],
                                               [0, 0, 0],
                                               [0, 1, 1],
                                               [0, 0, 0]],
                                           1],
                              'output': 6},
                          {   'input': [[[0, 1, 1], [1, 1, 1], [1, 0, 0]], 1],
                              'output': -1},
                          {   'input': [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0],
                              'output': 4},
                          {'input': [[[0]], 0], 'output': 0},
                          {'input': [[[0, 1], [1, 0]], 1], 'output': 2},
                          {'input': [[[0, 1], [1, 0]], 0], 'output': -1},
                          {   'input': [[[0, 0, 1], [1, 0, 0], [1, 1, 0]], 1],
                              'output': 4},
                          {   'input': [[[0, 1, 0], [1, 1, 0], [0, 0, 0]], 2],
                              'output': 4},
                          {   'input': [   [   [0, 1, 1, 1],
                                               [0, 0, 0, 0],
                                               [1, 1, 1, 0]],
                                           1],
                              'output': 5},
                          {'input': [[[0, 1], [0, 0]], 0], 'output': 2},
                          {'input': [[[0, 0], [1, 1]], 2], 'output': 2},
                          {   'input': [   [   [0, 1, 0, 1],
                                               [0, 1, 0, 1],
                                               [0, 0, 0, 0]],
                                           1],
                              'output': 5},
                          {   'input': [[[0, 1, 1], [0, 0, 1], [1, 0, 0]], 1],
                              'output': 4},
                          {   'input': [[[0, 0, 0], [1, 1, 1], [0, 0, 0]], 2],
                              'output': 4},
                          {   'input': [[[0, 1, 1, 1, 1], [0, 0, 0, 0, 0]], 0],
                              'output': 5}],
        'title': 'Shortest Path in a Grid with Obstacles Elimination',
        'titleSlug': 'shortest-path-in-a-grid-with-obstacles-elimination'},
    {   'description': '\n'
                       '<p>Given a signed 32-bit integer <code>x</code>, '
                       'return <code>x</code> <em>with its digits '
                       'reversed</em>. If reversing <code>x</code> causes the '
                       'value to go outside the signed 32-bit integer range '
                       '<code>[-2<sup>31</sup>, 2<sup>31</sup> - 1]</code>, '
                       'then return <code>0</code>.</p>\n'
                       '\n'
                       '<p><strong>Assume the environment does not allow you '
                       'to store 64-bit integers (signed or '
                       'unsigned).</strong></p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> x = 123\n'
                       '<strong>Output:</strong> 321\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> x = -123\n'
                       '<strong>Output:</strong> -321\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> x = 120\n'
                       '<strong>Output:</strong> 21\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>-2<sup>31</sup> <= x <= 2<sup>31</sup> - '
                       '1</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'reverseInteger',
        'id': 'premium-3',
        'starter_code': {   'c': 'int reverseInteger(int x) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int reverseInteger(int x) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int reverseInteger(int x) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def reverseInteger(x):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'reverseInteger <- function(x) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Math'],
        'test_cases': [   {'input': [123], 'output': 321},
                          {'input': [-123], 'output': -321},
                          {'input': [120], 'output': 21},
                          {'input': [0], 'output': 0},
                          {'input': [5], 'output': 5},
                          {'input': [-5], 'output': -5},
                          {'input': [100], 'output': 1},
                          {'input': [1000], 'output': 1},
                          {'input': [-1200], 'output': -21},
                          {'input': [1534236469], 'output': 0},
                          {'input': [1463847412], 'output': 2147483641},
                          {'input': [12], 'output': 21},
                          {'input': [-12], 'output': -21},
                          {'input': [121], 'output': 121},
                          {'input': [1221], 'output': 1221}],
        'title': 'Reverse Integer',
        'titleSlug': 'reverse-integer'},
    {   'description': '\n'
                       '<p>Given an integer array <code>nums</code>, move all '
                       '<code>0</code>s to the end of the array while '
                       'maintaining the relative order of the non-zero '
                       'elements.</p>\n'
                       '\n'
                       '<p>You must do this <strong>in-place</strong>, without '
                       'making a copy of the array.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [0,1,0,3,12]\n'
                       '<strong>Output:</strong> [1,3,12,0,0]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [0]\n'
                       '<strong>Output:</strong> [0]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>-2<sup>31</sup> <= nums[i] <= 2<sup>31</sup> '
                       '- 1</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'moveZeroes',
        'id': 'premium-34',
        'starter_code': {   'c': 'void moveZeroes(int* nums, int n) {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    void moveZeroes(vector<int>& nums) {\n'
                                   '        // Write your code here\n'
                                   '        \n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void moveZeroes(int[] nums) {\n'
                                    '        // Write your code here\n'
                                    '        \n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def moveZeroes(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'moveZeroes <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Two Pointers'],
        'test_cases': [   {   'input': [[0, 1, 0, 3, 12]],
                              'output': [1, 3, 12, 0, 0]},
                          {'input': [[0]], 'output': [0]},
                          {'input': [[1, 2, 3]], 'output': [1, 2, 3]},
                          {'input': [[0, 0, 0]], 'output': [0, 0, 0]},
                          {'input': [[1, 0, 1]], 'output': [1, 1, 0]},
                          {   'input': [[4, 2, 4, 0, 0, 3, 0, 5, 1]],
                              'output': [4, 2, 4, 3, 5, 1, 0, 0, 0]},
                          {'input': [[1]], 'output': [1]},
                          {'input': [[1, 0]], 'output': [1, 0]},
                          {'input': [[0, 1]], 'output': [1, 0]},
                          {   'input': [[2, 0, 3, 0, 4]],
                              'output': [2, 3, 4, 0, 0]},
                          {'input': [[-1, 0, -2, 0]], 'output': [-1, -2, 0, 0]},
                          {   'input': [[0, 5, 6, 0, 7]],
                              'output': [5, 6, 7, 0, 0]},
                          {'input': [[9, 8, 7, 0]], 'output': [9, 8, 7, 0]},
                          {'input': [[0, 9, 8, 7]], 'output': [9, 8, 7, 0]},
                          {'input': [[1, 0, 0, 1]], 'output': [1, 1, 0, 0]}],
        'title': 'Move Zeroes',
        'titleSlug': 'move-zeroes'},
    {   'description': '\n'
                       '<p>A message containing letters from <code>A-Z</code> '
                       'is encoded using the following mapping:</p>\n'
                       '\n'
                       '<pre>\n'
                       '\'A\' -> "1"\n'
                       '\'B\' -> "2"\n'
                       '...\n'
                       '\'Z\' -> "26"\n'
                       '</pre>\n'
                       '\n'
                       '<p>Given a string <code>s</code> containing only '
                       'digits, return <em>the number of ways to decode '
                       'it</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "12"\n'
                       '<strong>Output:</strong> 2\n'
                       '<strong>Explanation:</strong>\n'
                       '"12" can be decoded as "AB" (1 2) or "L" (12).\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "226"\n'
                       '<strong>Output:</strong> 3\n'
                       '<strong>Explanation:</strong>\n'
                       '"226" can be decoded as "BZ" (2 26), "VF" (22 6), or '
                       '"BBF" (2 2 6).\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "0"\n'
                       '<strong>Output:</strong> 0\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= s.length <= 100</code></li>\n'
                       '<li><code>s</code> contains only digits</li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'numDecodings',
        'id': 'premium-42',
        'starter_code': {   'c': 'int numDecodings(char* s) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int numDecodings(string s) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int numDecodings(String s) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def numDecodings(s):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'numDecodings <- function(s) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Dynamic Programming'],
        'test_cases': [   {'input': ['12'], 'output': 2},
                          {'input': ['226'], 'output': 3},
                          {'input': ['0'], 'output': 0},
                          {'input': ['06'], 'output': 0},
                          {'input': ['10'], 'output': 1},
                          {'input': ['27'], 'output': 1},
                          {'input': ['101'], 'output': 1},
                          {'input': ['110'], 'output': 1},
                          {'input': ['100'], 'output': 0},
                          {'input': ['11106'], 'output': 2},
                          {'input': ['1234'], 'output': 3},
                          {'input': ['2101'], 'output': 1},
                          {'input': ['301'], 'output': 0},
                          {'input': ['2611055971756562'], 'output': 4},
                          {'input': ['111111'], 'output': 13}],
        'title': 'Decode Ways',
        'titleSlug': 'decode-ways'},
    {   'description': '\n'
                       '<p>Given an <code>m x n</code> 2D binary grid '
                       '<code>grid</code> which represents a map of '
                       "<code>'1'</code>s (land) and <code>'0'</code>s "
                       '(water), return <em>the number of islands</em>.</p>\n'
                       '\n'
                       '<p>An <strong>island</strong> is surrounded by water '
                       'and is formed by connecting adjacent lands '
                       'horizontally or vertically.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> grid = [\n'
                       '  ["1","1","1","1","0"],\n'
                       '  ["1","1","0","1","0"],\n'
                       '  ["1","1","0","0","0"],\n'
                       '  ["0","0","0","0","0"]\n'
                       ']\n'
                       '<strong>Output:</strong> 1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> grid = [\n'
                       '  ["1","1","0","0","0"],\n'
                       '  ["1","1","0","0","0"],\n'
                       '  ["0","0","1","0","0"],\n'
                       '  ["0","0","0","1","1"]\n'
                       ']\n'
                       '<strong>Output:</strong> 3\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>m == grid.length</code></li>\n'
                       '<li><code>n == grid[i].length</code></li>\n'
                       '<li><code>1 <= m, n <= 300</code></li>\n'
                       "<li><code>grid[i][j]</code> is <code>'0'</code> or "
                       "<code>'1'</code>.</li>\n"
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'numIslands',
        'id': 'premium-18',
        'starter_code': {   'c': 'int numIslands(char grid[][100], int m, int '
                                 'n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int numIslands(vector<vector<char>>& '
                                   'grid) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int numIslands(char[][] grid) '
                                    '{\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def numIslands(grid):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'numIslands <- function(grid, m, n) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'DFS', 'BFS', 'Union Find', 'Matrix'],
        'test_cases': [   {   'input': [   [   ['1', '1', '1', '1', '0'],
                                               ['1', '1', '0', '1', '0'],
                                               ['1', '1', '0', '0', '0'],
                                               ['0', '0', '0', '0', '0']]],
                              'output': 1},
                          {   'input': [   [   ['1', '1', '0', '0', '0'],
                                               ['1', '1', '0', '0', '0'],
                                               ['0', '0', '1', '0', '0'],
                                               ['0', '0', '0', '1', '1']]],
                              'output': 3},
                          {'input': [[['1']]], 'output': 1},
                          {'input': [[['0']]], 'output': 0},
                          {'input': [[['0', '0'], ['0', '0']]], 'output': 0},
                          {'input': [[['1', '1'], ['1', '1']]], 'output': 1},
                          {'input': [[['1', '0'], ['0', '1']]], 'output': 2},
                          {'input': [[['1', '0', '1', '0', '1']]], 'output': 3},
                          {   'input': [[['1'], ['0'], ['1'], ['0'], ['1']]],
                              'output': 3},
                          {   'input': [   [   ['1', '1', '0', '0', '0'],
                                               ['1', '1', '0', '0', '0'],
                                               ['0', '0', '1', '0', '0'],
                                               ['0', '0', '0', '1', '1'],
                                               ['0', '0', '0', '1', '1']]],
                              'output': 3},
                          {   'input': [   [   ['1', '0', '1'],
                                               ['0', '1', '0'],
                                               ['1', '0', '1']]],
                              'output': 5},
                          {   'input': [   [   ['1', '1', '1'],
                                               ['1', '0', '1'],
                                               ['1', '1', '1']]],
                              'output': 1},
                          {'input': [[['1', '1'], ['0', '0']]], 'output': 1},
                          {   'input': [   [   ['1', '0', '0'],
                                               ['0', '1', '0'],
                                               ['0', '0', '1']]],
                              'output': 3},
                          {   'input': [   [   ['1', '0', '1', '0', '1'],
                                               ['0', '0', '0', '0', '0'],
                                               ['1', '0', '1', '0', '1']]],
                              'output': 6}],
        'title': 'Number of Islands',
        'titleSlug': 'number-of-islands'},
    {   'description': '\n'
                       '<p>You are a professional robber planning to rob '
                       'houses along a street. Each house has a certain amount '
                       'of money stashed, the only constraint stopping you '
                       'from robbing each of them is that adjacent houses have '
                       'security systems connected and <strong>it will '
                       'automatically contact the police if two adjacent '
                       'houses were broken into on the same '
                       'night</strong>.</p>\n'
                       '\n'
                       '<p>Given an integer array <code>nums</code> '
                       'representing the amount of money of each house, return '
                       '<em>the maximum amount of money you can rob tonight '
                       '<strong>without alerting the '
                       'police</strong></em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,2,3,1]\n'
                       '<strong>Output:</strong> 4\n'
                       '<strong>Explanation:</strong> Rob house 1 (money = 1) '
                       'and then rob house 3 (money = 3).\n'
                       'Total amount you can rob = 1 + 3 = 4.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [2,7,9,3,1]\n'
                       '<strong>Output:</strong> 12\n'
                       '<strong>Explanation:</strong> Rob house 1 (money = 2), '
                       'rob house 3 (money = 9) and rob house 5 (money = 1).\n'
                       'Total amount you can rob = 2 + 9 + 1 = 12.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= 100</code></li>\n'
                       '<li><code>0 <= nums[i] <= 400</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'rob',
        'id': 'premium-13',
        'starter_code': {   'c': 'int rob(int* nums, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int rob(vector<int>& nums) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int rob(int[] nums) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def rob(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'rob <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Dynamic Programming'],
        'test_cases': [   {'input': [[1, 2, 3, 1]], 'output': 4},
                          {'input': [[2, 7, 9, 3, 1]], 'output': 12},
                          {'input': [[5]], 'output': 5},
                          {'input': [[100]], 'output': 100},
                          {'input': [[1, 2]], 'output': 2},
                          {'input': [[2, 1]], 'output': 2},
                          {'input': [[5, 5]], 'output': 5},
                          {'input': [[0, 0, 0]], 'output': 0},
                          {'input': [[5, 1, 5, 1, 5]], 'output': 15},
                          {'input': [[1, 5, 1, 5, 1]], 'output': 11},
                          {'input': [[1, 2, 3, 4, 5]], 'output': 9},
                          {'input': [[5, 4, 3, 2, 1]], 'output': 9},
                          {'input': [[100, 1, 1, 100]], 'output': 200},
                          {'input': [[50, 10, 50, 10, 50]], 'output': 150},
                          {'input': [[1, 2, 3]], 'output': 4},
                          {'input': [[10, 5, 2]], 'output': 12},
                          {'input': [[2, 1, 1, 2]], 'output': 4}],
        'title': 'House Robber',
        'titleSlug': 'house-robber'},
    {   'description': '\n'
                       '<p>You are given an integer array <code>coins</code> '
                       'representing coins of different denominations and an '
                       'integer <code>amount</code> representing a total '
                       'amount of money.</p>\n'
                       '\n'
                       '<p>Return <em>the fewest number of coins that you need '
                       'to make up that amount</em>. If that amount of money '
                       'cannot be made up by any combination of the coins, '
                       'return <code>-1</code>.</p>\n'
                       '\n'
                       '<p>You may assume that you have an infinite number of '
                       'each kind of coin.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> coins = [1,2,5], amount = 11\n'
                       '<strong>Output:</strong> 3\n'
                       '<strong>Explanation:</strong> 11 = 5 + 5 + 1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> coins = [2], amount = 3\n'
                       '<strong>Output:</strong> -1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> coins = [1], amount = 0\n'
                       '<strong>Output:</strong> 0\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= coins.length <= 12</code></li>\n'
                       '<li><code>1 <= coins[i] <= 2<sup>31</sup> - '
                       '1</code></li>\n'
                       '<li><code>0 <= amount <= 10<sup>4</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'coinChange',
        'id': 'premium-14',
        'starter_code': {   'c': 'int coinChange(int* coins, int n, int '
                                 'amount) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int coinChange(vector<int>& coins, int '
                                   'amount) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int coinChange(int[] coins, '
                                    'int amount) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def coinChange(coins, amount):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'coinChange <- function(coins, amount) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Dynamic Programming', 'BFS'],
        'test_cases': [   {'input': [[1, 2, 5], 11], 'output': 3},
                          {'input': [[2], 3], 'output': -1},
                          {'input': [[1], 0], 'output': 0},
                          {'input': [[5], 5], 'output': 1},
                          {'input': [[1], 1], 'output': 1},
                          {'input': [[1, 3, 4], 6], 'output': 2},
                          {'input': [[1, 2, 5], 100], 'output': 20},
                          {'input': [[1, 5, 10, 25], 99], 'output': 9},
                          {'input': [[2, 5], 3], 'output': -1},
                          {'input': [[3], 2], 'output': -1},
                          {'input': [[1], 10], 'output': 10},
                          {'input': [[1, 2], 10], 'output': 5},
                          {'input': [[1, 2, 5], 0], 'output': 0},
                          {'input': [[10, 20, 50], 100], 'output': 2},
                          {'input': [[2, 3, 5], 13], 'output': 3}],
        'title': 'Coin Change',
        'titleSlug': 'coin-change'},
    {   'description': '\n'
                       '<p>Given an integer array <code>nums</code> sorted in '
                       '<strong>non-decreasing order</strong>, remove the '
                       'duplicates <strong>in-place</strong> such that each '
                       'unique element appears only <strong>once</strong>. The '
                       '<strong>relative order</strong> of the elements should '
                       'be kept the <strong>same</strong>. Return <em>the '
                       'number of unique elements</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,1,2]\n'
                       '<strong>Output:</strong> 2, nums = [1,2,_]\n'
                       '<strong>Explanation:</strong> Your function should '
                       'return k = 2.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [0,0,1,1,1,2,2,3,3,4]\n'
                       '<strong>Output:</strong> 5, nums = '
                       '[0,1,2,3,4,_,_,_,_,_]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= 3 * '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>-100 <= nums[i] <= 100</code></li>\n'
                       '<li><code>nums</code> is sorted in '
                       '<strong>non-decreasing</strong> order.</li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'removeDuplicates',
        'id': 'premium-15',
        'starter_code': {   'c': 'int removeDuplicates(int* nums, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int removeDuplicates(vector<int>& '
                                   'nums) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int removeDuplicates(int[] '
                                    'nums) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def removeDuplicates(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'removeDuplicates <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Two Pointers'],
        'test_cases': [   {'input': [[1, 1, 2]], 'output': 2},
                          {   'input': [[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]],
                              'output': 5},
                          {'input': [[1, 2, 3, 4, 5]], 'output': 5},
                          {'input': [[1]], 'output': 1},
                          {'input': [[1, 1, 1, 1]], 'output': 1},
                          {'input': [[5, 5]], 'output': 1},
                          {'input': [[1, 2]], 'output': 2},
                          {'input': [[1, 1]], 'output': 1},
                          {'input': [[-3, -1, 0, 0, 0, 3, 3]], 'output': 4},
                          {   'input': [   [   1,
                                               1,
                                               1,
                                               2,
                                               2,
                                               2,
                                               3,
                                               3,
                                               3,
                                               4,
                                               4,
                                               4,
                                               5,
                                               5,
                                               5]],
                              'output': 5},
                          {'input': [[1, 1, 1, 1, 1, 2]], 'output': 2},
                          {'input': [[1, 2, 2, 2, 2, 2]], 'output': 2},
                          {'input': [[0, 0, 0, 1, 2]], 'output': 3},
                          {'input': [[1, 1, 2, 2, 3, 3]], 'output': 3},
                          {'input': [[1, 1, 1, 1, 1, 1, 1, 1, 2]], 'output': 2},
                          {'input': [[1, 1, 3, 3, 5, 5, 7, 7]], 'output': 4}],
        'title': 'Remove Duplicates from Sorted Array',
        'titleSlug': 'remove-duplicates-from-sorted-array'},
    {   'description': '\n'
                       '<p>You are given an integer array <code>height</code> '
                       'of length <code>n</code>. There are <code>n</code> '
                       'vertical lines drawn such that the two endpoints of '
                       'the <code>i<sup>th</sup></code> line are <code>(i, '
                       '0)</code> and <code>(i, height[i])</code>.</p>\n'
                       '\n'
                       '<p>Find two lines that together with the x-axis form a '
                       'container, such that the container contains the most '
                       'water.</p>\n'
                       '\n'
                       '<p>Return <em>the maximum amount of water a container '
                       'can store</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> height = [1,8,6,2,5,4,8,3,7]\n'
                       '<strong>Output:</strong> 49\n'
                       '<strong>Explanation:</strong> The max area of water '
                       'the container can contain is 49.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> height = [1,1]\n'
                       '<strong>Output:</strong> 1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>n == height.length</code></li>\n'
                       '<li><code>2 <= n <= 10<sup>5</sup></code></li>\n'
                       '<li><code>0 <= height[i] <= '
                       '10<sup>4</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'maxArea',
        'id': 'premium-16',
        'starter_code': {   'c': 'int maxArea(int* height, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int maxArea(vector<int>& height) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int maxArea(int[] height) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def maxArea(height):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'maxArea <- function(height) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Two Pointers', 'Greedy'],
        'test_cases': [   {   'input': [[1, 8, 6, 2, 5, 4, 8, 3, 7]],
                              'output': 49},
                          {'input': [[1, 1]], 'output': 1},
                          {'input': [[4, 3, 2, 1, 4]], 'output': 16},
                          {'input': [[1, 2, 3, 4, 5]], 'output': 6},
                          {'input': [[1, 2, 4, 3]], 'output': 4},
                          {'input': [[5, 4, 3, 2, 1]], 'output': 6},
                          {'input': [[5, 5, 5, 5]], 'output': 15},
                          {'input': [[3, 3, 3]], 'output': 6},
                          {'input': [[10, 1, 1, 1, 10]], 'output': 40},
                          {'input': [[1, 3, 2, 5, 25, 24, 5]], 'output': 24},
                          {'input': [[0, 2, 0]], 'output': 0},
                          {'input': [[1, 2, 1]], 'output': 2},
                          {'input': [[3, 1, 3]], 'output': 6},
                          {'input': [[100, 50, 100]], 'output': 200},
                          {'input': [[1, 100, 100, 1]], 'output': 100}],
        'title': 'Container With Most Water',
        'titleSlug': 'container-with-most-water'},
    {   'description': '\n'
                       '<p>Given an integer array nums, return all the '
                       'triplets <code>[nums[i], nums[j], nums[k]]</code> such '
                       'that <code>i != j</code>, <code>i != k</code>, and '
                       '<code>j != k</code>, and <code>nums[i] + nums[j] + '
                       'nums[k] == 0</code>.</p>\n'
                       '\n'
                       '<p>Notice that the solution set must not contain '
                       'duplicate triplets.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [-1,0,1,2,-1,-4]\n'
                       '<strong>Output:</strong> [[-1,-1,2],[-1,0,1]]\n'
                       '<strong>Explanation:</strong> The distinct triplets '
                       'are [-1,0,1] and [-1,-1,2].\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [0,0,0]\n'
                       '<strong>Output:</strong> [[0,0,0]]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>3 <= nums.length <= 3000</code></li>\n'
                       '<li><code>-10<sup>5</sup> <= nums[i] <= '
                       '10<sup>5</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'threeSum',
        'id': 'premium-17',
        'starter_code': {   'c': 'void threeSum(int* nums, int n) {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    void threeSum() {\n'
                                   '        // Write your code here\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void threeSum() {\n'
                                    '        // Write your code here\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def threeSum(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'threeSum <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Two Pointers', 'Sorting'],
        'test_cases': [   {   'input': [[-1, 0, 1, 2, -1, -4]],
                              'output': [[-1, -1, 2], [-1, 0, 1]]},
                          {'input': [[0, 1, 1]], 'output': []},
                          {'input': [[0, 0, 0]], 'output': [[0, 0, 0]]},
                          {'input': [[1, 2, 3]], 'output': []},
                          {'input': [[1, 1, 1]], 'output': []},
                          {'input': [[-5, -4, -3, -2, -1]], 'output': []},
                          {'input': [[-1, 1, 2, 3]], 'output': []},
                          {'input': [[-2, 0, 0, 2, 2]], 'output': [[-2, 0, 2]]},
                          {   'input': [   [   -4,
                                               -2,
                                               -2,
                                               -2,
                                               0,
                                               1,
                                               2,
                                               2,
                                               2,
                                               3,
                                               3,
                                               4,
                                               4,
                                               6,
                                               6]],
                              'output': [   [-4, -2, 6],
                                            [-4, 0, 4],
                                            [-4, 1, 3],
                                            [-4, 2, 2],
                                            [-2, -2, 4],
                                            [-2, 0, 2]]},
                          {'input': [[0, 0, 0, 0]], 'output': [[0, 0, 0]]},
                          {'input': [[0, 0, 1]], 'output': []},
                          {'input': [[-1, 0, 1]], 'output': [[-1, 0, 1]]},
                          {'input': [[-10, 0, 10]], 'output': [[-10, 0, 10]]},
                          {'input': [[1, 1, -2]], 'output': [[-2, 1, 1]]},
                          {'input': [[-1, -1, 2]], 'output': [[-1, -1, 2]]}],
        'title': '3Sum',
        'titleSlug': '3sum'},
    {   'description': '\n'
                       '<p>Given <code>n</code> non-negative integers '
                       'representing an elevation map where the width of each '
                       'bar is <code>1</code>, compute how much water it can '
                       'trap after raining.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> height = '
                       '[0,1,0,2,1,0,1,3,2,1,2,1]\n'
                       '<strong>Output:</strong> 6\n'
                       '<strong>Explanation:</strong> 6 units of rain water '
                       'are being trapped.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> height = [4,2,0,3,2,5]\n'
                       '<strong>Output:</strong> 9\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>n == height.length</code></li>\n'
                       '<li><code>1 <= n <= 2 * 10<sup>4</sup></code></li>\n'
                       '<li><code>0 <= height[i] <= '
                       '10<sup>5</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'trap',
        'id': 'premium-19',
        'starter_code': {   'c': 'int trap(int* height, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int trap(vector<int>& height) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int trap(int[] height) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def trap(height):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'trap <- function(height) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Two Pointers', 'Dynamic Programming', 'Stack'],
        'test_cases': [   {   'input': [[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]],
                              'output': 6},
                          {'input': [[4, 2, 0, 3, 2, 5]], 'output': 9},
                          {'input': [[1, 2, 3, 4, 5]], 'output': 0},
                          {'input': [[5, 4, 3, 2, 1]], 'output': 0},
                          {'input': [[5]], 'output': 0},
                          {'input': [[1, 1]], 'output': 0},
                          {'input': [[3, 3, 3, 3]], 'output': 0},
                          {'input': [[3, 0, 2, 0, 4]], 'output': 7},
                          {'input': [[4, 0, 0, 4]], 'output': 8},
                          {'input': [[2, 1, 2, 1, 2]], 'output': 2},
                          {'input': [[0, 0, 0]], 'output': 0},
                          {'input': [[3, 0, 3]], 'output': 3},
                          {'input': [[5, 0, 5]], 'output': 5},
                          {'input': [[5, 2, 1, 2, 1, 5]], 'output': 14},
                          {'input': [[10, 1, 1, 10]], 'output': 18}],
        'title': 'Trapping Rain Water',
        'titleSlug': 'trapping-rain-water'},
    {   'description': '\n'
                       '<p>Given an integer <code>x</code>, return '
                       '<code>true</code> if <code>x</code> is a '
                       '<strong>palindrome</strong>, and <code>false</code> '
                       'otherwise.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> x = 121\n'
                       '<strong>Output:</strong> true\n'
                       '<strong>Explanation:</strong> 121 reads as 121 from '
                       'left to right and from right to left.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> x = -121\n'
                       '<strong>Output:</strong> false\n'
                       '<strong>Explanation:</strong> From left to right, it '
                       'reads -121. From right to left, it becomes 121-. '
                       'Therefore it is not a palindrome.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> x = 10\n'
                       '<strong>Output:</strong> false\n'
                       '<strong>Explanation:</strong> Reads 01 from right to '
                       'left. Therefore it is not a palindrome.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>-2<sup>31</sup> <= x <= 2<sup>31</sup> - '
                       '1</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'isPalindrome',
        'id': 'premium-2',
        'starter_code': {   'c': 'int isPalindrome(int x) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    bool isPalindrome(int x) {\n'
                                   '        // Write your code here\n'
                                   '        return false;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public boolean isPalindrome(int x) {\n'
                                    '        // Write your code here\n'
                                    '        return false;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def isPalindrome(x):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'isPalindrome <- function(x) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Math'],
        'test_cases': [   {'input': [121], 'output': True},
                          {'input': [12321], 'output': True},
                          {'input': [1221], 'output': True},
                          {'input': [123], 'output': False},
                          {'input': [10], 'output': False},
                          {'input': [-121], 'output': False},
                          {'input': [0], 'output': True},
                          {'input': [1], 'output': True},
                          {'input': [9], 'output': True},
                          {'input': [1000000001], 'output': True},
                          {'input': [123454321], 'output': True},
                          {'input': [100], 'output': False},
                          {'input': [1000], 'output': False},
                          {'input': [-101], 'output': False},
                          {'input': [-1], 'output': False}],
        'title': 'Palindrome Number',
        'titleSlug': 'palindrome-number'},
    {   'description': '\n'
                       '<p>You are given an array of <code>k</code> '
                       'linked-lists <code>lists</code>, each sorted in '
                       'ascending order.</p>\n'
                       '\n'
                       '<p><em>Merge all the linked-lists into one sorted '
                       'linked-list and return it.</em></p>\n'
                       '\n'
                       '<p><strong>Note:</strong> For simplicity, this problem '
                       'uses arrays instead of linked lists.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> lists = '
                       '[[1,4,5],[1,3,4],[2,6]]\n'
                       '<strong>Output:</strong> [1,1,2,3,4,4,5,6]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> lists = []\n'
                       '<strong>Output:</strong> []\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>k == lists.length</code></li>\n'
                       '<li><code>0 <= k <= 10<sup>4</sup></code></li>\n'
                       '<li><code>lists[i]</code> is sorted in '
                       '<strong>ascending</strong> order.</li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'mergeKLists',
        'id': 'premium-20',
        'starter_code': {   'c': 'void mergeKLists() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    void mergeKLists() {\n'
                                   '        // Write your code here\n'
                                   '        \n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void mergeKLists() {\n'
                                    '        // Write your code here\n'
                                    '        \n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def mergeKLists():\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'mergeKLists <- function() {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Linked List', 'Divide and Conquer', 'Heap', 'Merge Sort'],
        'test_cases': [   {   'input': [[[1, 4, 5], [1, 3, 4], [2, 6]]],
                              'output': [1, 1, 2, 3, 4, 4, 5, 6]},
                          {'input': [[[1, 2], [3, 4]]], 'output': [1, 2, 3, 4]},
                          {'input': [[[]]], 'output': []},
                          {'input': [[[], []]], 'output': []},
                          {'input': [[[], [1]]], 'output': [1]},
                          {'input': [[[1, 2, 3]]], 'output': [1, 2, 3]},
                          {   'input': [[[1], [2], [3], [4]]],
                              'output': [1, 2, 3, 4]},
                          {   'input': [[[1, 5], [2, 6], [3, 7]]],
                              'output': [1, 2, 3, 5, 6, 7]},
                          {   'input': [[[-2, -1], [-3, 0], [1, 2]]],
                              'output': [-3, -2, -1, 0, 1, 2]},
                          {'input': [[[1, 1], [1, 1]]], 'output': [1, 1, 1, 1]},
                          {   'input': [[[1], [1, 2, 3, 4], [2]]],
                              'output': [1, 1, 2, 2, 3, 4]},
                          {   'input': [[[1, 10], [5, 20], [15, 30]]],
                              'output': [1, 5, 10, 15, 20, 30]},
                          {   'input': [[[0, 2], [0, 3], [0, 4]]],
                              'output': [0, 0, 0, 2, 3, 4]},
                          {   'input': [[[1, 3, 5], [2, 4, 6]]],
                              'output': [1, 2, 3, 4, 5, 6]}],
        'title': 'Merge K Sorted Lists',
        'titleSlug': 'merge-k-sorted-lists'},
    {   'description': '\n'
                       '<p>You are given an array <code>prices</code> where '
                       '<code>prices[i]</code> is the price of a given stock '
                       'on the <code>i<sup>th</sup></code> day.</p>\n'
                       '\n'
                       '<p>You want to maximize your profit by choosing a '
                       '<strong>single day</strong> to buy one stock and '
                       'choosing a <strong>different day in the '
                       'future</strong> to sell that stock.</p>\n'
                       '\n'
                       '<p>Return <em>the maximum profit you can achieve from '
                       'this transaction</em>. If you cannot achieve any '
                       'profit, return <code>0</code>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> prices = [7,1,5,3,6,4]\n'
                       '<strong>Output:</strong> 5\n'
                       '<strong>Explanation:</strong> Buy on day 2 (price = 1) '
                       'and sell on day 5 (price = 6).\n'
                       'Profit = 6 − 1 = 5\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> prices = [7,6,4,3,1]\n'
                       '<strong>Output:</strong> 0\n'
                       '<strong>Explanation:</strong> Prices are decreasing, '
                       'so no profit is possible.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= prices.length <= '
                       '10<sup>5</sup></code></li>\n'
                       '<li><code>0 <= prices[i] <= '
                       '10<sup>4</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'maxProfit',
        'id': 'premium-22',
        'starter_code': {   'c': 'int maxProfit(int* prices, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int maxProfit(vector<int>& prices) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int maxProfit(int[] prices) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def maxProfit(prices):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'maxProfit <- function(prices) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Dynamic Programming', 'Greedy'],
        'test_cases': [   {'input': [[7, 1, 5, 3, 6, 4]], 'output': 5},
                          {'input': [[7, 6, 4, 3, 1]], 'output': 0},
                          {'input': [[1, 2, 3, 4, 5]], 'output': 4},
                          {'input': [[5, 4, 3, 2, 1]], 'output': 0},
                          {'input': [[2, 4, 1]], 'output': 2},
                          {'input': [[3, 3, 5, 0, 0, 3, 1, 4]], 'output': 4},
                          {'input': [[1]], 'output': 0},
                          {'input': [[2, 1]], 'output': 0},
                          {'input': [[1, 2]], 'output': 1},
                          {'input': [[6, 1, 3, 2, 4, 7]], 'output': 6},
                          {'input': [[10, 9, 8, 7]], 'output': 0},
                          {'input': [[1, 10]], 'output': 9},
                          {'input': [[4, 2, 8]], 'output': 6},
                          {'input': [[2, 7, 1, 4]], 'output': 5},
                          {'input': [[0, 5, 3, 6]], 'output': 6}],
        'title': 'Best Time to Buy and Sell Stock',
        'titleSlug': 'best-time-to-buy-and-sell-stock'},
    {   'description': '\n'
                       '<p>You are given a string <code>s</code> and an '
                       'integer <code>k</code>.</p>\n'
                       '\n'
                       '<p>You can choose <strong>at most k '
                       'characters</strong> in the string and replace them '
                       'with any other character.</p>\n'
                       '\n'
                       '<p>Return <em>the length of the longest substring '
                       'containing the same letter you can obtain after '
                       'performing at most <code>k</code> '
                       'replacements</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "ABAB", k = 2\n'
                       '<strong>Output:</strong> 4\n'
                       "<strong>Explanation:</strong> Replace both 'A's with "
                       "'B' or both 'B's with 'A'.\n"
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "AABABBA", k = 1\n'
                       '<strong>Output:</strong> 4\n'
                       "<strong>Explanation:</strong> Replace one 'A' with 'B' "
                       '→ "AABBBBA".\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= s.length <= 10<sup>5</sup></code></li>\n'
                       '<li><code>s</code> consists of only uppercase English '
                       'letters</li>\n'
                       '<li><code>0 <= k <= s.length</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'characterReplacement',
        'id': 'premium-23',
        'starter_code': {   'c': 'int characterReplacement(char* s, int k) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int characterReplacement(string s, int '
                                   'k) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int '
                                    'characterReplacement(String s, int k) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def characterReplacement(s, k):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'characterReplacement <- function(s, k) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Sliding Window', 'Hash Table'],
        'test_cases': [   {'input': ['ABAB', 2], 'output': 4},
                          {'input': ['AABABBA', 1], 'output': 4},
                          {'input': ['AAAA', 2], 'output': 4},
                          {'input': ['ABCDE', 1], 'output': 2},
                          {'input': ['BAAAB', 2], 'output': 5},
                          {'input': ['A', 0], 'output': 1},
                          {'input': ['AB', 0], 'output': 1},
                          {'input': ['AB', 1], 'output': 2},
                          {'input': ['AAABBC', 1], 'output': 4},
                          {'input': ['AAABBC', 2], 'output': 5},
                          {'input': ['AAABBC', 3], 'output': 6},
                          {'input': ['ABCDE', 2], 'output': 3},
                          {'input': ['AABA', 0], 'output': 2},
                          {'input': ['BBBB', 1], 'output': 4},
                          {'input': ['ABBBAC', 1], 'output': 4}],
        'title': 'Longest Repeating Character Replacement',
        'titleSlug': 'longest-repeating-character-replacement'},
    {   'description': '\n'
                       '<p>You are given a 2D image represented by an <code>m '
                       'x n</code> integer grid <code>image</code>, where '
                       '<code>image[i][j]</code> represents the pixel value of '
                       'the image.</p>\n'
                       '\n'
                       '<p>You are also given three integers:</p>\n'
                       '<ul>\n'
                       '<li><code>sr</code>: starting row</li>\n'
                       '<li><code>sc</code>: starting column</li>\n'
                       '<li><code>newColor</code>: the color to apply</li>\n'
                       '</ul>\n'
                       '\n'
                       '<p>Perform a <strong>flood fill</strong> on the image '
                       'starting from the pixel <code>(sr, sc)</code>.</p>\n'
                       '\n'
                       '<p>The flood fill changes the color of the starting '
                       'pixel and all connected pixels (4-directionally: up, '
                       'down, left, right) with the same original color to '
                       '<code>newColor</code>.</p>\n'
                       '\n'
                       '<p>Return <em>the modified image</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong>\n'
                       'image = [[1,1,1],\n'
                       '         [1,1,0],\n'
                       '         [1,0,1]]\n'
                       'sr = 1, sc = 1, newColor = 2\n'
                       '\n'
                       '<strong>Output:</strong>\n'
                       '[[2,2,2],\n'
                       ' [2,2,0],\n'
                       ' [2,0,1]]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong>\n'
                       'image = [[0,0,0],\n'
                       '         [0,0,0]]\n'
                       'sr = 0, sc = 0, newColor = 0\n'
                       '\n'
                       '<strong>Output:</strong>\n'
                       '[[0,0,0],\n'
                       ' [0,0,0]]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>m == image.length</code></li>\n'
                       '<li><code>n == image[i].length</code></li>\n'
                       '<li><code>1 <= m, n <= 50</code></li>\n'
                       '<li><code>0 <= image[i][j], newColor <= '
                       '65,535</code></li>\n'
                       '<li><code>0 <= sr < m</code></li>\n'
                       '<li><code>0 <= sc < n</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'floodFill',
        'id': 'premium-24',
        'starter_code': {   'c': 'void floodFill(int image[][100], int m, int '
                                 'n, int sr, int sc, int newColor) {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    void floodFill() {\n'
                                   '        // Write your code here\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int[][] floodFill(int[][] '
                                    'image, int sr, int sc, int newColor) {\n'
                                    '        // Write your code here\n'
                                    '        return new int[0][0];\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def floodFill(image, sr, sc, '
                                      'newColor):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'floodFill <- function(image, sr, sc, '
                                 'newColor) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Matrix', 'DFS', 'BFS'],
        'test_cases': [   {   'input': [   [[1, 1, 1], [1, 1, 0], [1, 0, 1]],
                                           1,
                                           1,
                                           2],
                              'output': [[2, 2, 2], [2, 2, 0], [2, 0, 1]]},
                          {   'input': [[[0, 0, 0], [0, 0, 0]], 0, 0, 0],
                              'output': [[0, 0, 0], [0, 0, 0]]},
                          {'input': [[[1]], 0, 0, 2], 'output': [[2]]},
                          {   'input': [[[1, 1], [1, 1]], 0, 0, 3],
                              'output': [[3, 3], [3, 3]]},
                          {   'input': [[[1, 1], [1, 0]], 0, 0, 2],
                              'output': [[2, 2], [2, 0]]},
                          {   'input': [[[2, 2, 2], [2, 2, 2]], 1, 1, 1],
                              'output': [[1, 1, 1], [1, 1, 1]]},
                          {   'input': [[[1, 2, 3], [4, 5, 6]], 0, 0, 9],
                              'output': [[9, 2, 3], [4, 5, 6]]},
                          {   'input': [   [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                                           2,
                                           2,
                                           0],
                              'output': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]},
                          {   'input': [[[1, 0, 1], [0, 1, 0]], 1, 1, 7],
                              'output': [[1, 0, 1], [0, 7, 0]]},
                          {   'input': [[[3, 3, 3], [3, 3, 3]], 0, 1, 8],
                              'output': [[8, 8, 8], [8, 8, 8]]},
                          {   'input': [[[1, 2], [3, 4]], 1, 1, 5],
                              'output': [[1, 2], [3, 5]]},
                          {   'input': [[[9, 9, 9]], 0, 1, 1],
                              'output': [[1, 1, 1]]},
                          {   'input': [[[5, 5, 5], [5, 0, 5]], 0, 0, 2],
                              'output': [[2, 2, 2], [2, 0, 2]]},
                          {   'input': [[[1, 1, 0], [1, 0, 1]], 0, 0, 4],
                              'output': [[4, 4, 0], [4, 0, 1]]},
                          {   'input': [[[8, 8], [8, 8]], 1, 1, 8],
                              'output': [[8, 8], [8, 8]]}],
        'title': 'Flood Fill',
        'titleSlug': 'flood-fill'},
    {   'description': '\n'
                       '<p>Given an array <code>nums</code> of size '
                       '<code>n</code>, return <em>the majority '
                       'element</em>.</p>\n'
                       '\n'
                       '<p>The majority element is the element that appears '
                       'more than <code>⌊n / 2⌋</code> times.</p>\n'
                       '\n'
                       '<p>You may assume that the majority element always '
                       'exists in the array.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [3,2,3]\n'
                       '<strong>Output:</strong> 3\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [2,2,1,1,1,2,2]\n'
                       '<strong>Output:</strong> 2\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>n == nums.length</code></li>\n'
                       '<li><code>1 <= n <= 5 × 10<sup>4</sup></code></li>\n'
                       '<li><code>-10<sup>9</sup> <= nums[i] <= '
                       '10<sup>9</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'majorityElement',
        'id': 'premium-25',
        'starter_code': {   'c': 'int majorityElement(int* nums, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int majorityElement(vector<int>& nums) '
                                   '{\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int majorityElement(int[] '
                                    'nums) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def majorityElement(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'majorityElement <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Hash Table', 'Boyer-Moore Voting Algorithm'],
        'test_cases': [   {'input': [[3, 2, 3]], 'output': 3},
                          {'input': [[2, 2, 1, 1, 1, 2, 2]], 'output': 2},
                          {'input': [[1]], 'output': 1},
                          {'input': [[1, 1]], 'output': 1},
                          {'input': [[1, 2, 1]], 'output': 1},
                          {'input': [[5, 5, 5, 5, 2, 3, 5]], 'output': 5},
                          {'input': [[-1, -1, -1, 2, 3]], 'output': -1},
                          {'input': [[9, 9, 9, 9, 1, 2, 3]], 'output': 9},
                          {'input': [[0, 0, 0, 0]], 'output': 0},
                          {   'input': [[1000000000, 1000000000, 1]],
                              'output': 1000000000},
                          {'input': [[2, 1, 2]], 'output': 2},
                          {'input': [[7, 7, 7, 3, 3]], 'output': 7},
                          {'input': [[4, 4, 4, 2, 4]], 'output': 4},
                          {'input': [[-5, -5, -5, -5, -1]], 'output': -5},
                          {'input': [[8, 8, 9, 8, 10]], 'output': 8}],
        'title': 'Majority Element',
        'titleSlug': 'majority-element'},
    {   'description': '\n'
                       '<p>Given two strings <code>s</code> and '
                       '<code>t</code>, return <em>the minimum window '
                       'substring of <code>s</code> such that every character '
                       'in <code>t</code> (including duplicates) is included '
                       'in the window</em>.</p>\n'
                       '\n'
                       '<p>If there is no such substring, return <em>an empty '
                       'string <code>""</code></em>.</p>\n'
                       '\n'
                       '<p>The answer is <strong>unique</strong>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "ADOBECODEBANC", t = '
                       '"ABC"\n'
                       '<strong>Output:</strong> "BANC"\n'
                       '<strong>Explanation:</strong> The smallest substring '
                       'containing A, B, and C is "BANC".\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "a", t = "a"\n'
                       '<strong>Output:</strong> "a"\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "a", t = "aa"\n'
                       '<strong>Output:</strong> ""\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= s.length, t.length <= '
                       '10<sup>5</sup></code></li>\n'
                       '<li><code>s</code> and <code>t</code> consist of '
                       'uppercase and lowercase English letters</li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'minWindow',
        'id': 'premium-27',
        'starter_code': {   'c': 'void minWindow() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    string minWindow(string s, string t) '
                                   '{\n'
                                   '        // Write your code here\n'
                                   '        return "";\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public String minWindow(String s, '
                                    'String t) {\n'
                                    '        // Write your code here\n'
                                    '        return "";\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def minWindow(s, t):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'minWindow <- function(s, t) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Sliding Window', 'Hash Table', 'Two Pointers'],
        'test_cases': [   {'input': ['ADOBECODEBANC', 'ABC'], 'output': 'BANC'},
                          {'input': ['a', 'a'], 'output': 'a'},
                          {'input': ['a', 'aa'], 'output': ''},
                          {'input': ['aa', 'aa'], 'output': 'aa'},
                          {'input': ['ab', 'b'], 'output': 'b'},
                          {'input': ['ab', 'a'], 'output': 'a'},
                          {'input': ['abc', 'ac'], 'output': 'abc'},
                          {   'input': ['aaflslflsldkalskaaa', 'aaa'],
                              'output': 'aaa'},
                          {   'input': ['thisisateststring', 'tist'],
                              'output': 'tstri'},
                          {   'input': ['aaaaaaaaaaaabbbbbcdd', 'abcdd'],
                              'output': 'abbbbbcdd'},
                          {'input': ['xyyzyzyx', 'xyz'], 'output': 'zyx'},
                          {'input': ['bba', 'ab'], 'output': 'ba'},
                          {'input': ['cabefgecdaecf', 'cae'], 'output': 'aec'},
                          {'input': ['abcdebdde', 'bde'], 'output': 'bdde'},
                          {   'input': ['aaabdabcefaecbef', 'abc'],
                              'output': 'abc'}],
        'title': 'Minimum Window Substring',
        'titleSlug': 'minimum-window-substring'},
    {   'description': '\n'
                       '<p>Given two strings <code>word1</code> and '
                       '<code>word2</code>, return <em>the minimum number of '
                       'operations required to convert <code>word1</code> into '
                       '<code>word2</code></em>.</p>\n'
                       '\n'
                       '<p>You are allowed to perform the following operations '
                       'on a word:</p>\n'
                       '<ul>\n'
                       '<li>Insert a character</li>\n'
                       '<li>Delete a character</li>\n'
                       '<li>Replace a character</li>\n'
                       '</ul>\n'
                       '\n'
                       '<p>This is also known as the <strong>Levenshtein '
                       'Distance</strong> problem.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> word1 = "horse", word2 = '
                       '"ros"\n'
                       '<strong>Output:</strong> 3\n'
                       '<strong>Explanation:</strong>\n'
                       "horse → rorse (replace 'h' with 'r')\n"
                       "rorse → rose (remove 'r')\n"
                       "rose → ros (remove 'e')\n"
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> word1 = "intention", word2 = '
                       '"execution"\n'
                       '<strong>Output:</strong> 5\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>0 <= word1.length, word2.length <= '
                       '500</code></li>\n'
                       '<li><code>word1</code> and <code>word2</code> consist '
                       'of lowercase English letters</li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'minDistance',
        'id': 'premium-28',
        'starter_code': {   'c': 'int minDistance(char* w1, char* w2) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int minDistance(string w1, string w2) '
                                   '{\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int minDistance(String w1, '
                                    'String w2) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def minDistance(w1, w2):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'minDistance <- function(w1, w2) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Dynamic Programming', 'String'],
        'test_cases': [   {'input': ['horse', 'ros'], 'output': 3},
                          {'input': ['intention', 'execution'], 'output': 5},
                          {'input': ['', 'a'], 'output': 1},
                          {'input': ['a', ''], 'output': 1},
                          {'input': ['', ''], 'output': 0},
                          {'input': ['a', 'a'], 'output': 0},
                          {'input': ['abc', 'yabd'], 'output': 2},
                          {'input': ['kitten', 'sitting'], 'output': 3},
                          {'input': ['flaw', 'lawn'], 'output': 2},
                          {'input': ['algorithm', 'altruistic'], 'output': 6},
                          {'input': ['distance', 'editing'], 'output': 5},
                          {'input': ['abcde', 'abc'], 'output': 2},
                          {'input': ['abc', 'abcde'], 'output': 2},
                          {'input': ['abcdef', 'azced'], 'output': 3},
                          {'input': ['aaaa', 'bbbb'], 'output': 4}],
        'title': 'Edit Distance',
        'titleSlug': 'edit-distance'},
    {   'description': '\n'
                       '<p>Given an array of integers <code>heights</code> '
                       "representing the histogram's bar heights, where the "
                       'width of each bar is <code>1</code>, return <em>the '
                       'area of the largest rectangle that can be formed '
                       'within the histogram</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> heights = [2,1,5,6,2,3]\n'
                       '<strong>Output:</strong> 10\n'
                       '<strong>Explanation:</strong>\n'
                       'The largest rectangle is formed by heights 5 and 6.\n'
                       'Area = 5 × 2 = 10\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> heights = [2,4]\n'
                       '<strong>Output:</strong> 4\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= heights.length <= '
                       '10<sup>5</sup></code></li>\n'
                       '<li><code>0 <= heights[i] <= '
                       '10<sup>4</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'largestRectangleArea',
        'id': 'premium-30',
        'starter_code': {   'c': 'int largestRectangleArea(int* heights, int '
                                 'n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int largestRectangleArea(vector<int>& '
                                   'heights) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int largestRectangleArea(int[] '
                                    'heights) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def largestRectangleArea(heights):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'largestRectangleArea <- function(heights) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Stack', 'Monotonic Stack'],
        'test_cases': [   {'input': [[2, 1, 5, 6, 2, 3]], 'output': 10},
                          {'input': [[2, 4]], 'output': 4},
                          {'input': [[1]], 'output': 1},
                          {'input': [[0]], 'output': 0},
                          {'input': [[1, 1, 1, 1]], 'output': 4},
                          {'input': [[4, 3, 2, 1]], 'output': 6},
                          {'input': [[1, 2, 3, 4, 5]], 'output': 9},
                          {'input': [[5, 4, 3, 2, 1]], 'output': 9},
                          {'input': [[2, 2, 2]], 'output': 6},
                          {'input': [[6, 2, 5, 4, 5, 1, 6]], 'output': 12},
                          {'input': [[2, 0, 2]], 'output': 2},
                          {'input': [[1, 0, 1]], 'output': 1},
                          {'input': [[4, 2, 0, 3, 2, 5]], 'output': 6},
                          {'input': [[10000]], 'output': 10000},
                          {'input': [[3, 6, 5, 7, 4, 8, 1, 0]], 'output': 20}],
        'title': 'Largest Rectangle in Histogram',
        'titleSlug': 'largest-rectangle-in-histogram'},
    {   'description': '\n'
                       '<p>Given a <code>rows x cols</code> binary matrix '
                       "filled with <code>'0'</code> and <code>'1'</code>, "
                       'find the <strong>largest rectangle containing only '
                       '1s</strong> and return <em>its area</em>.</p>\n'
                       '\n'
                       '<p>This problem extends the <strong>Largest Rectangle '
                       'in Histogram</strong> concept to a 2D matrix.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong>\n'
                       'matrix = [\n'
                       '  ["1","0","1","0","0"],\n'
                       '  ["1","0","1","1","1"],\n'
                       '  ["1","1","1","1","1"],\n'
                       '  ["1","0","0","1","0"]\n'
                       ']\n'
                       '<strong>Output:</strong> 6\n'
                       '<strong>Explanation:</strong> The largest rectangle of '
                       '1s has area = 6.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> matrix = [["0"]]\n'
                       '<strong>Output:</strong> 0\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> matrix = [["1"]]\n'
                       '<strong>Output:</strong> 1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>rows == matrix.length</code></li>\n'
                       '<li><code>cols == matrix[i].length</code></li>\n'
                       '<li><code>1 <= rows, cols <= 200</code></li>\n'
                       '<li><code>matrix[i][j]</code> is either '
                       "<code>'0'</code> or <code>'1'</code></li>\n"
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'maximalRectangle',
        'id': 'premium-31',
        'starter_code': {   'c': 'int maximalRectangle(char matrix[][100], int '
                                 'm, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int '
                                   'maximalRectangle(vector<vector<char>>& '
                                   'matrix) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int maximalRectangle(char[][] '
                                    'matrix) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def maximalRectangle(matrix):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'maximalRectangle <- function(matrix, m, n) '
                                 '{\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': [   'Array',
                    'Matrix',
                    'Stack',
                    'Dynamic Programming',
                    'Monotonic Stack'],
        'test_cases': [   {   'input': [   [   ['1', '0', '1', '0', '0'],
                                               ['1', '0', '1', '1', '1'],
                                               ['1', '1', '1', '1', '1'],
                                               ['1', '0', '0', '1', '0']]],
                              'output': 6},
                          {'input': [[['0']]], 'output': 0},
                          {'input': [[['1']]], 'output': 1},
                          {'input': [[['1', '1'], ['1', '1']]], 'output': 4},
                          {'input': [[['1', '0'], ['1', '0']]], 'output': 2},
                          {'input': [[['0', '0'], ['0', '0']]], 'output': 0},
                          {'input': [[['1', '1', '1', '1']]], 'output': 4},
                          {'input': [[['1'], ['1'], ['1']]], 'output': 3},
                          {'input': [[['1', '0', '1', '1', '1']]], 'output': 3},
                          {   'input': [   [   ['1', '1', '0', '1'],
                                               ['1', '1', '0', '1'],
                                               ['1', '1', '1', '1']]],
                              'output': 6},
                          {   'input': [   [   ['0', '1', '1', '0'],
                                               ['1', '1', '1', '1'],
                                               ['1', '1', '1', '1'],
                                               ['1', '1', '0', '0']]],
                              'output': 8},
                          {   'input': [[['1', '0', '1', '0', '1', '0']]],
                              'output': 1},
                          {   'input': [   [   ['1', '1', '1'],
                                               ['1', '1', '1'],
                                               ['1', '1', '1']]],
                              'output': 9},
                          {   'input': [   [   ['1', '0', '1'],
                                               ['1', '1', '1'],
                                               ['1', '1', '0']]],
                              'output': 4},
                          {   'input': [   [   ['0', '1', '0'],
                                               ['1', '1', '1'],
                                               ['0', '1', '0']]],
                              'output': 3}],
        'title': 'Maximal Rectangle',
        'titleSlug': 'maximal-rectangle'},
    {   'description': '\n'
                       '<p>Given an integer array <code>nums</code> and an '
                       'integer <code>k</code>, return <em>the '
                       '<code>k<sup>th</sup></code> largest element in the '
                       'array</em>.</p>\n'
                       '\n'
                       '<p>Note that it is the <code>k<sup>th</sup></code> '
                       'largest element in <strong>sorted order</strong>, not '
                       'the <code>k<sup>th</sup></code> distinct element.</p>\n'
                       '\n'
                       '<p>You must solve it <strong>without fully sorting the '
                       'array</strong>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [3,2,1,5,6,4], k = 2\n'
                       '<strong>Output:</strong> 5\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [3,2,3,1,2,4,5,5,6], k '
                       '= 4\n'
                       '<strong>Output:</strong> 4\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= '
                       '10<sup>5</sup></code></li>\n'
                       '<li><code>-10<sup>4</sup> <= nums[i] <= '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>1 <= k <= nums.length</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'findKthLargest',
        'id': 'premium-32',
        'starter_code': {   'c': 'int findKthLargest(int* nums, int n, int k) '
                                 '{\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int findKthLargest(vector<int>& nums, '
                                   'int k) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int findKthLargest(int[] nums, '
                                    'int k) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def findKthLargest(nums, k):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'findKthLargest <- function(nums, k) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Heap', 'Divide and Conquer', 'Quickselect'],
        'test_cases': [   {'input': [[3, 2, 1, 5, 6, 4], 2], 'output': 5},
                          {   'input': [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4],
                              'output': 4},
                          {'input': [[1], 1], 'output': 1},
                          {'input': [[2, 1], 1], 'output': 2},
                          {'input': [[2, 1], 2], 'output': 1},
                          {'input': [[1, 1, 1, 1], 2], 'output': 1},
                          {'input': [[5, 4, 3, 2, 1], 3], 'output': 3},
                          {'input': [[1, 2, 3, 4, 5], 5], 'output': 1},
                          {'input': [[-1, -2, -3, -4], 1], 'output': -1},
                          {'input': [[-1, -2, -3, -4], 4], 'output': -4},
                          {'input': [[7, 10, 4, 3, 20, 15], 3], 'output': 10},
                          {'input': [[100, 99, 98, 97], 2], 'output': 99},
                          {'input': [[5, 5, 5, 5, 5], 3], 'output': 5},
                          {   'input': [[9, 8, 7, 6, 5, 4, 3, 2, 1], 6],
                              'output': 4},
                          {'input': [[0, 0, 0, 0], 1], 'output': 0}],
        'title': 'Kth Largest Element in an Array',
        'titleSlug': 'kth-largest-element-in-an-array'},
    {   'description': '\n'
                       '<p>Given an unsorted integer array <code>nums</code>, '
                       'find the <strong>smallest missing positive '
                       'integer</strong>.</p>\n'
                       '\n'
                       '<p>You must implement an algorithm that runs in:</p>\n'
                       '<ul>\n'
                       '<li><code>O(n)</code> time</li>\n'
                       '<li><code>O(1)</code> extra space</li>\n'
                       '</ul>\n'
                       '\n'
                       '<p>This means you cannot use extra arrays, sets, or '
                       'sorting.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,2,0]\n'
                       '<strong>Output:</strong> 3\n'
                       '<strong>Explanation:</strong> The numbers 1 and 2 are '
                       'present, so the smallest missing positive is 3.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [3,4,-1,1]\n'
                       '<strong>Output:</strong> 2\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [7,8,9,11,12]\n'
                       '<strong>Output:</strong> 1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= '
                       '10<sup>5</sup></code></li>\n'
                       '<li><code>-2<sup>31</sup> <= nums[i] <= 2<sup>31</sup> '
                       '- 1</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'firstMissingPositive',
        'id': 'premium-33',
        'starter_code': {   'c': 'int firstMissingPositive(int* nums, int n) '
                                 '{\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int firstMissingPositive(vector<int>& '
                                   'nums) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int firstMissingPositive(int[] '
                                    'nums) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def firstMissingPositive(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'firstMissingPositive <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Hash Table', 'In-place Algorithm'],
        'test_cases': [   {'input': [[1, 2, 0]], 'output': 3},
                          {'input': [[3, 4, -1, 1]], 'output': 2},
                          {'input': [[7, 8, 9, 11, 12]], 'output': 1},
                          {'input': [[1]], 'output': 2},
                          {'input': [[2]], 'output': 1},
                          {'input': [[1, 1]], 'output': 2},
                          {'input': [[2, 2]], 'output': 1},
                          {'input': [[1, 2, 3]], 'output': 4},
                          {'input': [[0]], 'output': 1},
                          {'input': [[-1, -2]], 'output': 1},
                          {'input': [[4, 3, 2, 1]], 'output': 5},
                          {   'input': [[2, 3, 7, 6, 8, -1, -10, 15]],
                              'output': 1},
                          {'input': [[1, 1000]], 'output': 2},
                          {'input': [[3, 1]], 'output': 2},
                          {'input': [[5, 4, 1, 2]], 'output': 3}],
        'title': 'First Missing Positive',
        'titleSlug': 'first-missing-positive'},
    {   'description': '\n'
                       '<p>Given two integer arrays <code>nums1</code> and '
                       '<code>nums2</code>, return <em>an array of their '
                       'intersection</em>.</p>\n'
                       '\n'
                       '<p>Each element in the result must appear <strong>as '
                       'many times as it appears in both arrays</strong>, and '
                       'you may return the result in <strong>any '
                       'order</strong>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums1 = [1,2,2,1], nums2 = '
                       '[2,2]\n'
                       '<strong>Output:</strong> [2,2]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums1 = [4,9,5], nums2 = '
                       '[9,4,9,8,4]\n'
                       '<strong>Output:</strong> [4,9]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums1.length, nums2.length <= '
                       '1000</code></li>\n'
                       '<li><code>0 <= nums1[i], nums2[i] <= 1000</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'intersect',
        'id': 'premium-35',
        'starter_code': {   'c': 'void intersect(int* nums1, int n1, int* '
                                 'nums2, int n2) {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    vector<int> intersect(vector<int>& '
                                   'nums1, vector<int>& nums2) {\n'
                                   '        // Write your code here\n'
                                   '        return {};\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int[] intersect(int[] nums1, '
                                    'int[] nums2) {\n'
                                    '        // Write your code here\n'
                                    '        return new int[0];\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def intersect(nums1, nums2):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'intersect <- function(nums1, nums2) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Hash Table', 'Two Pointers'],
        'test_cases': [   {'input': [[1, 2, 2, 1], [2, 2]], 'output': [2, 2]},
                          {   'input': [[4, 9, 5], [9, 4, 9, 8, 4]],
                              'output': [4, 9]},
                          {'input': [[1, 1, 1], [1, 1]], 'output': [1, 1]},
                          {'input': [[1, 2, 3], [4, 5, 6]], 'output': []},
                          {'input': [[1], [1]], 'output': [1]},
                          {'input': [[1], [2]], 'output': []},
                          {'input': [[2, 2], [2, 2, 2]], 'output': [2, 2]},
                          {'input': [[0, 0], [0, 0, 0]], 'output': [0, 0]},
                          {'input': [[3, 3, 3], [3, 3]], 'output': [3, 3]},
                          {   'input': [[5, 6, 7], [7, 6, 5]],
                              'output': [5, 6, 7]},
                          {   'input': [[10, 20, 30], [30, 30, 20]],
                              'output': [20, 30]},
                          {'input': [[1, 2, 2, 3], [2, 2]], 'output': [2, 2]},
                          {'input': [[8, 9], [9, 8, 9]], 'output': [8, 9]},
                          {'input': [[4, 4, 4], [4, 4]], 'output': [4, 4]},
                          {'input': [[100, 200], [300]], 'output': []}],
        'title': 'Intersection of Two Arrays II',
        'titleSlug': 'intersection-of-two-arrays-ii'},
    {   'description': '\n'
                       '<p>Given an array of strings <code>strs</code>, group '
                       'the <strong>anagrams</strong> together.</p>\n'
                       '\n'
                       '<p>You can return the answer in <strong>any '
                       'order</strong>.</p>\n'
                       '\n'
                       '<p>Two strings are <strong>anagrams</strong> if they '
                       'contain the same characters in the same '
                       'frequency.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> strs = '
                       '["eat","tea","tan","ate","nat","bat"]\n'
                       '<strong>Output:</strong> '
                       '[["eat","tea","ate"],["tan","nat"],["bat"]]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> strs = [""]\n'
                       '<strong>Output:</strong> [[""]]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> strs = ["a"]\n'
                       '<strong>Output:</strong> [["a"]]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= strs.length <= '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>0 <= strs[i].length <= 100</code></li>\n'
                       '<li><code>strs[i]</code> consists of lowercase English '
                       'letters</li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'groupAnagrams',
        'id': 'premium-38',
        'starter_code': {   'c': 'void groupAnagrams() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    void groupAnagrams() {\n'
                                   '        // Write your code here\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void groupAnagrams() {\n'
                                    '        // Write your code here\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def groupAnagrams(strs):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'groupAnagrams <- function(strs) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Hash Table', 'Sorting'],
        'test_cases': [   {   'input': [   [   'eat',
                                               'tea',
                                               'tan',
                                               'ate',
                                               'nat',
                                               'bat']],
                              'output': [   ['eat', 'tea', 'ate'],
                                            ['tan', 'nat'],
                                            ['bat']]},
                          {'input': [['']], 'output': [['']]},
                          {'input': [['a']], 'output': [['a']]},
                          {   'input': [['abc', 'bca', 'cab', 'xyz', 'zyx']],
                              'output': [   ['abc', 'bca', 'cab'],
                                            ['xyz', 'zyx']]},
                          {   'input': [['rat', 'tar', 'art']],
                              'output': [['rat', 'tar', 'art']]},
                          {   'input': [['ab', 'ba', 'abc', 'cba']],
                              'output': [['ab', 'ba'], ['abc', 'cba']]},
                          {   'input': [['listen', 'silent', 'enlist']],
                              'output': [['listen', 'silent', 'enlist']]},
                          {   'input': [['a', 'b', 'c']],
                              'output': [['a'], ['b'], ['c']]},
                          {'input': [['aa', 'aa']], 'output': [['aa', 'aa']]},
                          {'input': [['abc']], 'output': [['abc']]},
                          {'input': [['', '']], 'output': [['', '']]},
                          {   'input': [['aaa', 'aaa', 'aaa']],
                              'output': [['aaa', 'aaa', 'aaa']]},
                          {   'input': [['ab', 'bc', 'cd']],
                              'output': [['ab'], ['bc'], ['cd']]},
                          {   'input': [['abc', 'def', 'ghi']],
                              'output': [['abc'], ['def'], ['ghi']]},
                          {   'input': [['abcd', 'dcba', 'lls', 'sll']],
                              'output': [['abcd', 'dcba'], ['lls', 'sll']]}],
        'title': 'Group Anagrams',
        'titleSlug': 'group-anagrams'},
    {   'description': '\n'
                       '<p>Given a string <code>s</code> and an integer '
                       '<code>k</code>, return <em>the length of the longest '
                       'substring that contains at most <code>k</code> '
                       'distinct characters</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "eceba", k = 2\n'
                       '<strong>Output:</strong> 3\n'
                       '<strong>Explanation:</strong> "ece" contains only 2 '
                       'distinct characters.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "aa", k = 1\n'
                       '<strong>Output:</strong> 2\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= s.length <= 10<sup>5</sup></code></li>\n'
                       '<li><code>0 <= k <= 52</code></li>\n'
                       '<li><code>s</code> consists of uppercase and lowercase '
                       'English letters</li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'lengthOfLongestSubstringKDistinct',
        'id': 'premium-39',
        'starter_code': {   'c': 'int lengthOfLongestSubstringKDistinct(char* '
                                 's, int k) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int '
                                   'lengthOfLongestSubstringKDistinct(string '
                                   's, int k) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int '
                                    'lengthOfLongestSubstringKDistinct(String '
                                    's, int k) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def '
                                      'lengthOfLongestSubstringKDistinct(s, '
                                      'k):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'lengthOfLongestSubstringKDistinct <- '
                                 'function(s, k) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Hash Table', 'Sliding Window'],
        'test_cases': [   {'input': ['eceba', 2], 'output': 3},
                          {'input': ['aa', 1], 'output': 2},
                          {'input': ['a', 1], 'output': 1},
                          {'input': ['a', 0], 'output': 0},
                          {'input': ['abc', 2], 'output': 2},
                          {'input': ['abc', 3], 'output': 3},
                          {'input': ['aaabbb', 1], 'output': 3},
                          {'input': ['aaabbb', 2], 'output': 6},
                          {'input': ['abaccc', 2], 'output': 4},
                          {'input': ['ababffzzeee', 2], 'output': 5},
                          {'input': ['abcd', 1], 'output': 1},
                          {'input': ['abcadcacacaca', 3], 'output': 11},
                          {'input': ['zzzz', 1], 'output': 4},
                          {'input': ['AaBbCc', 3], 'output': 3},
                          {'input': ['aabbcc', 2], 'output': 4}],
        'title': 'Longest Substring with At Most K Distinct Characters',
        'titleSlug': 'longest-substring-with-at-most-k-distinct-characters'},
    {   'description': '\n'
                       '<p>Given a string <code>s</code> containing just the '
                       "characters <code>'('</code>, <code>')'</code>, "
                       "<code>'{'</code>, <code>'}'</code>, <code>'['</code> "
                       "and <code>']'</code>, determine if the input string is "
                       'valid.</p>\n'
                       '\n'
                       '<p>An input string is valid if:</p>\n'
                       '<ol>\n'
                       '<li>Open brackets must be closed by the same type of '
                       'brackets.</li>\n'
                       '<li>Open brackets must be closed in the correct '
                       'order.</li>\n'
                       '<li>Every close bracket has a corresponding open '
                       'bracket of the same type.</li>\n'
                       '</ol>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "()"\n'
                       '<strong>Output:</strong> true\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "()[]{}"\n'
                       '<strong>Output:</strong> true\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "(]"\n'
                       '<strong>Output:</strong> false\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= s.length <= 10<sup>4</sup></code></li>\n'
                       '<li><code>s</code> consists of parentheses only '
                       "<code>'()[]{}'</code>.</li>\n"
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'isValid',
        'id': 'premium-4',
        'starter_code': {   'c': 'int isValid(char* s) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    bool isValid(string s) {\n'
                                   '        // Write your code here\n'
                                   '        return false;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public boolean isValid(String s) {\n'
                                    '        // Write your code here\n'
                                    '        return false;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def isValid(s):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'isValid <- function(s) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Stack'],
        'test_cases': [   {'input': ['()'], 'output': True},
                          {'input': ['()[]{}'], 'output': True},
                          {'input': ['{[]}'], 'output': True},
                          {'input': ['((()))'], 'output': True},
                          {'input': ['(]'], 'output': False},
                          {'input': ['([)]'], 'output': False},
                          {'input': ['{[}]'], 'output': False},
                          {'input': [''], 'output': True},
                          {'input': ['('], 'output': False},
                          {'input': [')'], 'output': False},
                          {'input': ['(([]){})'], 'output': True},
                          {'input': ['{[()()]}'], 'output': True},
                          {'input': ['(((('], 'output': False},
                          {'input': ['))))'], 'output': False},
                          {'input': ['{[(])}'], 'output': False}],
        'title': 'Valid Parentheses',
        'titleSlug': 'valid-parentheses'},
    {   'description': '\n'
                       '<p>Given an array of positive integers '
                       '<code>nums</code> and an integer <code>k</code>, '
                       'return <em>the number of contiguous subarrays where '
                       'the product of all the elements is strictly less than '
                       '<code>k</code></em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [10,5,2,6], k = 100\n'
                       '<strong>Output:</strong> 8\n'
                       '<strong>Explanation:</strong>\n'
                       'The 8 subarrays are:\n'
                       '[10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,2,3], k = 0\n'
                       '<strong>Output:</strong> 0\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= 3 × '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>1 <= nums[i] <= 1000</code></li>\n'
                       '<li><code>0 <= k <= 10<sup>6</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'numSubarrayProductLessThanK',
        'id': 'premium-40',
        'starter_code': {   'c': 'int numSubarrayProductLessThanK(int* nums, '
                                 'int n, int k) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int '
                                   'numSubarrayProductLessThanK(vector<int>& '
                                   'nums, int k) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int '
                                    'numSubarrayProductLessThanK(int[] nums, '
                                    'int k) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def numSubarrayProductLessThanK(nums, '
                                      'k):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'numSubarrayProductLessThanK <- '
                                 'function(nums, k) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Sliding Window'],
        'test_cases': [   {'input': [[10, 5, 2, 6], 100], 'output': 8},
                          {'input': [[1, 2, 3], 0], 'output': 0},
                          {'input': [[1, 1, 1], 2], 'output': 6},
                          {'input': [[1, 2, 3], 7], 'output': 4},
                          {'input': [[3, 4, 7], 50], 'output': 5},
                          {'input': [[1], 2], 'output': 1},
                          {'input': [[1], 1], 'output': 0},
                          {'input': [[10], 11], 'output': 1},
                          {'input': [[10], 10], 'output': 0},
                          {'input': [[2, 5, 3, 10], 30], 'output': 6},
                          {'input': [[5, 2, 6], 50], 'output': 6},
                          {'input': [[1, 2, 3, 4], 10], 'output': 7},
                          {'input': [[4, 3, 2, 1], 5], 'output': 4},
                          {'input': [[1, 1, 1, 1], 1], 'output': 0},
                          {'input': [[2, 2, 2], 10], 'output': 6}],
        'title': 'Subarray Product Less Than K',
        'titleSlug': 'subarray-product-less-than-k'},
    {   'description': '\n'
                       '<p>You are given an <code>m x n</code> grid '
                       'where:</p>\n'
                       '<ul>\n'
                       '<li><code>0</code> represents an empty cell</li>\n'
                       '<li><code>1</code> represents a fresh orange</li>\n'
                       '<li><code>2</code> represents a rotten orange</li>\n'
                       '</ul>\n'
                       '\n'
                       '<p>Every minute, any fresh orange that is '
                       '<strong>4-directionally adjacent</strong> to a rotten '
                       'orange becomes rotten.</p>\n'
                       '\n'
                       '<p>Return <em>the minimum number of minutes that must '
                       'elapse until no cell has a fresh orange</em>.</p>\n'
                       '\n'
                       '<p>If this is impossible, return <code>-1</code>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong>\n'
                       'grid = [[2,1,1],\n'
                       '        [1,1,0],\n'
                       '        [0,1,1]]\n'
                       '<strong>Output:</strong> 4\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong>\n'
                       'grid = [[2,1,1],\n'
                       '        [0,1,1],\n'
                       '        [1,0,1]]\n'
                       '<strong>Output:</strong> -1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> grid = [[0,2]]\n'
                       '<strong>Output:</strong> 0\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>m == grid.length</code></li>\n'
                       '<li><code>n == grid[i].length</code></li>\n'
                       '<li><code>1 <= m, n <= 10</code></li>\n'
                       '<li><code>grid[i][j]</code> is <code>0</code>, '
                       '<code>1</code>, or <code>2</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'orangesRotting',
        'id': 'premium-41',
        'starter_code': {   'c': 'int orangesRotting(int grid[][100], int m, '
                                 'int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int '
                                   'orangesRotting(vector<vector<int>>& grid) '
                                   '{\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int orangesRotting(int[][] '
                                    'grid) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def orangesRotting(grid):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'orangesRotting <- function(grid, m, n) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Matrix', 'BFS'],
        'test_cases': [   {   'input': [[[2, 1, 1], [1, 1, 0], [0, 1, 1]]],
                              'output': 4},
                          {   'input': [[[2, 1, 1], [0, 1, 1], [1, 0, 1]]],
                              'output': -1},
                          {'input': [[[0, 2]]], 'output': 0},
                          {'input': [[[1]]], 'output': -1},
                          {'input': [[[2]]], 'output': 0},
                          {'input': [[[1, 2]]], 'output': 1},
                          {'input': [[[2, 1]]], 'output': 1},
                          {   'input': [[[1, 1, 1], [1, 2, 1], [1, 1, 1]]],
                              'output': 2},
                          {'input': [[[2, 2, 2], [2, 2, 2]]], 'output': 0},
                          {'input': [[[1, 0, 1]]], 'output': -1},
                          {'input': [[[2, 1, 0, 1]]], 'output': -1},
                          {'input': [[[0, 0, 0]]], 'output': 0},
                          {'input': [[[1, 1], [1, 1]]], 'output': -1},
                          {'input': [[[2, 1], [1, 1]]], 'output': 2},
                          {'input': [[[2, 0], [0, 1]]], 'output': -1}],
        'title': 'Rotting Oranges',
        'titleSlug': 'rotting-oranges'},
    {   'description': '\n'
                       '<p>Koko loves to eat bananas. There are <code>n</code> '
                       'piles of bananas, where <code>piles[i]</code> is the '
                       'number of bananas in the <code>i<sup>th</sup></code> '
                       'pile.</p>\n'
                       '\n'
                       '<p>Koko can decide her eating speed <code>k</code> '
                       '(bananas per hour). Each hour, she chooses one pile '
                       'and eats up to <code>k</code> bananas from it. If the '
                       'pile has fewer than <code>k</code> bananas, she eats '
                       'the entire pile.</p>\n'
                       '\n'
                       '<p>Given an integer <code>h</code> (total hours '
                       'available), return <em>the minimum integer eating '
                       'speed <code>k</code> such that Koko can eat all the '
                       'bananas within <code>h</code> hours</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> piles = [3,6,7,11], h = 8\n'
                       '<strong>Output:</strong> 4\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> piles = [30,11,23,4,20], h = '
                       '5\n'
                       '<strong>Output:</strong> 30\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> piles = [30,11,23,4,20], h = '
                       '6\n'
                       '<strong>Output:</strong> 23\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= piles.length <= '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>1 <= piles[i] <= 10<sup>9</sup></code></li>\n'
                       '<li><code>piles.length <= h <= '
                       '10<sup>9</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'minEatingSpeed',
        'id': 'premium-43',
        'starter_code': {   'c': 'int minEatingSpeed(int* piles, int n, int h) '
                                 '{\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int minEatingSpeed(vector<int>& piles, '
                                   'int h) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int minEatingSpeed(int[] '
                                    'piles, int h) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def minEatingSpeed(piles, h):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'minEatingSpeed <- function(piles, h) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Binary Search', 'Array'],
        'test_cases': [   {'input': [[3, 6, 7, 11], 8], 'output': 4},
                          {'input': [[30, 11, 23, 4, 20], 5], 'output': 30},
                          {'input': [[30, 11, 23, 4, 20], 6], 'output': 23},
                          {'input': [[1], 1], 'output': 1},
                          {'input': [[1], 2], 'output': 1},
                          {'input': [[10], 1], 'output': 10},
                          {'input': [[10], 10], 'output': 1},
                          {'input': [[5, 5, 5, 5], 4], 'output': 5},
                          {'input': [[5, 5, 5, 5], 8], 'output': 3},
                          {'input': [[1000000000], 2], 'output': 500000000},
                          {'input': [[2, 2, 2], 3], 'output': 2},
                          {'input': [[2, 2, 2], 6], 'output': 1},
                          {'input': [[7, 15, 6, 3], 10], 'output': 3},
                          {'input': [[9, 8, 7], 3], 'output': 9},
                          {'input': [[9, 8, 7], 10], 'output': 3}],
        'title': 'Koko Eating Bananas',
        'titleSlug': 'koko-eating-bananas'},
    {   'description': '\n'
                       '<p>You are given a list of <code>tasks</code>, where '
                       'each task is represented by a capital letter from '
                       '<code>A</code> to <code>Z</code>.</p>\n'
                       '\n'
                       '<p>Each task takes <strong>1 unit of time</strong> to '
                       'execute, and there is a <strong>cooldown period '
                       '<code>n</code></strong> between two same tasks.</p>\n'
                       '\n'
                       '<p>Return <em>the minimum number of time units '
                       'required to finish all tasks</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> tasks = '
                       '["A","A","A","B","B","B"], n = 2\n'
                       '<strong>Output:</strong> 8\n'
                       '<strong>Explanation:</strong>\n'
                       'A → B → idle → A → B → idle → A → B\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> tasks = '
                       '["A","A","A","B","B","B"], n = 0\n'
                       '<strong>Output:</strong> 6\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> tasks = '
                       '["A","A","A","B","B","C"], n = 2\n'
                       '<strong>Output:</strong> 7\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= tasks.length <= '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>tasks[i]</code> is an uppercase English '
                       'letter</li>\n'
                       '<li><code>0 <= n <= 100</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'leastInterval',
        'id': 'premium-44',
        'starter_code': {   'c': 'int leastInterval(char* tasks, int n, int '
                                 'cooldown) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int leastInterval(vector<char>& tasks, '
                                   'int cooldown) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int leastInterval(char[] '
                                    'tasks, int cooldown) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def leastInterval(tasks, cooldown):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'leastInterval <- function(tasks, cooldown) '
                                 '{\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Hash Table', 'Greedy', 'Heap'],
        'test_cases': [   {   'input': [['A', 'A', 'A', 'B', 'B', 'B'], 2],
                              'output': 8},
                          {   'input': [['A', 'A', 'A', 'B', 'B', 'B'], 0],
                              'output': 6},
                          {   'input': [['A', 'A', 'A', 'B', 'B', 'C'], 2],
                              'output': 7},
                          {'input': [['A', 'A', 'A', 'A'], 3], 'output': 13},
                          {'input': [['A', 'B', 'C', 'D'], 2], 'output': 4},
                          {'input': [['A', 'A', 'B', 'B'], 2], 'output': 5},
                          {   'input': [['A', 'A', 'A', 'B', 'C', 'D'], 2],
                              'output': 7},
                          {'input': [['A'], 5], 'output': 1},
                          {'input': [['A', 'A', 'A'], 1], 'output': 5},
                          {'input': [['A', 'B', 'A'], 2], 'output': 4},
                          {   'input': [['A', 'A', 'B', 'B', 'C', 'C'], 2],
                              'output': 6},
                          {   'input': [   [   'A',
                                               'A',
                                               'A',
                                               'B',
                                               'B',
                                               'B',
                                               'C',
                                               'C'],
                                           2],
                              'output': 8},
                          {'input': [['A', 'B', 'A', 'B'], 3], 'output': 6},
                          {   'input': [   [   'A',
                                               'A',
                                               'A',
                                               'A',
                                               'B',
                                               'B',
                                               'C',
                                               'C'],
                                           1],
                              'output': 8},
                          {   'input': [   [   'A',
                                               'A',
                                               'A',
                                               'B',
                                               'B',
                                               'B',
                                               'C',
                                               'C',
                                               'D',
                                               'D'],
                                           2],
                              'output': 10}],
        'title': 'Task Scheduler',
        'titleSlug': 'task-scheduler'},
    {   'description': '\n'
                       '<p>Given two strings <code>s</code> and '
                       '<code>p</code>, return <em>a list of all start indices '
                       "of <code>p</code>'s anagrams in "
                       '<code>s</code></em>.</p>\n'
                       '\n'
                       '<p>An <strong>anagram</strong> is formed by '
                       'rearranging the letters of <code>p</code>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "cbaebabacd", p = "abc"\n'
                       '<strong>Output:</strong> [0,6]\n'
                       '<strong>Explanation:</strong>\n'
                       'The substrings "cba" (index 0) and "bac" (index 6) are '
                       'anagrams of "abc".\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "abab", p = "ab"\n'
                       '<strong>Output:</strong> [0,1,2]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= s.length, p.length <= 3 × '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>s</code> and <code>p</code> consist of '
                       'lowercase English letters</li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'findAnagrams',
        'id': 'premium-45',
        'starter_code': {   'c': 'void findAnagrams(char* s, char* p) {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    vector<int> findAnagrams(string s, '
                                   'string p) {\n'
                                   '        // Write your code here\n'
                                   '        return {};\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void findAnagrams() {\n'
                                    '        // Write your code here\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def findAnagrams(s, p):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'findAnagrams <- function(s, p) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Sliding Window', 'Hash Table'],
        'test_cases': [   {'input': ['cbaebabacd', 'abc'], 'output': [0, 6]},
                          {'input': ['abab', 'ab'], 'output': [0, 1, 2]},
                          {'input': ['aaaaa', 'aa'], 'output': [0, 1, 2, 3]},
                          {'input': ['abc', 'abcd'], 'output': []},
                          {'input': ['baa', 'aa'], 'output': [1]},
                          {   'input': ['abababab', 'ab'],
                              'output': [0, 1, 2, 3, 4, 5, 6]},
                          {'input': ['af', 'be'], 'output': []},
                          {'input': ['acdcaeccde', 'cde'], 'output': [6]},
                          {   'input': ['aaaaaaaaaa', 'aaa'],
                              'output': [0, 1, 2, 3, 4, 5, 6, 7]},
                          {'input': ['abcabc', 'bca'], 'output': [0, 1, 2, 3]},
                          {'input': ['abc', 'a'], 'output': [0]},
                          {'input': ['aaa', 'a'], 'output': [0, 1, 2]},
                          {'input': ['abcdefg', 'hij'], 'output': []},
                          {'input': ['abab', 'ba'], 'output': [0, 1, 2]},
                          {'input': ['babc', 'abc'], 'output': [1]}],
        'title': 'Find All Anagrams in a String',
        'titleSlug': 'find-all-anagrams-in-a-string'},
    {   'description': '\n'
                       '<p>Given an array of integers <code>nums</code> and an '
                       'integer <code>k</code>, return <em>the total number of '
                       'subarrays whose sum equals to '
                       '<code>k</code></em>.</p>\n'
                       '\n'
                       '<p>A subarray is a contiguous '
                       '<strong>non-empty</strong> sequence of elements within '
                       'an array.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,1,1], k = 2\n'
                       '<strong>Output:</strong> 2\n'
                       '<strong>Explanation:</strong> The subarrays [1,1] '
                       '(index 0-1) and [1,1] (index 1-2) both sum to 2.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,2,3], k = 3\n'
                       '<strong>Output:</strong> 2\n'
                       '<strong>Explanation:</strong> The subarrays [1,2] and '
                       '[3] both sum to 3.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= 2 * '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>-1000 <= nums[i] <= 1000</code></li>\n'
                       '<li><code>-10<sup>7</sup> <= k <= '
                       '10<sup>7</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'subarraySum',
        'id': 'premium-6',
        'starter_code': {   'c': 'int subarraySum(int* nums, int n, int k) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int subarraySum(vector<int>& nums, int '
                                   'k) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int subarraySum(int[] nums, '
                                    'int k) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def subarraySum(nums, k):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'subarraySum <- function(nums, k) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Hash Table', 'Prefix Sum'],
        'test_cases': [   {'input': [[1, 1, 1], 2], 'output': 2},
                          {'input': [[1, 2, 3], 3], 'output': 2},
                          {'input': [[1, 2, 3], 7], 'output': 0},
                          {'input': [[1], 1], 'output': 1},
                          {'input': [[1], 0], 'output': 0},
                          {'input': [[1, -1, 0], 0], 'output': 3},
                          {'input': [[-1, -1, 1], 0], 'output': 1},
                          {'input': [[0, 0, 0], 0], 'output': 6},
                          {'input': [[1, 2, 1, 2, 1], 3], 'output': 4},
                          {'input': [[1, 2, 3], 6], 'output': 1},
                          {'input': [[1, 1, 1, 1], 2], 'output': 3},
                          {   'input': [[3, 4, 7, 2, -3, 1, 4, 2], 7],
                              'output': 4},
                          {'input': [[10], 10], 'output': 1},
                          {'input': [[0, 1, 0, 1, 0], 1], 'output': 5},
                          {'input': [[1, 2, 3, 4, 5], 9], 'output': 2}],
        'title': 'Subarray Sum Equals K',
        'titleSlug': 'subarray-sum-equals-k'},
    {   'description': '\n'
                       '<p>Given a string <code>s</code> and a dictionary of '
                       'strings <code>wordDict</code>, add spaces in '
                       '<code>s</code> to construct all possible sentences '
                       'where each word is a valid dictionary word.</p>\n'
                       '\n'
                       '<p>Return <em>all such possible sentences in '
                       '<strong>any order</strong></em>.</p>\n'
                       '\n'
                       '<p><strong>Note:</strong></p>\n'
                       '<ul>\n'
                       '<li>You may reuse words in the dictionary multiple '
                       'times</li>\n'
                       '<li>The same word may appear multiple times in a '
                       'sentence</li>\n'
                       '</ul>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "catsanddog"\n'
                       'wordDict = ["cat","cats","and","sand","dog"]\n'
                       '\n'
                       '<strong>Output:</strong> ["cats and dog","cat sand '
                       'dog"]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "pineapplepenapple"\n'
                       'wordDict = '
                       '["apple","pen","applepen","pine","pineapple"]\n'
                       '\n'
                       '<strong>Output:</strong>\n'
                       '["pine apple pen apple",\n'
                       ' "pineapple pen apple",\n'
                       ' "pine applepen apple"]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "catsandog"\n'
                       'wordDict = ["cats","dog","sand","and","cat"]\n'
                       '\n'
                       '<strong>Output:</strong> []\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= s.length <= 20</code></li>\n'
                       '<li><code>1 <= wordDict.length <= 1000</code></li>\n'
                       '<li><code>1 <= wordDict[i].length <= 10</code></li>\n'
                       '<li><code>s</code> and <code>wordDict[i]</code> '
                       'consist of lowercase English letters</li>\n'
                       '<li>All strings in <code>wordDict</code> are '
                       '<strong>unique</strong></li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'wordBreak',
        'id': 'premium-46',
        'starter_code': {   'c': 'void wordBreak() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    vector<string> wordBreak(string s, '
                                   'vector<string>& wordDict) {\n'
                                   '        // Write your code here\n'
                                   '        return {};\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void wordBreak() {\n'
                                    '        // Write your code here\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def wordBreak(s, wordDict):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'wordBreak <- function(s, dict) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Dynamic Programming', 'Backtracking'],
        'test_cases': [   {   'input': [   'catsanddog',
                                           [   'cat',
                                               'cats',
                                               'and',
                                               'sand',
                                               'dog']],
                              'output': ['cats and dog', 'cat sand dog']},
                          {   'input': [   'pineapplepenapple',
                                           [   'apple',
                                               'pen',
                                               'applepen',
                                               'pine',
                                               'pineapple']],
                              'output': [   'pine apple pen apple',
                                            'pineapple pen apple',
                                            'pine applepen apple']},
                          {   'input': [   'catsandog',
                                           [   'cats',
                                               'dog',
                                               'sand',
                                               'and',
                                               'cat']],
                              'output': []},
                          {'input': ['a', ['a']], 'output': ['a']},
                          {   'input': ['aaaaaaa', ['a', 'aa', 'aaa']],
                              'output': [   'a a a a a a a',
                                            'aa a a a a a',
                                            'a aa a a a a',
                                            'a a aa a a a',
                                            'aa aa a a a',
                                            'a a a aa a a',
                                            'aa a aa a a',
                                            'a aa aa a a',
                                            'a a a a aa a',
                                            'aa a a aa a',
                                            'a aa a aa a',
                                            'a a aa aa a',
                                            'aa aa aa a',
                                            'a a a a a aa',
                                            'aa a a a aa',
                                            'a aa a a aa',
                                            'a a aa a aa',
                                            'aa aa a aa',
                                            'a a a aa aa',
                                            'aa a aa aa',
                                            'a aa aa aa']},
                          {   'input': ['leetcode', ['leet', 'code']],
                              'output': ['leet code']},
                          {   'input': ['aaaa', ['a', 'aa']],
                              'output': [   'a a a a',
                                            'aa a a',
                                            'a aa a',
                                            'a a aa',
                                            'aa aa']},
                          {   'input': ['abcd', ['a', 'abc', 'b', 'cd']],
                              'output': ['a b cd']},
                          {   'input': ['cars', ['car', 'ca', 'rs']],
                              'output': ['ca rs']},
                          {   'input': [   'banana',
                                           ['ban', 'ana', 'b', 'a', 'n', 'na']],
                              'output': [   'b a n a n a',
                                            'ban a n a',
                                            'b a na n a',
                                            'b a n ana',
                                            'ban ana']},
                          {   'input': [   'penpineappleapplepen',
                                           [   'apple',
                                               'pen',
                                               'applepen',
                                               'pine',
                                               'pineapple']],
                              'output': [   'pen pine apple apple pen',
                                            'pen pineapple apple pen']},
                          {   'input': ['aaaaab', ['a', 'aa', 'aaa']],
                              'output': []},
                          {   'input': ['dogcat', ['dog', 'cat']],
                              'output': ['dog cat']},
                          {   'input': ['abab', ['a', 'ab', 'b']],
                              'output': [   'a b a b',
                                            'ab a b',
                                            'a b ab',
                                            'ab ab']},
                          {   'input': ['xyz', ['x', 'y', 'z']],
                              'output': ['x y z']}],
        'title': 'Word Break II',
        'titleSlug': 'word-break-ii'},
    {   'description': '\n'
                       '<p>Write a function to find the longest common prefix '
                       'string amongst an array of strings.</p>\n'
                       '\n'
                       '<p>If there is no common prefix, return an empty '
                       'string <code>""</code>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> strs = '
                       '["flower","flow","flight"]\n'
                       '<strong>Output:</strong> "fl"\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> strs = '
                       '["dog","racecar","car"]\n'
                       '<strong>Output:</strong> ""\n'
                       '<strong>Explanation:</strong> There is no common '
                       'prefix among the input strings.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= strs.length <= 200</code></li>\n'
                       '<li><code>0 <= strs[i].length <= 200</code></li>\n'
                       '<li><code>strs[i]</code> consists of only lowercase '
                       'English letters.</li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'longestCommonPrefix',
        'id': 'premium-10',
        'starter_code': {   'c': 'void longestCommonPrefix() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    string '
                                   'longestCommonPrefix(vector<string>& strs) '
                                   '{\n'
                                   '        // Write your code here\n'
                                   '        return "";\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public String '
                                    'longestCommonPrefix(String[] strs) {\n'
                                    '        // Write your code here\n'
                                    '        return "";\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def longestCommonPrefix(strs):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'longestCommonPrefix <- function(strs) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Trie'],
        'test_cases': [   {   'input': [['flower', 'flow', 'flight']],
                              'output': 'fl'},
                          {'input': [['dog', 'racecar', 'car']], 'output': ''},
                          {   'input': [['test', 'test', 'test']],
                              'output': 'test'},
                          {'input': [['alone']], 'output': 'alone'},
                          {'input': [[]], 'output': ''},
                          {'input': [['', 'a']], 'output': ''},
                          {'input': [['a', '']], 'output': ''},
                          {'input': [['abc', 'def', 'ghi']], 'output': ''},
                          {'input': [['a', 'abc', 'abcde']], 'output': 'a'},
                          {   'input': [['test', 'testing', 'tester']],
                              'output': 'test'},
                          {'input': [['a', 'ab', 'abc']], 'output': 'a'},
                          {'input': [['hello', 'hell']], 'output': 'hell'},
                          {'input': [['prefix', 'pre']], 'output': 'pre'},
                          {'input': [['Test', 'test']], 'output': ''},
                          {'input': [['test123', 'test456']], 'output': 'test'},
                          {'input': [['123abc', '123def']], 'output': '123'}],
        'title': 'Longest Common Prefix',
        'titleSlug': 'longest-common-prefix'},
    {   'description': '\n'
                       '<p>Given an array of integers <code>nums</code> which '
                       'is sorted in ascending order, and an integer '
                       '<code>target</code>, write a function to search '
                       '<code>target</code> in <code>nums</code>. If '
                       '<code>target</code> exists, return its index. '
                       'Otherwise, return <code>-1</code>.</p>\n'
                       '\n'
                       '<p>You must write an algorithm with <code>O(log '
                       'n)</code> runtime complexity.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [-1,0,3,5,9,12], target '
                       '= 9\n'
                       '<strong>Output:</strong> 4\n'
                       '<strong>Explanation:</strong> 9 exists in nums and its '
                       'index is 4\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [-1,0,3,5,9,12], target '
                       '= 2\n'
                       '<strong>Output:</strong> -1\n'
                       '<strong>Explanation:</strong> 2 does not exist in nums '
                       'so return -1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= '
                       '10<sup>4</sup></code></li>\n'
                       '<li>All the integers in <code>nums</code> are '
                       '<strong>unique</strong>.</li>\n'
                       '<li><code>nums</code> is sorted in ascending '
                       'order.</li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'binarySearch',
        'id': 'premium-11',
        'starter_code': {   'c': 'int binarySearch(int* nums, int n, int '
                                 'target) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int binarySearch(vector<int>& nums, '
                                   'int target) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int binarySearch(int[] nums, '
                                    'int target) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def binarySearch(nums, target):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'binarySearch <- function(nums, target) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Binary Search'],
        'test_cases': [   {'input': [[-1, 0, 3, 5, 9, 12], 9], 'output': 4},
                          {'input': [[-1, 0, 3, 5, 9, 12], 2], 'output': -1},
                          {'input': [[5], 5], 'output': 0},
                          {'input': [[5], -5], 'output': -1},
                          {'input': [[1, 2, 3, 4, 5], 1], 'output': 0},
                          {'input': [[1, 2, 3, 4, 5], 5], 'output': 4},
                          {'input': [[1, 2, 3, 4, 5], 3], 'output': 2},
                          {'input': [[1, 2], 1], 'output': 0},
                          {'input': [[1, 2], 2], 'output': 1},
                          {   'input': [[1, 3, 5, 7, 9, 11, 13, 15], 7],
                              'output': 3},
                          {'input': [[2, 4, 6, 8, 10, 12], 6], 'output': 2},
                          {'input': [[-10, -5, 0, 5, 10], -5], 'output': 1},
                          {'input': [[-10, -5, 0, 5, 10], 10], 'output': 4},
                          {   'input': [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 11],
                              'output': -1},
                          {   'input': [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0],
                              'output': -1}],
        'title': 'Binary Search',
        'titleSlug': 'binary-search'},
    {   'description': '\n'
                       '<p>Given an array of integers <code>nums</code> and an '
                       'integer <code>target</code>, return <em>indices of the '
                       'two numbers such that they add up to '
                       '<code>target</code></em>.</p>\n'
                       '\n'
                       '<p>You may assume that each input would have '
                       '<strong>exactly one solution</strong>, and you may not '
                       'use the same element twice.</p>\n'
                       '\n'
                       '<p>You can return the answer in any order.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [2,7,11,15], target = '
                       '9\n'
                       '<strong>Output:</strong> [0,1]\n'
                       '<strong>Explanation:</strong> Because nums[0] + '
                       'nums[1] == 9, we return [0, 1].\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [3,2,4], target = 6\n'
                       '<strong>Output:</strong> [1,2]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [3,3], target = 6\n'
                       '<strong>Output:</strong> [0,1]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>2 <= nums.length <= '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>-10<sup>9</sup> <= nums[i] <= '
                       '10<sup>9</sup></code></li>\n'
                       '<li><code>-10<sup>9</sup> <= target <= '
                       '10<sup>9</sup></code></li>\n'
                       '<li><strong>Only one valid answer '
                       'exists.</strong></li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'twoSum',
        'id': 'premium-1',
        'starter_code': {   'c': 'int* twoSum(int* nums, int n, int target, '
                                 'int* returnSize) {\n'
                                 '    // Write your code here\n'
                                 '    return NULL;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    vector<int> twoSum(vector<int>& nums, '
                                   'int target) {\n'
                                   '        // Write your code here\n'
                                   '        return {};\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int[] twoSum(int[] nums, int '
                                    'target) {\n'
                                    '        // Write your code here\n'
                                    '        return new int[0];\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def twoSum(nums, target):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'twoSum <- function(nums, target) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Hash Table'],
        'test_cases': [   {'input': [[2, 7, 11, 15], 9], 'output': [0, 1]},
                          {'input': [[3, 2, 4], 6], 'output': [1, 2]},
                          {'input': [[3, 3], 6], 'output': [0, 1]},
                          {'input': [[1, 2], 3], 'output': [0, 1]},
                          {'input': [[0, 0], 0], 'output': [0, 1]},
                          {   'input': [[-1, -2, -3, -4, -5], -8],
                              'output': [2, 4]},
                          {'input': [[1, -1, 0], 0], 'output': [0, 1]},
                          {'input': [[-10, -5, 3, 8], -7], 'output': [0, 2]},
                          {   'input': [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19],
                              'output': [8, 9]},
                          {   'input': [[10, 20, 30, 40, 50, 60, 70], 130],
                              'output': [5, 6]},
                          {'input': [[5, 1, 2, 3, 4], 6], 'output': [0, 1]},
                          {'input': [[1, 2, 3, 4, 5], 9], 'output': [3, 4]},
                          {'input': [[5, 5, 5, 5], 10], 'output': [0, 1]},
                          {   'input': [[1000000, 2000000, 3000000], 5000000],
                              'output': [1, 2]},
                          {'input': [[-5, 10, -3, 8, 2], 5], 'output': [0, 1]}],
        'title': 'Two Sum',
        'titleSlug': 'two-sum'},
    {   'description': '\n'
                       '<p>You are climbing a staircase. It takes '
                       '<code>n</code> steps to reach the top.</p>\n'
                       '\n'
                       '<p>Each time you can either climb <code>1</code> or '
                       '<code>2</code> steps. In how many distinct ways can '
                       'you climb to the top?</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> n = 2\n'
                       '<strong>Output:</strong> 2\n'
                       '<strong>Explanation:</strong> There are two ways to '
                       'climb to the top.\n'
                       '1. 1 step + 1 step\n'
                       '2. 2 steps\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> n = 3\n'
                       '<strong>Output:</strong> 3\n'
                       '<strong>Explanation:</strong> There are three ways to '
                       'climb to the top.\n'
                       '1. 1 step + 1 step + 1 step\n'
                       '2. 1 step + 2 steps\n'
                       '3. 2 steps + 1 step\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= n <= 45</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'climbStairs',
        'id': 'premium-12',
        'starter_code': {   'c': 'int climbStairs(int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int climbStairs(int n) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int climbStairs(int n) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def climbStairs(n):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'climbStairs <- function(n) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Math', 'Dynamic Programming', 'Memoization'],
        'test_cases': [   {'input': [2], 'output': 2},
                          {'input': [3], 'output': 3},
                          {'input': [4], 'output': 5},
                          {'input': [1], 'output': 1},
                          {'input': [0], 'output': 1},
                          {'input': [5], 'output': 8},
                          {'input': [6], 'output': 13},
                          {'input': [7], 'output': 21},
                          {'input': [8], 'output': 34},
                          {'input': [10], 'output': 89},
                          {'input': [15], 'output': 987},
                          {'input': [20], 'output': 10946},
                          {'input': [9], 'output': 55},
                          {'input': [11], 'output': 144},
                          {'input': [12], 'output': 233}],
        'title': 'Climbing Stairs',
        'titleSlug': 'climbing-stairs'},
    {   'description': '\n'
                       '<p>A <strong>peak element</strong> is an element that '
                       'is strictly greater than its neighbors.</p>\n'
                       '\n'
                       '<p>Given an integer array <code>nums</code>, find a '
                       'peak element and return its index. If the array '
                       'contains multiple peaks, return the index of '
                       '<strong>any one of them</strong>.</p>\n'
                       '\n'
                       '<p>You may assume that:</p>\n'
                       '<ul>\n'
                       '<li><code>nums[-1] = -∞</code></li>\n'
                       '<li><code>nums[n] = -∞</code></li>\n'
                       '</ul>\n'
                       '\n'
                       '<p>This means elements outside the array are always '
                       'smaller.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,2,3,1]\n'
                       '<strong>Output:</strong> 2\n'
                       '<strong>Explanation:</strong> 3 is greater than both 2 '
                       'and 1, so it is a peak.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,2,1,3,5,6,4]\n'
                       '<strong>Output:</strong> 5\n'
                       '<strong>Explanation:</strong> 6 is a peak element.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>-2<sup>31</sup> <= nums[i] <= 2<sup>31</sup> '
                       '- 1</code></li>\n'
                       '<li><code>nums[i] != nums[i + 1]</code> for all valid '
                       'i</li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'findPeakElement',
        'id': 'premium-21',
        'starter_code': {   'c': 'int findPeakElement(int* nums, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int findPeakElement(vector<int>& nums) '
                                   '{\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int findPeakElement(int[] '
                                    'nums) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def findPeakElement(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'findPeakElement <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Binary Search'],
        'test_cases': [   {'input': [[1, 2, 3, 1]], 'output': 2},
                          {'input': [[1, 2, 1, 3, 5, 6, 4]], 'output': 5},
                          {'input': [[1]], 'output': 0},
                          {'input': [[1, 2]], 'output': 1},
                          {'input': [[2, 1]], 'output': 0},
                          {'input': [[1, 3, 2]], 'output': 1},
                          {'input': [[1, 2, 3, 4, 5]], 'output': 4},
                          {'input': [[5, 4, 3, 2, 1]], 'output': 0},
                          {'input': [[2, 1, 2]], 'output': 0},
                          {'input': [[1, 2, 3, 2, 1]], 'output': 2},
                          {'input': [[10, 20, 15]], 'output': 1},
                          {'input': [[-1, -2, -3]], 'output': 0},
                          {'input': [[3, 4, 3, 2, 1]], 'output': 1},
                          {'input': [[1, 3, 5, 7, 6, 4, 2]], 'output': 3},
                          {'input': [[100]], 'output': 0}],
        'title': 'Find Peak Element',
        'titleSlug': 'find-peak-element'},
    {   'description': '\n'
                       '<p>Design an algorithm to <strong>serialize and '
                       'deserialize</strong> a binary tree.</p>\n'
                       '\n'
                       '<p><strong>Serialization</strong> is the process of '
                       'converting a binary tree into a string so that it can '
                       'be stored or transmitted.</p>\n'
                       '\n'
                       '<p><strong>Deserialization</strong> is the reverse '
                       'process of reconstructing the tree from the '
                       'string.</p>\n'
                       '\n'
                       '<p>You must ensure that the tree can be '
                       '<strong>accurately reconstructed</strong>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input Tree:</strong>\n'
                       '    1\n'
                       '   / \\\n'
                       '  2   3\n'
                       '     / \\\n'
                       '    4   5\n'
                       '\n'
                       '<strong>Serialized:</strong> '
                       '"1,2,null,null,3,4,null,null,5,null,null"\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input Tree:</strong> []\n'
                       '<strong>Serialized:</strong> ""\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li>The number of nodes in the tree is in the range '
                       '<code>[0, 10<sup>4</sup>]</code></li>\n'
                       '<li><code>-1000 <= Node.val <= 1000</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'serializeDeserialize',
        'id': 'premium-47',
        'starter_code': {   'c': 'void serializeDeserialize() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    void serializeDeserialize() {\n'
                                   '        // Write your code here\n'
                                   '        \n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void serializeDeserialize() {\n'
                                    '        // Write your code here\n'
                                    '        \n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def serializeDeserialize():\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'serializeDeserialize <- function() {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Tree', 'DFS', 'BFS', 'Design'],
        'test_cases': [   {   'input': [[1, 2, 3, None, None, 4, 5]],
                              'output': [1, 2, 3, None, None, 4, 5]},
                          {'input': [[]], 'output': []},
                          {'input': [[1]], 'output': [1]},
                          {'input': [[1, None, 2]], 'output': [1, None, 2]},
                          {   'input': [[1, 2, None, 3, None, 4, None]],
                              'output': [1, 2, None, 3, None, 4, None]},
                          {   'input': [[1, 2, 3, 4, 5, 6, 7]],
                              'output': [1, 2, 3, 4, 5, 6, 7]},
                          {'input': [[-1, -2, -3]], 'output': [-1, -2, -3]},
                          {'input': [[0]], 'output': [0]},
                          {   'input': [[10, 20, 30, None, None, 40]],
                              'output': [10, 20, 30, None, None, 40]},
                          {'input': [[1, None, None]], 'output': [1]},
                          {   'input': [[5, 3, 7, 2, 4, 6, 8]],
                              'output': [5, 3, 7, 2, 4, 6, 8]},
                          {   'input': [[1, 2, None, None, 3]],
                              'output': [1, 2, None, None, 3]},
                          {'input': [[1000, -1000]], 'output': [1000, -1000]},
                          {   'input': [[1, None, 2, 3]],
                              'output': [1, None, 2, 3]},
                          {   'input': [[7, 3, None, None, 5]],
                              'output': [7, 3, None, None, 5]}],
        'title': 'Serialize and Deserialize Binary Tree',
        'titleSlug': 'serialize-and-deserialize-binary-tree'},
    {   'description': '\n'
                       '<p>There are <code>n</code> courses you can take, '
                       'where each course is described by two integers:</p>\n'
                       '\n'
                       '<p><code>courses[i] = [duration, lastDay]</code></p>\n'
                       '\n'
                       '<ul>\n'
                       '<li>You must take the course for <code>duration</code> '
                       'days</li>\n'
                       '<li>You must finish it on or before '
                       '<code>lastDay</code></li>\n'
                       '<li>You can only take <strong>one course at a '
                       'time</strong></li>\n'
                       '</ul>\n'
                       '\n'
                       '<p>Return <em>the maximum number of courses you can '
                       'take</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> courses = '
                       '[[100,200],[200,1300],[1000,1250],[2000,3200]]\n'
                       '<strong>Output:</strong> 3\n'
                       '<strong>Explanation:</strong>\n'
                       'You can take courses with durations 100, 200, and '
                       '1000.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> courses = [[1,2]]\n'
                       '<strong>Output:</strong> 1\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> courses = [[3,2],[4,3]]\n'
                       '<strong>Output:</strong> 0\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= courses.length <= '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>1 <= duration, lastDay <= '
                       '10<sup>4</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'scheduleCourse',
        'id': 'premium-48',
        'starter_code': {   'c': 'void scheduleCourse() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    void scheduleCourse() {\n'
                                   '        // Write your code here\n'
                                   '        \n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void scheduleCourse() {\n'
                                    '        // Write your code here\n'
                                    '        \n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def scheduleCourse():\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'scheduleCourse <- function() {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Greedy', 'Heap', 'Sorting'],
        'test_cases': [   {   'input': [   [   [100, 200],
                                               [200, 1300],
                                               [1000, 1250],
                                               [2000, 3200]]],
                              'output': 3},
                          {'input': [[[1, 2]]], 'output': 1},
                          {'input': [[[3, 2], [4, 3]]], 'output': 0},
                          {'input': [[[5, 5], [4, 6], [2, 6]]], 'output': 2},
                          {'input': [[[5, 5], [2, 6], [4, 6]]], 'output': 2},
                          {   'input': [[[1, 10], [2, 10], [3, 10], [4, 10]]],
                              'output': 4},
                          {'input': [[[3, 3], [2, 4], [1, 5]]], 'output': 3},
                          {'input': [[[5, 10], [6, 11], [7, 12]]], 'output': 1},
                          {'input': [[[2, 3], [1, 2]]], 'output': 2},
                          {'input': [[[10, 20], [5, 5], [5, 10]]], 'output': 2},
                          {'input': [[[7, 7], [2, 10], [1, 8]]], 'output': 2},
                          {   'input': [[[4, 4], [3, 5], [2, 6], [1, 7]]],
                              'output': 4},
                          {'input': [[[8, 8], [1, 9], [2, 10]]], 'output': 2},
                          {'input': [[[6, 6], [5, 7], [4, 8]]], 'output': 2},
                          {   'input': [[[1000, 1000], [999, 1000], [1, 1000]]],
                              'output': 2}],
        'title': 'Course Schedule III',
        'titleSlug': 'course-schedule-iii'},
    {   'description': '\n'
                       '<p>Given two sorted arrays <code>nums1</code> and '
                       '<code>nums2</code> of size <code>m</code> and '
                       '<code>n</code> respectively, return <strong>the '
                       'median</strong> of the two sorted arrays.</p>\n'
                       '\n'
                       '<p>The overall run time complexity should be '
                       '<code>O(log (m + n))</code>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums1 = [1,3], nums2 = [2]\n'
                       '<strong>Output:</strong> 2.0\n'
                       '<strong>Explanation:</strong> The merged array is '
                       '[1,2,3], and the median is 2.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums1 = [1,2], nums2 = [3,4]\n'
                       '<strong>Output:</strong> 2.5\n'
                       '<strong>Explanation:</strong> The merged array is '
                       '[1,2,3,4], median = (2 + 3) / 2.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>0 <= nums1.length <= 1000</code></li>\n'
                       '<li><code>0 <= nums2.length <= 1000</code></li>\n'
                       '<li><code>1 <= nums1.length + nums2.length <= '
                       '2000</code></li>\n'
                       '<li><code>-10<sup>6</sup> <= nums1[i], nums2[i] <= '
                       '10<sup>6</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Hard',
        'function_name': 'findMedianSortedArrays',
        'id': 'premium-26',
        'starter_code': {   'c': 'double findMedianSortedArrays(int* a, int n, '
                                 'int* b, int m) {\n'
                                 '    // Write your code here\n'
                                 '    return 0.0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    double '
                                   'findMedianSortedArrays(vector<int>& a, '
                                   'vector<int>& b) {\n'
                                   '        // Write your code here\n'
                                   '        return 0.0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public double '
                                    'findMedianSortedArrays(int[] a, int[] b) '
                                    '{\n'
                                    '        // Write your code here\n'
                                    '        return 0.0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def findMedianSortedArrays(a, b):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'findMedianSortedArrays <- function(a, b) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Binary Search', 'Divide and Conquer'],
        'test_cases': [   {'input': [[1, 3], [2]], 'output': 2.0},
                          {'input': [[1, 2], [3, 4]], 'output': 2.5},
                          {'input': [[], [1]], 'output': 1.0},
                          {'input': [[2], []], 'output': 2.0},
                          {'input': [[0, 0], [0, 0]], 'output': 0.0},
                          {'input': [[1], [2, 3, 4]], 'output': 2.5},
                          {'input': [[1, 2, 3], [4, 5, 6]], 'output': 3.5},
                          {'input': [[3], [1, 2]], 'output': 2.0},
                          {'input': [[1, 4, 7], [2, 3, 5, 6]], 'output': 4.0},
                          {'input': [[-5, -3, -1], [-2, 0, 2]], 'output': -1.5},
                          {   'input': [[1000000], [1000001]],
                              'output': 1000000.5},
                          {'input': [[1, 2], [3]], 'output': 2.0},
                          {   'input': [[1, 2, 3, 4], [5, 6, 7, 8]],
                              'output': 4.5},
                          {'input': [[1], [1]], 'output': 1.0},
                          {'input': [[2, 3], [1, 4]], 'output': 2.5}],
        'title': 'Median of Two Sorted Arrays',
        'titleSlug': 'median-of-two-sorted-arrays'},
    {   'description': '\n'
                       '<p>Given the <code>root</code> of a binary tree, '
                       "return <em>the level order traversal of its nodes' "
                       'values</em>.</p>\n'
                       '\n'
                       '<p><strong>Level order traversal</strong> means '
                       'traversing the tree level by level, from left to '
                       'right.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> root = '
                       '[3,9,20,null,null,15,7]\n'
                       '<strong>Output:</strong> [[3],[9,20],[15,7]]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> root = [1]\n'
                       '<strong>Output:</strong> [[1]]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> root = []\n'
                       '<strong>Output:</strong> []\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li>The number of nodes in the tree is in the range '
                       '<code>[0, 2000]</code></li>\n'
                       '<li><code>-1000 <= Node.val <= 1000</code></li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'levelOrder',
        'id': 'premium-49',
        'starter_code': {   'c': 'void levelOrder() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    void levelOrder() {\n'
                                   '        // Write your code here\n'
                                   '        \n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void levelOrder() {\n'
                                    '        // Write your code here\n'
                                    '        \n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def levelOrder():\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'levelOrder <- function() {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Tree', 'BFS', 'Queue'],
        'test_cases': [   {   'input': [[3, 9, 20, None, None, 15, 7]],
                              'output': [[3], [9, 20], [15, 7]]},
                          {'input': [[1]], 'output': [[1]]},
                          {'input': [[]], 'output': []},
                          {'input': [[1, 2, 3]], 'output': [[1], [2, 3]]},
                          {'input': [[1, None, 2]], 'output': [[1], [2]]},
                          {   'input': [[1, 2, None, 3, None]],
                              'output': [[1], [2], [3]]},
                          {   'input': [[1, 2, 3, 4, 5, 6, 7]],
                              'output': [[1], [2, 3], [4, 5, 6, 7]]},
                          {   'input': [[10, 5, 15, None, None, 12, 20]],
                              'output': [[10], [5, 15], [12, 20]]},
                          {'input': [[-1, -2, -3]], 'output': [[-1], [-2, -3]]},
                          {'input': [[0]], 'output': [[0]]},
                          {   'input': [[5, 3, 8, 1, 4, 7, 9]],
                              'output': [[5], [3, 8], [1, 4, 7, 9]]},
                          {   'input': [[1, 2, 3, None, 4, None, 5]],
                              'output': [[1], [2, 3], [4, 5]]},
                          {'input': [[1, 2]], 'output': [[1], [2]]},
                          {   'input': [[1, None, 2, 3]],
                              'output': [[1], [2], [3]]},
                          {   'input': [[7, 3, None, None, 5]],
                              'output': [[7], [3], [5]]}],
        'title': 'Binary Tree Level Order Traversal',
        'titleSlug': 'binary-tree-level-order-traversal'},
    {   'description': '\n'
                       '<p>Given an integer array <code>nums</code>, return '
                       '<code>true</code> if any value appears <strong>at '
                       'least twice</strong> in the array.</p>\n'
                       '\n'
                       '<p>Return <code>false</code> if every element is '
                       'distinct.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,2,3,1]\n'
                       '<strong>Output:</strong> true\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,2,3,4]\n'
                       '<strong>Output:</strong> false\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,1,1,3,3,4,3,2,4,2]\n'
                       '<strong>Output:</strong> true\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= '
                       '10<sup>5</sup></code></li>\n'
                       '<li><code>-10<sup>9</sup> <= nums[i] <= '
                       '10<sup>9</sup></code></li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'containsDuplicate',
        'id': 'premium-36',
        'starter_code': {   'c': 'int containsDuplicate(int* nums, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    bool containsDuplicate(vector<int>& '
                                   'nums) {\n'
                                   '        // Write your code here\n'
                                   '        return false;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public boolean '
                                    'containsDuplicate(int[] nums) {\n'
                                    '        // Write your code here\n'
                                    '        return false;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def containsDuplicate(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'containsDuplicate <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Hash Table', 'Sorting'],
        'test_cases': [   {'input': [[1, 2, 3, 1]], 'output': True},
                          {'input': [[1, 2, 3, 4]], 'output': False},
                          {   'input': [[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]],
                              'output': True},
                          {'input': [[1]], 'output': False},
                          {'input': [[2, 2]], 'output': True},
                          {'input': [[0, 1, 2, 3, 4]], 'output': False},
                          {'input': [[-1, -2, -3, -1]], 'output': True},
                          {   'input': [[100000, 200000, 300000]],
                              'output': False},
                          {'input': [[5, 5, 5, 5]], 'output': True},
                          {'input': [[9, 8, 7, 6, 5]], 'output': False},
                          {'input': [[1, 2, 3, 2, 5]], 'output': True},
                          {'input': [[0, 0]], 'output': True},
                          {'input': [[-10, 10, -10]], 'output': True},
                          {'input': [[3, 1]], 'output': False},
                          {'input': [[7, 7, 8, 9]], 'output': True}],
        'title': 'Contains Duplicate',
        'titleSlug': 'contains-duplicate'},
    {   'description': '\n'
                       '<p>Given an integer array <code>nums</code>, return '
                       '<em>an array <code>answer</code> such that</em>:</p>\n'
                       '\n'
                       '<p><code>answer[i]</code> = product of all elements of '
                       '<code>nums</code> except <code>nums[i]</code></p>\n'
                       '\n'
                       '<p>You must solve it:</p>\n'
                       '<ul>\n'
                       '<li><strong>without using division</strong></li>\n'
                       '<li>in <code>O(n)</code> time</li>\n'
                       '<li>The result fits in a 32-bit integer</li>\n'
                       '</ul>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,2,3,4]\n'
                       '<strong>Output:</strong> [24,12,8,6]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [-1,1,0,-3,3]\n'
                       '<strong>Output:</strong> [0,0,9,0,0]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>2 <= nums.length <= '
                       '10<sup>5</sup></code></li>\n'
                       '<li><code>-30 <= nums[i] <= 30</code></li>\n'
                       '<li>Product of any prefix or suffix fits in 32-bit '
                       'integer</li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'productExceptSelf',
        'id': 'premium-37',
        'starter_code': {   'c': 'void productExceptSelf(int* nums, int n, '
                                 'int* result) {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    vector<int> '
                                   'productExceptSelf(vector<int>& nums) {\n'
                                   '        // Write your code here\n'
                                   '        return {};\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int[] productExceptSelf(int[] '
                                    'nums) {\n'
                                    '        // Write your code here\n'
                                    '        return new int[0];\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def productExceptSelf(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'productExceptSelf <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Prefix Sum'],
        'test_cases': [   {'input': [[1, 2, 3, 4]], 'output': [24, 12, 8, 6]},
                          {   'input': [[-1, 1, 0, -3, 3]],
                              'output': [0, 0, 9, 0, 0]},
                          {'input': [[2, 3]], 'output': [3, 2]},
                          {'input': [[1, 1, 1, 1]], 'output': [1, 1, 1, 1]},
                          {'input': [[0, 0]], 'output': [0, 0]},
                          {   'input': [[5, 4, 3, 2, 1]],
                              'output': [24, 30, 40, 60, 120]},
                          {   'input': [[10, 3, 5, 6, 2]],
                              'output': [180, 600, 360, 300, 900]},
                          {'input': [[1, 0, 3, 0]], 'output': [0, 0, 0, 0]},
                          {   'input': [[-1, -2, -3, -4]],
                              'output': [-24, -12, -8, -6]},
                          {'input': [[9, 1, 2, 3]], 'output': [6, 54, 27, 18]},
                          {'input': [[100, 2, 5]], 'output': [10, 500, 200]},
                          {'input': [[2, 2, 2, 2]], 'output': [8, 8, 8, 8]},
                          {'input': [[1, 2, 0, 4]], 'output': [0, 0, 8, 0]},
                          {'input': [[7, 3, 5]], 'output': [15, 35, 21]},
                          {'input': [[-2, 0, -1]], 'output': [0, 2, 0]}],
        'title': 'Product of Array Except Self',
        'titleSlug': 'product-of-array-except-self'},
    {   'description': '\n'
                       '<p>Given a string <code>s</code>, find the length of '
                       'the <strong>longest substring</strong> without '
                       'repeating characters.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "abcabcbb"\n'
                       '<strong>Output:</strong> 3\n'
                       '<strong>Explanation:</strong> The answer is "abc", '
                       'with the length of 3.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "bbbbb"\n'
                       '<strong>Output:</strong> 1\n'
                       '<strong>Explanation:</strong> The answer is "b", with '
                       'the length of 1.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "pwwkew"\n'
                       '<strong>Output:</strong> 3\n'
                       '<strong>Explanation:</strong> The answer is "wke", '
                       'with the length of 3. Notice that "pwke" is a '
                       'subsequence, not a substring.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>0 <= s.length <= 5 * '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>s</code> consists of English letters, '
                       'digits, symbols and spaces.</li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'lengthOfLongestSubstring',
        'id': 'premium-7',
        'starter_code': {   'c': 'int lengthOfLongestSubstring(char* s) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int lengthOfLongestSubstring(string s) '
                                   '{\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int '
                                    'lengthOfLongestSubstring(String s) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def lengthOfLongestSubstring(s):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'lengthOfLongestSubstring <- function(s) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Hash Table', 'String', 'Sliding Window'],
        'test_cases': [   {'input': ['abcabcbb'], 'output': 3},
                          {'input': ['bbbbb'], 'output': 1},
                          {'input': ['pwwkew'], 'output': 3},
                          {'input': [''], 'output': 0},
                          {'input': ['a'], 'output': 1},
                          {'input': ['au'], 'output': 2},
                          {'input': ['abcdef'], 'output': 6},
                          {'input': ['xyz'], 'output': 3},
                          {'input': ['aaaa'], 'output': 1},
                          {'input': [' '], 'output': 1},
                          {'input': ['a b c'], 'output': 3},
                          {'input': ['abc123'], 'output': 6},
                          {'input': ['!!abc'], 'output': 3},
                          {'input': ['dvdf'], 'output': 3},
                          {'input': ['abba'], 'output': 2},
                          {'input': ['tmmzuxt'], 'output': 5}],
        'title': 'Longest Substring Without Repeating Characters',
        'titleSlug': 'longest-substring-without-repeating-characters'},
    {   'description': '\n'
                       '<p>Given two strings <code>s</code> and '
                       '<code>t</code>, return <code>true</code> if '
                       '<code>t</code> is an <strong>anagram</strong> of '
                       '<code>s</code>, and <code>false</code> otherwise.</p>\n'
                       '\n'
                       '<p>An <strong>Anagram</strong> is a word or phrase '
                       'formed by rearranging the letters of a different word '
                       'or phrase, using all the original letters exactly '
                       'once.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "anagram", t = "nagaram"\n'
                       '<strong>Output:</strong> true\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> s = "rat", t = "car"\n'
                       '<strong>Output:</strong> false\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= s.length, t.length <= 5 * '
                       '10<sup>4</sup></code></li>\n'
                       '<li><code>s</code> and <code>t</code> consist of '
                       'lowercase English letters.</li>\n'
                       '</ul>\n',
        'difficulty': 'Easy',
        'function_name': 'isAnagram',
        'id': 'premium-9',
        'starter_code': {   'c': 'int isAnagram(char* s, char* t) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    bool isAnagram(string s, string t) {\n'
                                   '        // Write your code here\n'
                                   '        return false;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public boolean isAnagram(String s, '
                                    'String t) {\n'
                                    '        // Write your code here\n'
                                    '        return false;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def isAnagram(s, t):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'isAnagram <- function(s, t) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['String', 'Hash Table', 'Sorting'],
        'test_cases': [   {'input': ['anagram', 'nagaram'], 'output': True},
                          {'input': ['rat', 'car'], 'output': False},
                          {'input': ['listen', 'silent'], 'output': True},
                          {'input': ['a', 'a'], 'output': True},
                          {'input': ['', ''], 'output': True},
                          {'input': ['abc', 'bca'], 'output': True},
                          {'input': ['abc', 'abcd'], 'output': False},
                          {'input': ['aabbcc', 'abcabc'], 'output': True},
                          {'input': ['hello', 'billion'], 'output': False},
                          {'input': ['aaaa', 'aaa'], 'output': False},
                          {   'input': ['programming', 'grammingpro'],
                              'output': True},
                          {'input': ['test', 'tttt'], 'output': False},
                          {'input': ['abc', 'def'], 'output': False},
                          {'input': ['aabbccdd', 'ddccbbaa'], 'output': True},
                          {'input': ['z', 'y'], 'output': False}],
        'title': 'Valid Anagram',
        'titleSlug': 'valid-anagram'},
    {   'description': '\n'
                       '<p>You are given the heads of two sorted linked lists '
                       '<code>list1</code> and <code>list2</code>.</p>\n'
                       '\n'
                       '<p>Merge the two lists into one '
                       '<strong>sorted</strong> list. The list should be made '
                       'by splicing together the nodes of the first two '
                       'lists.</p>\n'
                       '\n'
                       '<p>Return <em>the head of the merged linked '
                       'list</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> list1 = [1,2,4], list2 = '
                       '[1,3,4]\n'
                       '<strong>Output:</strong> [1,1,2,3,4,4]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> list1 = [], list2 = []\n'
                       '<strong>Output:</strong> []\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> list1 = [], list2 = [0]\n'
                       '<strong>Output:</strong> [0]\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Note:</strong> For simplicity, this problem '
                       'uses arrays instead of linked lists.</p>\n',
        'difficulty': 'Easy',
        'function_name': 'mergeTwoLists',
        'id': 'premium-5',
        'starter_code': {   'c': 'void mergeTwoLists() {\n'
                                 '    // Write your code here\n'
                                 '    \n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    void mergeTwoLists() {\n'
                                   '        // Write your code here\n'
                                   '        \n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public void mergeTwoLists() {\n'
                                    '        // Write your code here\n'
                                    '        \n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def mergeTwoLists():\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'mergeTwoLists <- function() {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Linked List', 'Array'],
        'test_cases': [   {   'input': [[1, 2, 4], [1, 3, 4]],
                              'output': [1, 1, 2, 3, 4, 4]},
                          {   'input': [[1, 3, 5], [2, 4, 6]],
                              'output': [1, 2, 3, 4, 5, 6]},
                          {'input': [[], [1, 2]], 'output': [1, 2]},
                          {'input': [[1, 2], []], 'output': [1, 2]},
                          {'input': [[], []], 'output': []},
                          {'input': [[1], [2]], 'output': [1, 2]},
                          {'input': [[2], [1]], 'output': [1, 2]},
                          {   'input': [[1, 1, 1], [1, 1]],
                              'output': [1, 1, 1, 1, 1]},
                          {   'input': [[-3, -1, 0], [-2, 1, 3]],
                              'output': [-3, -2, -1, 0, 1, 3]},
                          {   'input': [[1], [1, 2, 3, 4, 5]],
                              'output': [1, 1, 2, 3, 4, 5]},
                          {   'input': [[1, 2, 3, 4, 5], [6]],
                              'output': [1, 2, 3, 4, 5, 6]},
                          {   'input': [[1, 2], [100, 200]],
                              'output': [1, 2, 100, 200]},
                          {   'input': [[1, 3, 5, 7], [2, 4, 6, 8]],
                              'output': [1, 2, 3, 4, 5, 6, 7, 8]},
                          {   'input': [[0, 2, 4], [0, 1, 3]],
                              'output': [0, 0, 1, 2, 3, 4]},
                          {'input': [[0], [0]], 'output': [0, 0]}],
        'title': 'Merge Two Sorted Lists',
        'titleSlug': 'merge-two-sorted-lists'},
    {   'description': '\n'
                       '<p>Given an array <code>nums</code> containing <code>n '
                       '+ 1</code> integers where each integer is in the range '
                       '<code>[1, n]</code> inclusive.</p>\n'
                       '\n'
                       '<p>There is <strong>only one repeated number</strong>, '
                       'but it may appear more than once.</p>\n'
                       '\n'
                       '<p>You must solve the problem <strong>without '
                       'modifying the array</strong> and using only '
                       '<strong>constant extra space</strong>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1,3,4,2,2]\n'
                       '<strong>Output:</strong> 2\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [3,1,3,4,2]\n'
                       '<strong>Output:</strong> 3\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= n <= 10<sup>5</sup></code></li>\n'
                       '<li><code>nums.length = n + 1</code></li>\n'
                       '<li><code>1 <= nums[i] <= n</code></li>\n'
                       '<li>Exactly one integer appears more than once</li>\n'
                       '</ul>\n',
        'difficulty': 'Medium',
        'function_name': 'findDuplicate',
        'id': 'premium-50',
        'starter_code': {   'c': 'int findDuplicate(int* nums, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int findDuplicate(vector<int>& nums) '
                                   '{\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int findDuplicate(int[] nums) '
                                    '{\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def findDuplicate(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'findDuplicate <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Two Pointers', 'Binary Search'],
        'test_cases': [   {'input': [[1, 3, 4, 2, 2]], 'output': 2},
                          {'input': [[3, 1, 3, 4, 2]], 'output': 3},
                          {'input': [[1, 1]], 'output': 1},
                          {'input': [[1, 4, 4, 2, 3]], 'output': 4},
                          {   'input': [[2, 5, 9, 6, 9, 3, 8, 9, 7, 1]],
                              'output': 9},
                          {'input': [[1, 2, 3, 4, 5, 5]], 'output': 5},
                          {'input': [[3, 2, 1, 4, 3]], 'output': 3},
                          {'input': [[2, 2, 2, 2, 2]], 'output': 2},
                          {'input': [[5, 4, 3, 2, 1, 1]], 'output': 1},
                          {'input': [[1, 3, 2, 4, 2]], 'output': 2},
                          {'input': [[6, 1, 5, 2, 4, 3, 6]], 'output': 6},
                          {'input': [[7, 7, 1, 2, 3, 4, 5, 6]], 'output': 7},
                          {'input': [[8, 1, 2, 3, 4, 5, 6, 7, 8]], 'output': 8},
                          {   'input': [[9, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
                              'output': 9},
                          {'input': [[4, 1, 4, 2, 3]], 'output': 4}],
        'title': 'Find the Duplicate Number',
        'titleSlug': 'find-the-duplicate-number'},
    {   'description': '\n'
                       '<p>Given an integer array <code>nums</code>, find the '
                       'subarray with the largest sum, and return <em>its '
                       'sum</em>.</p>\n'
                       '\n'
                       '<p><strong>Example 1:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = '
                       '[-2,1,-3,4,-1,2,1,-5,4]\n'
                       '<strong>Output:</strong> 6\n'
                       '<strong>Explanation:</strong> The subarray [4,-1,2,1] '
                       'has the largest sum 6.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 2:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [1]\n'
                       '<strong>Output:</strong> 1\n'
                       '<strong>Explanation:</strong> The subarray [1] has the '
                       'largest sum 1.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Example 3:</strong></p>\n'
                       '<pre>\n'
                       '<strong>Input:</strong> nums = [5,4,-1,7,8]\n'
                       '<strong>Output:</strong> 23\n'
                       '<strong>Explanation:</strong> The subarray '
                       '[5,4,-1,7,8] has the largest sum 23.\n'
                       '</pre>\n'
                       '\n'
                       '<p><strong>Constraints:</strong></p>\n'
                       '<ul>\n'
                       '<li><code>1 <= nums.length <= '
                       '10<sup>5</sup></code></li>\n'
                       '<li><code>-10<sup>4</sup> <= nums[i] <= '
                       '10<sup>4</sup></code></li>\n'
                       '</ul>\n'
                       '\n'
                       '<p><strong>Follow up:</strong> If you have figured out '
                       'the O(n) solution, try coding another solution using '
                       'the divide and conquer approach.</p>\n',
        'difficulty': 'Medium',
        'function_name': 'maxSubArray',
        'id': 'premium-8',
        'starter_code': {   'c': 'int maxSubArray(int* nums, int n) {\n'
                                 '    // Write your code here\n'
                                 '    return 0;\n'
                                 '}\n',
                            'cpp': 'class Solution {\n'
                                   'public:\n'
                                   '    int maxSubArray(vector<int>& nums) {\n'
                                   '        // Write your code here\n'
                                   '        return 0;\n'
                                   '    }\n'
                                   '};\n',
                            'java': 'class Solution {\n'
                                    '    public int maxSubArray(int[] nums) {\n'
                                    '        // Write your code here\n'
                                    '        return 0;\n'
                                    '    }\n'
                                    '}\n',
                            'python': 'def maxSubArray(nums):\n'
                                      '    # Write your code here\n'
                                      '    pass\n',
                            'r': 'maxSubArray <- function(nums) {\n'
                                 '    # Write your code here\n'
                                 '    return(c())\n'
                                 '}\n'},
        'tags': ['Array', 'Divide and Conquer', 'Dynamic Programming'],
        'test_cases': [   {   'input': [[-2, 1, -3, 4, -1, 2, 1, -5, 4]],
                              'output': 6},
                          {'input': [[1]], 'output': 1},
                          {'input': [[5, 4, -1, 7, 8]], 'output': 23},
                          {'input': [[-1]], 'output': -1},
                          {'input': [[-2, -1]], 'output': -1},
                          {'input': [[-5, -3, -1, -4]], 'output': -1},
                          {'input': [[1, 2, 3, 4, 5]], 'output': 15},
                          {'input': [[10, 20, 30]], 'output': 60},
                          {'input': [[0, -2, 3, -1, 4]], 'output': 6},
                          {'input': [[0, 0, 0, 1]], 'output': 1},
                          {'input': [[1, -1, 1, -1, 1]], 'output': 1},
                          {'input': [[5, -3, 5]], 'output': 7},
                          {'input': [[100, -50, 50, -25, 75]], 'output': 150},
                          {'input': [[-10, -5, 100, -20, -10]], 'output': 100},
                          {'input': [[1, -1]], 'output': 1},
                          {'input': [[-3, 4]], 'output': 4}],
        'title': 'Maximum Subarray',
        'titleSlug': 'maximum-subarray'}]