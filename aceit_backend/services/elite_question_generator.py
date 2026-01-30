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
        # Using stable model
        self.model = genai.GenerativeModel("models/gemini-2.0-flash")
        
    
    def generate_question(
        self,
        category: str,
        sub_topic: str,
        difficulty_level: str = "Medium",
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
                    temperature=0.9,
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
            
        # Placement Exam Context mapping
        exam_context_map = {
            "Easy": "Warm-up / confidence builders. Direct formula application.",
            "Medium": "Cutoff & shortlisting level. Concept selection + logical reasoning.",
            "Hard": "Top 10-20% filtering. Multi-step logic, traps, and real-test complexity."
        }
        exam_context = exam_context_map.get(difficulty_level, "Standard aptitude test")
        
        prompt = f"""You are an elite aptitude question architect for top-tier placement exams (Google, Amazon, TCS Digital, etc) and competitive exams (CAT, GMAT).

Your task is to generate ONE HIGH-QUALITY "SCENARIO-BASED" aptitude question.

-------------------------
STRICT SCENARIO REQUIREMENT
-------------------------
Every question MUST be wrapped in a realistic short story or scenario.
DO NOT ask: "Find the compound interest on $5000..."
INSTEAD ask: "TechCorp invests a surplus of $5.2M in a high-yield bond..." or "Alice is organizing a hackathon..."

Use diverse contexts:
- Business (Profit/Loss, percentages)
- Engineering (Time/Work, manufacturing)
- Daily Life (Travel, shopping)
- Abstract Logic (Puzzle scenarios)

-------------------------
QUESTION SPECIFICATIONS
-------------------------
Topic Category: {category}
Sub-topic: {sub_topic}
Difficulty Level: {difficulty_level}
Exam Context: {exam_context}

-------------------------
DIFFICULTY CALIBRATION (STRICT)
-------------------------
{json.dumps(difficulty_specs, indent=2)}

-------------------------
AVAILABLE CONCEPTS
-------------------------
Primary Concepts: {', '.join(concepts[:6])}
Elite Traps: {', '.join(elite_traps[:4])}

-------------------------
GENERATION RULES
-------------------------
1. **Scenario-Based**: Start with a 1-2 sentence context.
2. **Difficulty Compliance**:
   - Easy: Direct application, but still in a scenario.
   - Medium: Combinations of 2 concepts. subtle traps.
   - Hard: Hidden constraints, reverse reasoning.
3. **Diverse Formats**: Do not just use "Solve for X". vary the style:
   - "Find the odd one out" (in context)
   - "Statement I vs Statement II sufficiency"
   - "Match the following" logic
4. **Options**: 4 distinct options. Wrong options must be "tempting" (based on common errors).
5. **No Toy Numbers**: Use realistic figures (e.g., $12,450 instead of $100), unless integer logic is the core concept.

-------------------------
OUTPUT FORMAT (STRICT JSON)
-------------------------
You MUST respond with ONLY a valid JSON object:

{{
  "question": "The full question text including the scenario and the specific question asked.",
  "options": [
    "Option A",
    "Option B",
    "Option C",
    "Option D"
  ],
  "correct_option": 0,
  "difficulty_level": "{difficulty_level}",
  "primary_concepts": ["concept1", "concept2"],
  "trap_explanation": "Explain why wrong options are tempting",
  "optimal_solution_strategy": "Step-by-step reasoning for the fastest solution",
  "common_mistake": "What average students typically do wrong",
  "time_to_solve_sec": {difficulty_specs['time_expected_sec']},
  "follow_up_logic": {{
      "if_correct": "How to increase complexity",
      "if_wrong": "Remedial concept"
  }}
}}

Generate the question now. Return ONLY the JSON object."""

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
            
            # --- SHUFFLING LOGIC start ---
            # Shuffle options to ensure randomness even if LLM generates strictly ordered options
            import random
            options = question_data["options"]
            correct_idx = question_data["correct_option"]
            
            if 0 <= correct_idx < len(options):
                correct_answer_text = options[correct_idx]
                random.shuffle(options)
                
                # Find new index of the correct answer
                new_correct_idx = options.index(correct_answer_text)
                
                # Update data
                question_data["options"] = options
                question_data["correct_option"] = new_correct_idx
                print(f"[EliteQGen] Shuffled options. New correct index: {new_correct_idx}")
            else:
                print(f"[EliteQGen] Warning: Invalid correct_option index {correct_idx} from LLM")
            # --- SHUFFLING LOGIC end ---
            
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
