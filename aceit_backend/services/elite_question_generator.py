"""
Elite Question Generator Service

AI-powered question generation engine that creates CAT/XAT/GMAT/GRE/GATE-level
aptitude questions using Google Gemini API with structured prompt engineering.

Features:
- Multi-step reasoning question generation
- Trap-aware option creation
- Solution strategy generation
- Difficulty calibration
- Quality validation
"""

import os
import json
import google.generativeai as genai
from typing import Optional, Dict, List
from services.question_taxonomy import (
    APTITUDE_TAXONOMY,
    DIFFICULTY_CALIBRATION,
    get_concepts,
    get_elite_traps,
    get_difficulty_specs,
    validate_category_subtopic
)


class EliteQuestionGenerator:
    """
    AI-powered elite aptitude question generator
    """
    
    def __init__(self):
        """Initialize Gemini API client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        # Using stable model instead of experimental to avoid quota issues
        self.model = genai.GenerativeModel("models/gemini-1.5-flash")
        
    
    def generate_question(
        self,
        category: str,
        sub_topic: str,
        difficulty_level: str = "Intermediate",
        user_level: Optional[str] = None,
        performance_signals: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Generate an elite-level aptitude question
        
        Args:
            category: Main category (Quantitative, Logical, Verbal, Data Sufficiency)
            sub_topic: Specific sub-topic within category
            difficulty_level: Beginner, Intermediate, Advanced, Elite
            user_level: Optional user tier for personalization
            performance_signals: Optional dict with accuracy_trend, time_trend, error_pattern
        
        Returns:
            Dictionary with question data or None if generation fails
        """
        # Validate inputs
        if not validate_category_subtopic(category, sub_topic):
            print(f"[ERROR] Invalid category/subtopic: {category}/{sub_topic}")
            return None
        
        # Build the prompt
        prompt = self._build_generation_prompt(
            category, sub_topic, difficulty_level, user_level, performance_signals
        )
        
        try:
            print(f"[EliteQGen] Generating {difficulty_level} question for {category}/{sub_topic}...")
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,  # Higher creativity for diverse questions
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )
            
            # Parse response
            question_data = self._parse_response(response.text)
            
            if question_data:
                # Validate quality
                if self.validate_question_quality(question_data):
                    print(f"[EliteQGen] ✅ Question generated successfully")
                    return question_data
                else:
                    print(f"[EliteQGen] ⚠️ Question failed quality validation")
                    return None
            else:
                print(f"[EliteQGen] ❌ Failed to parse response")
                return None
                
        except Exception as e:
            print(f"[EliteQGen ERROR] {e}")
            return None
    
    
    def _build_generation_prompt(
        self,
        category: str,
        sub_topic: str,
        difficulty_level: str,
        user_level: Optional[str],
        performance_signals: Optional[Dict]
    ) -> str:
        """Build structured prompt for question generation"""
        
        # Get taxonomy data
        concepts = get_concepts(category, sub_topic)
        elite_traps = get_elite_traps(category, sub_topic)
        difficulty_specs = get_difficulty_specs(difficulty_level)
        
        # Build performance context
        performance_context = ""
        if performance_signals:
            performance_context = f"""
User Performance Signals:
- Accuracy Trend: {performance_signals.get('accuracy_trend', 'N/A')}
- Time Taken Trend: {performance_signals.get('time_trend', 'N/A')}
- Error Pattern: {performance_signals.get('error_pattern', 'N/A')}
"""
        
        prompt = f"""You are an elite aptitude question architect trained in the standards of CAT, XAT, GMAT, GRE, GATE, and top-tier product company interviews.

Your task is to generate ONE HIGH-INTELLIGENCE aptitude question that is:
1. Conceptually deep (not formula-based)
2. Trap-aware (misleading but fair)
3. Time-efficient (solvable within {difficulty_specs['time_expected_sec']} seconds by a strong candidate)
4. Discriminatory (clearly separates average from top 5% performers)

-------------------------
QUESTION SPECIFICATIONS
-------------------------
Topic Category: {category}
Sub-topic: {sub_topic}
Difficulty Level: {difficulty_level}
Current User Level: {user_level or 'Not specified'}

{performance_context}

-------------------------
DIFFICULTY CALIBRATION
-------------------------
{json.dumps(difficulty_specs, indent=2)}

-------------------------
AVAILABLE CONCEPTS
-------------------------
Primary Concepts: {', '.join(concepts[:5])}
Elite Traps: {', '.join(elite_traps[:3])}

-------------------------
GENERATION RULES
-------------------------
1. Question must involve {difficulty_specs['reasoning_steps']} reasoning steps
2. Use {difficulty_specs['concept_count']} concept(s)
3. Introduce at least ONE {difficulty_specs['trap_level']} trap
4. Use realistic numbers (no toy values like 1, 2, 3)
5. Question must be solvable WITHOUT brute force
6. Create exactly 4 options (A, B, C, D)
7. Make wrong options tempting based on common mistakes

-------------------------
TRAP DESIGN GUIDELINES
-------------------------
- Beginner: Calculation errors, unit confusion
- Intermediate: Conceptual misunderstanding, partial solutions
- Advanced: Hidden assumptions, data sufficiency traps
- Elite: Reverse logic, pattern blindness, overthinking traps

-------------------------
OUTPUT FORMAT (STRICT JSON)
-------------------------
You MUST respond with ONLY a valid JSON object (no markdown, no extra text):

{{
  "question": "Well-structured MCQ question text here",
  "options": [
    "Option A text",
    "Option B text",
    "Option C text",
    "Option D text"
  ],
  "correct_option": 0,
  "difficulty_level": "{difficulty_level}",
  "primary_concepts": ["concept1", "concept2"],
  "trap_explanation": "Explain why wrong options are tempting and what mistakes lead to them",
  "optimal_solution_strategy": "Describe the fastest reasoning path to solve this question",
  "common_mistake": "What average students typically do wrong",
  "time_to_solve_sec": {difficulty_specs['time_expected_sec']},
  "follow_up_logic": {{
      "if_correct": "How to increase complexity for next question",
      "if_wrong": "What remedial concept to focus on"
  }}
}}

-------------------------
QUALITY CHECKLIST
-------------------------
Before finalizing, ensure:
✓ Question is intellectually rewarding
✓ Traps are fair but subtle
✓ Solution exists and is elegant
✓ Numbers are realistic
✓ Options are distinct and plausible
✓ Explanation is clear and educational

Generate the question now. Return ONLY the JSON object, nothing else."""

        return prompt
    
    
    def _parse_response(self, response_text: str) -> Optional[Dict]:
        """Parse LLM response and extract JSON"""
        try:
            # Remove markdown code blocks if present
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            # Parse JSON
            question_data = json.loads(cleaned)
            
            # Validate required fields
            required_fields = [
                "question", "options", "correct_option", "difficulty_level",
                "primary_concepts", "trap_explanation", "optimal_solution_strategy",
                "common_mistake", "time_to_solve_sec", "follow_up_logic"
            ]
            
            for field in required_fields:
                if field not in question_data:
                    print(f"[Parse Error] Missing required field: {field}")
                    return None
            
            return question_data
            
        except json.JSONDecodeError as e:
            print(f"[Parse Error] Invalid JSON: {e}")
            print(f"Response text: {response_text[:200]}...")
            return None
        except Exception as e:
            print(f"[Parse Error] {e}")
            return None
    
    
    def validate_question_quality(self, question_data: Dict) -> bool:
        """
        Validate generated question meets quality standards
        
        Quality checks:
        - Question text is substantial (>50 chars)
        - Exactly 4 options
        - Correct option index is valid (0-3)
        - All required fields are non-empty
        - Time to solve is reasonable (30-300 seconds)
        """
        try:
            # Check question text
            if len(question_data.get("question", "")) < 50:
                print("[Quality] Question text too short")
                return False
            
            # Check options
            options = question_data.get("options", [])
            if len(options) != 4:
                print(f"[Quality] Expected 4 options, got {len(options)}")
                return False
            
            # Check all options are non-empty
            if any(len(opt.strip()) < 1 for opt in options):
                print("[Quality] Empty option detected")
                return False
            
            # Check correct option
            correct_idx = question_data.get("correct_option")
            if not isinstance(correct_idx, int) or correct_idx not in [0, 1, 2, 3]:
                print(f"[Quality] Invalid correct_option: {correct_idx}")
                return False
            
            # Check time to solve
            time_sec = question_data.get("time_to_solve_sec", 0)
            if not (30 <= time_sec <= 300):
                print(f"[Quality] Unreasonable time_to_solve_sec: {time_sec}")
                return False
            
            # Check primary concepts
            concepts = question_data.get("primary_concepts", [])
            if not concepts or len(concepts) < 1:
                print("[Quality] No primary concepts specified")
                return False
            
            # Check explanations are substantial
            if len(question_data.get("trap_explanation", "")) < 20:
                print("[Quality] Trap explanation too short")
                return False
            
            if len(question_data.get("optimal_solution_strategy", "")) < 20:
                print("[Quality] Solution strategy too short")
                return False
            
            return True
            
        except Exception as e:
            print(f"[Quality Check Error] {e}")
            return False
    
    
    def calibrate_difficulty(
        self,
        question_data: Dict,
        target_level: str,
        adjustment_reason: str = ""
    ) -> Dict:
        """
        Adjust question difficulty based on user performance
        
        This can be used to fine-tune difficulty after initial generation
        """
        # This is a placeholder for future enhancement
        # Could regenerate with adjusted parameters or modify existing question
        
        print(f"[Calibration] Adjusting to {target_level}: {adjustment_reason}")
        question_data["difficulty_level"] = target_level
        question_data["calibration_note"] = adjustment_reason
        
        return question_data
    
    
    def generate_batch(
        self,
        category: str,
        sub_topic: str,
        difficulty_level: str,
        count: int = 5,
        user_level: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate multiple questions in batch
        
        Args:
            category: Main category
            sub_topic: Specific sub-topic
            difficulty_level: Target difficulty
            count: Number of questions to generate
            user_level: Optional user tier
        
        Returns:
            List of generated questions
        """
        questions = []
        
        for i in range(count):
            print(f"\n[Batch Generation] Question {i+1}/{count}")
            question = self.generate_question(
                category=category,
                sub_topic=sub_topic,
                difficulty_level=difficulty_level,
                user_level=user_level
            )
            
            if question:
                questions.append(question)
            else:
                print(f"[Batch] Failed to generate question {i+1}")
        
        print(f"\n[Batch Complete] Generated {len(questions)}/{count} questions")
        return questions


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def test_generation():
    """Test question generation with sample parameters"""
    try:
        generator = EliteQuestionGenerator()
        
        # Test cases
        test_cases = [
            {
                "category": "Quantitative",
                "sub_topic": "Probability",
                "difficulty_level": "Advanced",
                "user_level": "advanced"
            },
            {
                "category": "Logical",
                "sub_topic": "Seating Arrangements",
                "difficulty_level": "Intermediate",
                "user_level": "competent"
            },
            {
                "category": "Verbal",
                "sub_topic": "Critical Reasoning",
                "difficulty_level": "Elite",
                "user_level": "elite"
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\n{'='*60}")
            print(f"TEST CASE {i}")
            print(f"{'='*60}")
            
            question = generator.generate_question(**test)
            
            if question:
                print(f"\n✅ Question Generated:")
                print(f"Q: {question['question'][:100]}...")
                print(f"Options: {len(question['options'])}")
                print(f"Correct: {question['correct_option']}")
                print(f"Concepts: {', '.join(question['primary_concepts'])}")
            else:
                print(f"\n❌ Generation failed")
        
    except Exception as e:
        print(f"[Test Error] {e}")


if __name__ == "__main__":
    # Run test when executed directly
    test_generation()
