"""
Test Script for Elite Question Generator

Tests the AI-powered question generation system with various categories and difficulty levels.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from services.elite_question_generator import EliteQuestionGenerator
from services.question_taxonomy import APTITUDE_TAXONOMY, get_subtopics
import json


def test_single_question():
    """Test generating a single question"""
    print("\n" + "="*70)
    print("TEST 1: Single Question Generation")
    print("="*70)
    
    try:
        generator = EliteQuestionGenerator()
        
        # Test case: Advanced Probability question
        question = generator.generate_question(
            category="Quantitative",
            sub_topic="Probability",
            difficulty_level="Hard",
            user_level="advanced",
            performance_signals={
                "accuracy_trend": "high",
                "time_trend": "normal",
                "error_pattern": "trap_susceptibility"
            }
        )
        
        if question:
            print("\n✅ Question Generated Successfully!\n")
            print(f"Question: {question['question']}\n")
            print("Options:")
            for i, opt in enumerate(question['options']):
                marker = "✓" if i == question['correct_option'] else " "
                print(f"  [{marker}] {chr(65+i)}. {opt}")
            
            print(f"\nDifficulty: {question['difficulty_level']}")
            print(f"Concepts: {', '.join(question['primary_concepts'])}")
            print(f"Expected Time: {question['time_to_solve_sec']} seconds")
            print(f"\nTrap Explanation: {question['trap_explanation'][:150]}...")
            print(f"\nOptimal Strategy: {question['optimal_solution_strategy'][:150]}...")
            
            return True
        else:
            print("\n❌ Question generation failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_multiple_categories():
    """Test generating questions across different categories"""
    print("\n" + "="*70)
    print("TEST 2: Multiple Categories")
    print("="*70)
    
    test_cases = [
        {
            "category": "Quantitative",
            "sub_topic": "Number Systems",
            "difficulty_level": "Medium"
        },
        {
            "category": "Logical",
            "sub_topic": "Seating Arrangements",
            "difficulty_level": "Hard"
        },
        {
            "category": "Verbal",
            "sub_topic": "Critical Reasoning",
            "difficulty_level": "Hard"
        }
    ]
    
    generator = EliteQuestionGenerator()
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] Generating {test['category']} - {test['sub_topic']} ({test['difficulty_level']})...")
        
        try:
            question = generator.generate_question(**test)
            
            if question:
                print(f"  ✅ Success!")
                print(f"     Question: {question['question'][:80]}...")
                print(f"     Concepts: {', '.join(question['primary_concepts'][:2])}")
                results.append(True)
            else:
                print(f"  ❌ Failed")
                results.append(False)
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append(False)
    
    success_rate = (sum(results) / len(results)) * 100
    print(f"\n📊 Success Rate: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return success_rate >= 66  # At least 2/3 should succeed


def test_difficulty_progression():
    """Test question generation across difficulty levels"""
    print("\n" + "="*70)
    print("TEST 3: Difficulty Progression")
    print("="*70)
    
    difficulties = ["Easy", "Medium", "Hard"]
    generator = EliteQuestionGenerator()
    
    for difficulty in difficulties:
        print(f"\n[{difficulty}] Generating question...")
        
        try:
            question = generator.generate_question(
                category="Quantitative",
                sub_topic="Percentages & Ratios",
                difficulty_level=difficulty
            )
            
            if question:
                print(f"  ✅ Generated")
                print(f"     Concepts: {len(question['primary_concepts'])} concept(s)")
                print(f"     Time: {question['time_to_solve_sec']}s")
                print(f"     Question length: {len(question['question'])} chars")
                # Check for Scenario
                if len(question['question']) > 50 and "find" not in question['question'].lower()[:20]:
                     print("     ✅ Scenario detected")
            else:
                print(f"  ❌ Failed")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:100]}")
    
    return True


def test_batch_generation():
    """Test batch question generation"""
    print("\n" + "="*70)
    print("TEST 4: Batch Generation")
    print("="*70)
    
    try:
        generator = EliteQuestionGenerator()
        
        print("\nGenerating batch of 3 questions...")
        questions = generator.generate_batch(
            category="Quantitative",
            sub_topic="Time & Work",
            difficulty_level="Medium",
            count=3
        )
        
        print(f"\n✅ Generated {len(questions)}/3 questions")
        
        for i, q in enumerate(questions, 1):
            print(f"\n  Question {i}:")
            print(f"    - {q['question'][:60]}...")
            print(f"    - Difficulty: {q['difficulty_level']}")
            print(f"    - Concepts: {', '.join(q['primary_concepts'][:2])}")
        
        return len(questions) >= 2  # At least 2/3 should succeed
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_quality_validation():
    """Test question quality validation"""
    print("\n" + "="*70)
    print("TEST 5: Quality Validation")
    print("="*70)
    
    generator = EliteQuestionGenerator()
    
    # Test valid question
    valid_question = {
        "question": "A train travels at 60 km/h for the first half of the journey and 40 km/h for the second half. What is the average speed?",
        "options": ["50 km/h", "48 km/h", "45 km/h", "52 km/h"],
        "correct_option": 1,
        "difficulty_level": "Medium",
        "primary_concepts": ["average_speed", "harmonic_mean"],
        "trap_explanation": "Option A is tempting as arithmetic mean",
        "optimal_solution_strategy": "Use harmonic mean formula for average speed",
        "common_mistake": "Taking arithmetic mean instead of harmonic mean",
        "time_to_solve_sec": 90,
        "follow_up_logic": {"if_correct": "increase", "if_wrong": "review"}
    }
    
    # Test invalid question (too short)
    invalid_question = {
        "question": "What is 2+2?",
        "options": ["3", "4", "5", "6"],
        "correct_option": 1,
        "difficulty_level": "Easy",
        "primary_concepts": [],
        "trap_explanation": "Too short",
        "optimal_solution_strategy": "Add",
        "common_mistake": "None",
        "time_to_solve_sec": 10,
        "follow_up_logic": {}
    }
    
    print("\nTesting valid question...")
    if generator.validate_question_quality(valid_question):
        print("  ✅ Valid question passed validation")
    else:
        print("  ❌ Valid question failed validation")
    
    print("\nTesting invalid question...")
    if not generator.validate_question_quality(invalid_question):
        print("  ✅ Invalid question correctly rejected")
    else:
        print("  ❌ Invalid question incorrectly accepted")
    
    return True


def test_taxonomy():
    """Test question taxonomy"""
    print("\n" + "="*70)
    print("TEST 6: Question Taxonomy")
    print("="*70)
    
    print("\nAvailable Categories:")
    for category in APTITUDE_TAXONOMY.keys():
        subtopics = get_subtopics(category)
        print(f"  • {category}: {len(subtopics)} subtopics")
        print(f"    - {', '.join(subtopics[:3])}...")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("ELITE QUESTION GENERATOR - TEST SUITE")
    print("="*70)
    
    # Check API key
    if not os.getenv("GEMINI_API_KEY"):
        print("\n❌ GEMINI_API_KEY not found in environment!")
        print("Please set GEMINI_API_KEY in your .env file")
        return
    
    print(f"\n✓ GEMINI_API_KEY found")
    
    tests = [
        ("Taxonomy", test_taxonomy),
        ("Quality Validation", test_quality_validation),
        ("Single Question", test_single_question),
        ("Multiple Categories", test_multiple_categories),
        ("Difficulty Progression", test_difficulty_progression),
        ("Batch Generation", test_batch_generation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Elite question generator is ready.")
    elif passed >= total * 0.7:
        print("\n⚠️  Most tests passed. System is functional but needs refinement.")
    else:
        print("\n❌ Multiple tests failed. Please review the errors above.")


if __name__ == "__main__":
    run_all_tests()
