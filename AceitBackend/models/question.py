from pydantic import BaseModel
from typing import List, Optional

# This defines what an aptitude question looks like
class AptitudeQuestion(BaseModel):
    id: str
    question: str
    options: List[str]  # List of answer choices
    correct_answer: int  # Index of correct option (0, 1, 2, 3)
    explanation: str  # Explanation of the answer
    topic: str  # quantitative, logical, verbal
    difficulty: str  # easy, medium, hard
    source: Optional[str] = None

# This defines what a coding problem looks like  
class CodingProblem(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str  # easy, medium, hard
    test_cases: List[dict]  # Input-output test cases
    starter_code: str  # Initial code template for user
    source: Optional[str] = None