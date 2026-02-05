# COMPLETE PROBLEM TEMPLATE EXAMPLE

Here's a complete example from the existing "Two Sum" problem in the database.
Use this as a reference when adding new problems.

---

## PROBLEM STRUCTURE

```python
{
    # ============ REQUIRED FIELDS ============
    
    "id": "premium-1",  # Unique ID (auto-generated if you don't provide)
    
    "title": "Two Sum",  # Problem name
    
    "titleSlug": "two-sum",  # URL-friendly slug (auto-generated from title)
    
    "difficulty": "Easy",  # Must be: "Easy", "Medium", or "Hard"
    
    "function_name": "twoSum",  # The main function name to call
    
    # ============ DESCRIPTION (HTML format) ============
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
    
    # ============ TAGS (Array of strings) ============
    "tags": ["Arrays", "Hash Table"],
    
    # ============ TEST CASES (15 recommended) ============
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
    
    # ============ STARTER CODE (All 5 languages) ============
    "starter_code": {
        "python": """class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Write your code here
        pass
""",
        
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
};""",
        
        "c": """int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    // Write your code here
    *returnSize = 0;
    return NULL;
}""",
        
        "r": """twoSum <- function(nums, target) {
    # Write your code here
    return(c())
}"""
    },
    
    # ============ SOLUTION (Optional, for reference) ============
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
}
```

---

## SIMPLIFIED FORMAT (Just provide these, I'll generate the rest)

When you give me a new problem, you can use this simple format:

```
Title: Find Peak Element
Difficulty: Medium
Function Name: findPeakElement
Tags: Array, Binary Search

Description:
A peak element is an element that is strictly greater than its neighbors.
Given an array nums, find a peak element and return its index.
You may imagine that nums[-1] = nums[n] = -∞.

Example 1:
Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 is a peak element.

Example 2:
Input: nums = [1,2,1,3,5,6,4]
Output: 5
Explanation: 5 is a peak element.

Constraints:
- 1 <= nums.length <= 1000
- -2^31 <= nums[i] <= 2^31 - 1

Test Cases:
1. Input: [1,2,3,1], Output: 2
2. Input: [1,2,1,3,5,6,4], Output: 5
3. Input: [1], Output: 0
4. Input: [1,2], Output: 1
5. Input: [2,1], Output: 0
... (provide at least 15 test cases)
```

I will automatically:
- Generate unique ID
- Format description as HTML
- Create starter code for all 5 languages
- Structure it correctly for database insertion

---

## NOTES:

1. **Test Cases Format**:
   - For single argument: `{"input": [arg1], "output": result}`
   - For multiple arguments: `{"input": [arg1, arg2, arg3], "output": result}`
   - For boolean outputs: use `true` or `false` (lowercase)
   - For arrays: use `[1, 2, 3]` format

2. **HTML Description Tips**:
   - Use `<p>` for paragraphs
   - Use `<code>` for inline code
   - Use `<pre>` for code blocks
   - Use `<strong>` for bold
   - Use `<em>` for italics
   - Use `<ul>` and `<li>` for lists
   - Use `<sup>` for superscripts (like 10^4)

3. **Function Signatures**:
   - Python: Class-based with `self`
   - Java: Class-based with types
   - C++: Class-based with vectors
   - C: Standalone with pointers
   - R: Standalone function

Ready to add new problems! Just provide the basics and I'll handle the formatting. 🚀
