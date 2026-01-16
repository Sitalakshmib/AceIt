import requests
import logging

LEETCODE_API_URL = "https://alfa-leetcode-api.onrender.com"
logger = logging.getLogger(__name__)

def get_leetcode_problems(limit=20):
    """
    Fetch a list of coding problems
    """
    try:
        # Check 'daily' or 'problems' endpoint
        response = requests.get(f"{LEETCODE_API_URL}/problemset-question-list?limit={limit}")
        if response.status_code == 200:
            data = response.json()
            questions = data.get('questions', [])
            return questions
        return []
    except Exception as e:
        logger.error(f"Error fetching LeetCode problems: {e}")
        return []

def get_problem_details(title_slug):
    """
    Fetch specific problem details including description
    """
    try:
        response = requests.get(f"{LEETCODE_API_URL}/select?titleSlug={title_slug}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Error fetching problem details: {e}")
        return None
