
def get_local_problems():
    """
    Returns a list of local coding problems with LeetCode-style format.
    Each problem has:
      - id: unique identifier
      - title: problem title
      - description: HTML description
      - difficulty: Easy/Medium/Hard
      - starter_code: dict with language keys (python, java, c)
      - test_cases: list of {input, output} dicts
      - solution: reference solution
      - function_name: the function/method name to call
    """
    return [
        {
            "id": "premium-1",
            "title": "Two Sum",
            "titleSlug": "two-sum",
            "description": """
<p>Given an array of integers <code>nums</code> and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>

<p>You may assume that each input would have <strong>exactly one solution</strong>, and you may not use the same element twice.</p>

<p>You can return the answer in any order.</p>

<p><strong>Example 1:</strong></p>
<pre>
<strong>Input:</strong> nums = [2,7,11,15], target = 9
<strong>Output:</strong> [0,1]
<strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].
</pre>

<p><strong>Example 2:</strong></p>
<pre>
<strong>Input:</strong> nums = [3,2,4], target = 6
<strong>Output:</strong> [1,2]
</pre>

<p><strong>Example 3:</strong></p>
<pre>
<strong>Input:</strong> nums = [3,3], target = 6
<strong>Output:</strong> [0,1]
</pre>

<p><strong>Constraints:</strong></p>
<ul>
<li><code>2 <= nums.length <= 10<sup>4</sup></code></li>
<li><code>-10<sup>9</sup> <= nums[i] <= 10<sup>9</sup></code></li>
<li><code>-10<sup>9</sup> <= target <= 10<sup>9</sup></code></li>
<li><strong>Only one valid answer exists.</strong></li>
</ul>
""",
            "difficulty": "Easy",
            "tags": ["Array", "Hash Table"],
            "function_name": "twoSum",
            "starter_code": {
                "python": """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Write your code here
        pass
""",
                "javascript": """function twoSum(nums, target) {
    // Write your code here
    return [];
}""",
                "java": """class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Write your code here
        return new int[]{};
    }
}""",
                "cpp": """class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // Write your code here
        return {};
    }
};"""
            },
            "test_cases": [
                {"input": [[2,7,11,15], 9], "output": [0, 1]},
                {"input": [[3,2,4], 6], "output": [1, 2]},
                {"input": [[3,3], 6], "output": [0, 1]},
                {"input": [[1,5,9], 10], "output": [0, 2]},
                {"input": [[-1,-2,-3,-4,-5], -8], "output": [2, 4]},
                {"input": [[10,20,30,40], 50], "output": [1, 2]},
                {"input": [[0,4,3,0], 0], "output": [0, 3]},
                {"input": [[-3,4,3,90], 0], "output": [0, 2]},
                {"input": [[5,5], 10], "output": [0, 1]},
                {"input": [[1,2,3,4,5], 9], "output": [3, 4]},
                {"input": [[100,200,300], 500], "output": [1, 2]},
                {"input": [[-10,10], 0], "output": [0, 1]},
                {"input": [[7,2], 9], "output": [0, 1]},
                {"input": [[1000,2000,3000], 5000], "output": [1, 2]},
                {"input": [[1,100], 101], "output": [0, 1]},
            ],
            "solution": """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
"""
        },
        {
            "id": "premium-2",
            "title": "Palindrome Number",
            "titleSlug": "palindrome-number",
            "description": """
<p>Given an integer <code>x</code>, return <code>true</code> if <code>x</code> is a <strong>palindrome</strong>, and <code>false</code> otherwise.</p>

<p><strong>Example 1:</strong></p>
<pre>
<strong>Input:</strong> x = 121
<strong>Output:</strong> true
<strong>Explanation:</strong> 121 reads as 121 from left to right and from right to left.
</pre>

<p><strong>Example 2:</strong></p>
<pre>
<strong>Input:</strong> x = -121
<strong>Output:</strong> false
<strong>Explanation:</strong> From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
</pre>

<p><strong>Example 3:</strong></p>
<pre>
<strong>Input:</strong> x = 10
<strong>Output:</strong> false
<strong>Explanation:</strong> Reads 01 from right to left. Therefore it is not a palindrome.
</pre>

<p><strong>Constraints:</strong></p>
<ul>
<li><code>-2<sup>31</sup> <= x <= 2<sup>31</sup> - 1</code></li>
</ul>
""",
            "difficulty": "Easy",
            "tags": ["Math"],
            "function_name": "isPalindrome",
            "starter_code": {
                "python": """class Solution:
    def isPalindrome(self, x: int) -> bool:
        # Write your code here
        pass
""",
                "javascript": """function isPalindrome(x) {
    // Write your code here
    return false;
}""",
                "java": """class Solution {
    public boolean isPalindrome(int x) {
        // Write your code here
        return false;
    }
}""",
                "cpp": """class Solution {
public:
    bool isPalindrome(int x) {
        // Write your code here
        return false;
    }
};"""
            },
            "test_cases": [
                {"input": [121], "output": True},
                {"input": [-121], "output": False},
                {"input": [10], "output": False},
                {"input": [0], "output": True},
                {"input": [1], "output": True},
                {"input": [12321], "output": True},
                {"input": [123456], "output": False},
                {"input": [1221], "output": True},
                {"input": [11], "output": True},
                {"input": [123], "output": False},
                {"input": [-100], "output": False},
                {"input": [1000021], "output": False},
                {"input": [1000000001], "output": True},
                {"input": [11111111], "output": True},
                {"input": [12344321], "output": True},
            ],
            "solution": """class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        return str(x) == str(x)[::-1]
"""
        },
        {
            "id": "premium-3",
            "title": "Reverse Integer",
            "titleSlug": "reverse-integer",
            "description": """
<p>Given a signed 32-bit integer <code>x</code>, return <code>x</code> <em>with its digits reversed</em>. If reversing <code>x</code> causes the value to go outside the signed 32-bit integer range <code>[-2<sup>31</sup>, 2<sup>31</sup> - 1]</code>, then return <code>0</code>.</p>

<p><strong>Assume the environment does not allow you to store 64-bit integers (signed or unsigned).</strong></p>

<p><strong>Example 1:</strong></p>
<pre>
<strong>Input:</strong> x = 123
<strong>Output:</strong> 321
</pre>

<p><strong>Example 2:</strong></p>
<pre>
<strong>Input:</strong> x = -123
<strong>Output:</strong> -321
</pre>

<p><strong>Example 3:</strong></p>
<pre>
<strong>Input:</strong> x = 120
<strong>Output:</strong> 21
</pre>

<p><strong>Constraints:</strong></p>
<ul>
<li><code>-2<sup>31</sup> <= x <= 2<sup>31</sup> - 1</code></li>
</ul>
""",
            "difficulty": "Medium",
            "tags": ["Math"],
            "function_name": "reverse",
            "starter_code": {
                "python": """class Solution:
    def reverse(self, x: int) -> int:
        # Write your code here
        pass
""",
                "javascript": """function reverse(x) {
    // Write your code here
    return 0;
}"""
            },
            "test_cases": [
                {"input": [123], "output": 321},
                {"input": [-123], "output": -321},
                {"input": [120], "output": 21},
                {"input": [0], "output": 0},
                {"input": [1534236469], "output": 0},
                {"input": [-2147483648], "output": 0},
                {"input": [100], "output": 1},
                {"input": [1], "output": 1},
                {"input": [-1], "output": -1},
                {"input": [1000000003], "output": 0},
                {"input": [12], "output": 21},
                {"input": [-12], "output": -21},
                {"input": [1000], "output": 1},
                {"input": [2147483647], "output": 0},
                {"input": [1463847412], "output": 2147483641},
            ],
            "solution": """class Solution:
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        x = abs(x)
        reversed_x = int(str(x)[::-1]) * sign
        if reversed_x < -2**31 or reversed_x > 2**31 - 1:
            return 0
        return reversed_x
"""
        },
        {
            "id": "premium-4",
            "title": "Valid Parentheses",
            "titleSlug": "valid-parentheses",
            "description": """
<p>Given a string <code>s</code> containing just the characters <code>'('</code>, <code>')'</code>, <code>'{'</code>, <code>'}'</code>, <code>'['</code> and <code>']'</code>, determine if the input string is valid.</p>

<p>An input string is valid if:</p>
<ol>
<li>Open brackets must be closed by the same type of brackets.</li>
<li>Open brackets must be closed in the correct order.</li>
<li>Every close bracket has a corresponding open bracket of the same type.</li>
</ol>

<p><strong>Example 1:</strong></p>
<pre>
<strong>Input:</strong> s = "()"
<strong>Output:</strong> true
</pre>

<p><strong>Example 2:</strong></p>
<pre>
<strong>Input:</strong> s = "()[]{}"
<strong>Output:</strong> true
</pre>

<p><strong>Example 3:</strong></p>
<pre>
<strong>Input:</strong> s = "(]"
<strong>Output:</strong> false
</pre>

<p><strong>Constraints:</strong></p>
<ul>
<li><code>1 <= s.length <= 10<sup>4</sup></code></li>
<li><code>s</code> consists of parentheses only <code>'()[]{}'</code>.</li>
</ul>
""",
            "difficulty": "Easy",
            "tags": ["String", "Stack"],
            "function_name": "isValid",
            "starter_code": {
                "python": """class Solution:
    def isValid(self, s: str) -> bool:
        # Write your code here
        pass
""",
                "javascript": """function isValid(s) {
    // Write your code here
    return false;
}"""
            },
            "test_cases": [
                {"input": ["()"], "output": True},
                {"input": ["()[]{}"], "output": True},
                {"input": ["(]"], "output": False},
                {"input": ["([)]"], "output": False},
                {"input": ["{[]}"], "output": True},
                {"input": [""], "output": True},
                {"input": ["("], "output": False},
                {"input": [")"], "output": False},
                {"input": ["((()))"], "output": True},
                {"input": ["({[()]})"], "output": True},
                {"input": ["{{{{}}}}"], "output": True},
                {"input": ["[[[[]"], "output": False},
                {"input": ["((((()))))"], "output": True},
                {"input": ["{[()]}{[()]}"], "output": True},
                {"input": ["((()))(())"], "output": True},
            ],
            "solution": """class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        for char in s:
            if char in mapping:
                if not stack or stack.pop() != mapping[char]:
                    return False
            else:
                stack.append(char)
        return len(stack) == 0
"""
        },
        {
            "id": "premium-5",
            "title": "Merge Two Sorted Lists",
            "titleSlug": "merge-two-sorted-lists",
            "description": """
<p>You are given the heads of two sorted linked lists <code>list1</code> and <code>list2</code>.</p>

<p>Merge the two lists into one <strong>sorted</strong> list. The list should be made by splicing together the nodes of the first two lists.</p>

<p>Return <em>the head of the merged linked list</em>.</p>

<p><strong>Example 1:</strong></p>
<pre>
<strong>Input:</strong> list1 = [1,2,4], list2 = [1,3,4]
<strong>Output:</strong> [1,1,2,3,4,4]
</pre>

<p><strong>Example 2:</strong></p>
<pre>
<strong>Input:</strong> list1 = [], list2 = []
<strong>Output:</strong> []
</pre>

<p><strong>Example 3:</strong></p>
<pre>
<strong>Input:</strong> list1 = [], list2 = [0]
<strong>Output:</strong> [0]
</pre>

<p><strong>Note:</strong> For simplicity, this problem uses arrays instead of linked lists.</p>
""",
            "difficulty": "Easy",
            "tags": ["Linked List", "Array"],
            "function_name": "mergeTwoLists",
            "starter_code": {
                "python": """class Solution:
    def mergeTwoLists(self, list1: List[int], list2: List[int]) -> List[int]:
        # Write your code here
        # For simplicity, we use arrays instead of linked lists
        pass
"""
            },
            "test_cases": [
                {"input": [[1,2,4], [1,3,4]], "output": [1,1,2,3,4,4]},
                {"input": [[], []], "output": []},
                {"input": [[], [0]], "output": [0]},
                {"input": [[1], [2]], "output": [1,2]},
                {"input": [[5], [1,2,3,4]], "output": [1,2,3,4,5]},
            ],
            "solution": """class Solution:
    def mergeTwoLists(self, list1: List[int], list2: List[int]) -> List[int]:
        result = []
        i, j = 0, 0
        while i < len(list1) and j < len(list2):
            if list1[i] <= list2[j]:
                result.append(list1[i])
                i += 1
            else:
                result.append(list2[j])
                j += 1
        result.extend(list1[i:])
        result.extend(list2[j:])
        return result
"""
        },
        {
            "id": "premium-6",
            "title": "Subarray Sum Equals K",
            "titleSlug": "subarray-sum-equals-k",
            "description": """
<p>Given an array of integers <code>nums</code> and an integer <code>k</code>, return <em>the total number of subarrays whose sum equals to <code>k</code></em>.</p>
<p>A subarray is a contiguous <strong>non-empty</strong> sequence of elements within an array.</p>
""",
            "difficulty": "Medium",
            "tags": ["Array", "Hash Table", "Prefix Sum"],
            "function_name": "subarraySum",
            "starter_code": {
                "python": """class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # Write your code here
        pass
"""
            },
            "test_cases": [
                {"input": [[1,1,1], 2], "output": 2},
                {"input": [[1,2,3], 3], "output": 2},
                {"input": [[1], 0], "output": 0},
                {"input": [[-1,-1,1], 0], "output": 1},
            ],
            "solution": """class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        sum_counts = {0: 1}
        current_sum = 0
        for num in nums:
            current_sum += num
            if current_sum - k in sum_counts:
                count += sum_counts[current_sum - k]
            sum_counts[current_sum] = sum_counts.get(current_sum, 0) + 1
        return count
"""
        },
        {
            "id": "premium-7",
            "title": "Longest Substring Without Repeating Characters",
            "titleSlug": "longest-substring-without-repeating-characters",
            "description": """
<p>Given a string <code>s</code>, find the length of the <strong>longest subarray</strong> without repeating characters.</p>
""",
            "difficulty": "Medium",
            "tags": ["Hash Table", "String", "Sliding Window"],
            "function_name": "lengthOfLongestSubstring",
            "starter_code": {
                "python": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Write your code here
        pass
"""
            },
            "test_cases": [
                {"input": ["abcabcbb"], "output": 3},
                {"input": ["bbbbb"], "output": 1},
                {"input": ["pwwkew"], "output": 3},
                {"input": [""], "output": 0},
            ],
            "solution": """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_map = {}
        max_len = 0
        start = 0
        for i, char in enumerate(s):
            if char in char_map and char_map[char] >= start:
                start = char_map[char] + 1
            char_map[char] = i
            max_len = max(max_len, i - start + 1)
        return max_len
"""
        },
        {
            "id": "premium-8",
            "title": "Maximum Subarray",
            "titleSlug": "maximum-subarray",
            "description": """
<p>Given an integer array <code>nums</code>, find the subarray with the largest sum, and return <em>its sum</em>.</p>
""",
            "difficulty": "Medium",
            "tags": ["Array", "Divide and Conquer", "Dynamic Programming"],
            "function_name": "maxSubArray",
            "starter_code": {
                "python": """class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # Write your code here
        pass
"""
            },
            "test_cases": [
                {"input": [[-2,1,-3,4,-1,2,1,-5,4]], "output": 6},
                {"input": [[1]], "output": 1},
                {"input": [[5,4,-1,7,8]], "output": 23},
            ],
            "solution": """class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]
        current_sum = nums[0]
        for i in range(1, len(nums)):
            current_sum = max(nums[i], current_sum + nums[i])
            max_sum = max(max_sum, current_sum)
        return max_sum
"""
        }
    ]
