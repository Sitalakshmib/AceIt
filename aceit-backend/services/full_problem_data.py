
# Full dataset of 50 Coding Problems for Offline Fallback
# Includes Starter Codes for: Python, Java, C++, C, R
# Includes 15 Test Cases per problem

FULL_PROBLEM_DATA = [
    {
        "id": "premium-1",
        "title": "Two Sum",
        "titleSlug": "two-sum",
        "description": "<p>Given an array of integers <code>nums</code> and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p><p>You may assume that each input would have <strong>exactly one solution</strong>, and you may not use the same element twice.</p><p>You can return the answer in any order.</p><p><strong>Example 1:</strong><br>Input: nums = [2,7,11,15], target = 9<br>Output: [0,1]</p>",
        "difficulty": "Easy",
        "tags": ["Array", "Hash Table"],
        "function_name": "twoSum",
        "starter_code": {
            "python": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        # Write your code here\n        pass",
            "java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Write your code here\n        return new int[]{};\n    }\n}",
            "cpp": "class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Write your code here\n        return {};\n    }\n};",
            "c": "/**\n * Note: The returned array must be malloced, assume caller calls free().\n */\nint* twoSum(int* nums, int numsSize, int target, int* returnSize) {\n    // Write your code here\n    *returnSize = 2;\n    return 0;\n}",
            "r": "twoSum <- function(nums, target) {\n  # Write your code here\n  return(c())\n}"
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
            {"input": [[1,100], 101], "output": [0, 1]}
        ]
    },
    {
        "id": "premium-2",
        "title": "Palindrome Number",
        "titleSlug": "palindrome-number",
        "description": "<p>Given an integer <code>x</code>, return <code>true</code> if <code>x</code> is a <strong>palindrome</strong>, and <code>false</code> otherwise.</p><p><strong>Example 1:</strong><br>Input: x = 121<br>Output: true</p>",
        "difficulty": "Easy",
        "tags": ["Math"],
        "function_name": "isPalindrome",
        "starter_code": {
            "python": "class Solution:\n    def isPalindrome(self, x: int) -> bool:\n        # Write your code here\n        pass",
            "java": "class Solution {\n    public boolean isPalindrome(int x) {\n        // Write your code here\n        return false;\n    }\n}",
            "cpp": "class Solution {\npublic:\n    bool isPalindrome(int x) {\n        // Write your code here\n        return false;\n    }\n};",
            "c": "bool isPalindrome(int x) {\n    // Write your code here\n    return false;\n}",
            "r": "isPalindrome <- function(x) {\n  # Write your code here\n  return(FALSE)\n}"
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
            {"input": [12344321], "output": True}
        ]
    },
    {
        "id": "premium-3",
        "title": "Reverse Integer",
        "titleSlug": "reverse-integer",
        "description": "<p>Given a signed 32-bit integer <code>x</code>, return <code>x</code> <em>with its digits reversed</em>. If reversing <code>x</code> causes the value to go outside the signed 32-bit integer range <code>[-2<sup>31</sup>, 2<sup>31</sup> - 1]</code>, then return <code>0</code>.</p>",
        "difficulty": "Medium",
        "tags": ["Math"],
        "function_name": "reverse",
        "starter_code": {
            "python": "class Solution:\n    def reverse(self, x: int) -> int:\n        # Write your code here\n        pass",
            "java": "class Solution {\n    public int reverse(int x) {\n        // Write your code here\n        return 0;\n    }\n}",
            "cpp": "class Solution {\npublic:\n    int reverse(int x) {\n        // Write your code here\n        return 0;\n    }\n};",
            "c": "int reverse(int x) {\n    // Write your code here\n    return 0;\n}",
            "r": "reverse <- function(x) {\n  # Write your code here\n  return(0)\n}"
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
            {"input": [1463847412], "output": 2147483641}
        ]
    },
    {
        "id": "premium-4",
        "title": "Valid Parentheses",
        "titleSlug": "valid-parentheses",
        "description": "<p>Given a string <code>s</code> containing just the characters <code>'('</code>, <code>')'</code>, <code>'{'</code>, <code>'}'</code>, <code>'['</code> and <code>']'</code>, determine if the input string is valid.</p>",
        "difficulty": "Easy",
        "tags": ["String", "Stack"],
        "function_name": "isValid",
        "starter_code": {
            "python": "class Solution:\n    def isValid(self, s: str) -> bool:\n        # Write your code here\n        pass",
            "java": "class Solution {\n    public boolean isValid(String s) {\n        // Write your code here\n        return false;\n    }\n}",
            "cpp": "class Solution {\npublic:\n    bool isValid(string s) {\n        // Write your code here\n        return false;\n    }\n};",
            "c": "bool isValid(char * s) {\n    // Write your code here\n    return false;\n}",
            "r": "isValid <- function(s) {\n  # Write your code here\n  return(FALSE)\n}"
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
            {"input": ["((()))(())"], "output": True}
        ]
    },
    {
        "id": "premium-5",
        "title": "Merge Two Sorted Lists",
        "titleSlug": "merge-two-sorted-lists",
        "description": "<p>You are given the heads of two sorted linked lists <code>list1</code> and <code>list2</code>. Merge the two lists into one <strong>sorted</strong> list.</p>",
        "difficulty": "Easy",
        "tags": ["Linked List", "Recursion"],
        "function_name": "mergeTwoLists",
        "starter_code": {
            "python": "class Solution:\n    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:\n        # Write your code here\n        pass",
            "java": "class Solution {\n    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {\n        // Write your code here\n        return null;\n    }\n}",
            "cpp": "class Solution {\npublic:\n    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {\n        // Write your code here\n        return nullptr;\n    }\n};",
            "c": "struct ListNode* mergeTwoLists(struct ListNode* list1, struct ListNode* list2) {\n    // Write your code here\n    return NULL;\n}",
            "r": "mergeTwoLists <- function(list1, list2) {\n  # Write your code here\n  return(NULL)\n}"
        },
        "test_cases": [
            {"input": [[1,2,4], [1,3,4]], "output": [1,1,2,3,4,4]},
            {"input": [[], []], "output": []},
            {"input": [[], [0]], "output": [0]},
            {"input": [[1], [2]], "output": [1,2]},
            {"input": [[5], [1,2,3,4]], "output": [1,2,3,4,5]},
            {"input": [[1,1,1], [1,1,1]], "output": [1,1,1,1,1,1]},
            {"input": [[-10,-5], [-2,3]], "output": [-10,-5,-2,3]},
            {"input": [[1], []], "output": [1]},
            {"input": [[], [1]], "output": [1]},
            {"input": [[100], [200]], "output": [100,200]},
            {"input": [[1,3,5], [2,4,6]], "output": [1,2,3,4,5,6]},
            {"input": [[1], [0]], "output": [0,1]},
            {"input": [[2], [1]], "output": [1,2]},
            {"input": [[1,1], [2,2]], "output": [1,1,2,2]},
            {"input": [[-1,10], [-20,30]], "output": [-20,-1,10,30]}
        ]
    }
]
