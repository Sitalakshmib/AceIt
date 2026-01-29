from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database_postgres import get_db
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from models.analytics_sql import QuestionAttempt
from services.adaptive_engine import AdaptiveEngine, get_or_create_progress
from typing import Optional, List
import random
import datetime

router = APIRouter()

# --- HELPER FUNCTIONS ---

def calculate_next_difficulty(progress: UserAptitudeProgress) -> str:
    """
    Adaptive Algorithm:
    - If accuracy > 80% at current level -> Level Up
    - If accuracy < 50% at current level -> Level Down (if not easy)
    - Otherwise -> Stay
    """
    current_diff = progress.current_difficulty
    
    if current_diff == "easy":
        total = progress.easy_total
        correct = progress.easy_correct
    elif current_diff == "medium":
        total = progress.medium_total
        correct = progress.medium_correct
    else: # hard
        total = progress.hard_total
        correct = progress.hard_correct
        
    if total < 3: # Need minimum 3 attempts to judge
        return current_diff
        
    accuracy = correct / total
    
    if accuracy >= 0.8: # > 80% Success
        if current_diff == "easy": return "medium"
        if current_diff == "medium": return "hard"
        
    if accuracy < 0.5: # < 50% Success
        if current_diff == "hard": return "medium"
        if current_diff == "medium": return "easy"
        
    return current_diff

def format_questions(questions, include_explanations=False):
    """Format SQL objects to JSON response with RUNTIME SHUFFLING"""
    formatted = []
    for q in questions:
        # Runtime Shuffle Logic
        # Create a copy of options to shuffle
        shuffled_options = list(q.options) if q.options else []
        original_correct_idx = q.correct_answer
        new_correct_idx = 0
        
        if shuffled_options and 0 <= original_correct_idx < len(shuffled_options):
            correct_text = shuffled_options[original_correct_idx]
            random.shuffle(shuffled_options)
            new_correct_idx = shuffled_options.index(correct_text)
        
        item = {
            "id": q.id,
            "question": q.question,
            "options": shuffled_options,
            "correct_answer": new_correct_idx, # Updated index for shuffled options
            "type": q.topic,
            "topic": q.topic,
            "category": q.category,
            "difficulty": q.difficulty,
            "image_url": q.image_url
        }
        if include_explanations:
            item["explanation"] = q.answer_explanation
        formatted.append(item)
    return formatted

# --- ENDPOINTS ---

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get available aptitude categories and topics"""
    # Group topics by category and sort them
    results = db.query(AptitudeQuestion.category, AptitudeQuestion.topic).distinct().all()
    
    categories_raw = {}
    for cat, topic in results:
        if cat not in categories_raw:
            categories_raw[cat] = []
        if topic not in categories_raw[cat]:
            categories_raw[cat].append(topic)
            
    # Sort categories and topics within them
    sorted_categories = {}
    for cat in sorted(categories_raw.keys()):
        sorted_categories[cat] = sorted(categories_raw[cat])
            
    return {"categories": sorted_categories}

@router.get("/questions")
async def get_aptitude_questions(
    user_id: Optional[str] = None, 
    topic: Optional[str] = None, 
    category: Optional[str] = None,
    count: int = 10, 
    include_explanations: bool = False,
    db: Session = Depends(get_db)
):
    """Get adaptive aptitude questions based on user proficiency"""
    
    # 1. Determine Difficulty
    target_difficulty = "easy" # Default
    
    if user_id and topic:
        # Check existing progress to find correct difficulty
        # We need the category to create progress if missing. Query one question to find category if not provided
        if not category:
            q_sample = db.query(AptitudeQuestion).filter(AptitudeQuestion.topic == topic).first()
            category = q_sample.category if q_sample else "General"
            
        progress = get_or_create_progress(db, user_id, topic, category)
        target_difficulty = progress.current_difficulty
        
    # 2. Query Questions
    query = db.query(AptitudeQuestion)
    
    if topic:
        query = query.filter(AptitudeQuestion.topic == topic)
    if category:
        query = query.filter(AptitudeQuestion.category == category)
        
    # Try to get questions of target difficulty
    preferred_query = query.filter(AptitudeQuestion.difficulty == target_difficulty)
    questions = preferred_query.limit(count * 2).all() # Get pool
    
    # If not enough, fallback to any difficulty
    if len(questions) < count:
        questions = query.limit(count * 2).all()
        
    # 3. Randomize Selection
    if not questions:
        return []
        
    selected_questions = random.sample(questions, min(len(questions), count))
    
    return format_questions(selected_questions, include_explanations)

@router.post("/submit")
async def submit_answers(payload: dict, db: Session = Depends(get_db)):
    """
    Submit user answers, calculate score, and update adaptive progress
    """
    try:
        user_id = payload.get("user_id")
        user_answers = payload.get("answers", {}) # {question_id: selected_index}
        
        if not user_answers:
            return {"message": "No answers provided", "correct": 0, "total": 0, "percentage": 0, "results": []}

        score = 0
        total = len(user_answers)
        results = []
        
        # Fetch all questions at once
        question_ids = list(user_answers.keys())
        questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(question_ids)).all()
        questions_map = {q.id: q for q in questions}
        
        # Process each answer
        for q_id, user_ans_idx in user_answers.items():
            question = questions_map.get(q_id)
            if not question: 
                continue
                
            is_correct = (question.correct_answer == user_ans_idx)
            if is_correct: 
                score += 1
                
            results.append({
                "question_id": q_id,
                "correct": is_correct,
                "topic": question.topic,
                "category": question.category,
                "difficulty": question.difficulty
            })
            
            # Adaptive Update (if user logged in)
            if user_id:
                progress = get_or_create_progress(db, user_id, question.topic, question.category)
                
                # Only update if progress was successfully created
                if progress:
                    # Update counters
                    progress.questions_attempted += 1
                    if is_correct:
                        progress.questions_correct += 1
                        progress.streak += 1
                    else:
                        progress.streak = 0
                        
                    # Update difficulty specific counters
                    if question.difficulty == "easy":
                        progress.easy_total += 1
                        if is_correct: progress.easy_correct += 1
                    elif question.difficulty == "medium":
                        progress.medium_total += 1
                        if is_correct: progress.medium_correct += 1
                    elif question.difficulty == "hard":
                        progress.hard_total += 1
                        if is_correct: progress.hard_correct += 1
                    
                    # Recalculate accuracies
                    if progress.questions_attempted > 0:
                        progress.overall_accuracy = (progress.questions_correct / progress.questions_attempted) * 100
                    
                    # Recent accuracy (last 10)
                    recent_attempts = db.query(QuestionAttempt)\
                        .filter(
                            QuestionAttempt.user_id == user_id,
                            QuestionAttempt.topic == question.topic,
                            QuestionAttempt.context == "practice"
                        )\
                        .order_by(QuestionAttempt.attempted_at.desc())\
                        .limit(10).all()
                    
                    if recent_attempts:
                        recent_correct = sum(1 for a in recent_attempts if a.is_correct)
                        progress.recent_accuracy = (recent_correct / len(recent_attempts)) * 100

                    # Recalculate difficulty for next time
                    progress.current_difficulty = calculate_next_difficulty(progress)
                    progress.last_practiced = datetime.datetime.utcnow()
                
        if user_id:
            db.commit()
            
        percentage = (score / total) * 100 if total > 0 else 0
        return {
            "correct": score,
            "total": total,
            "percentage": round(percentage, 2),
            "results": results
        }
    except Exception as e:
        print(f"[ERROR] Aptitude submit failed: {e}")
        return {
            "correct": 0,
            "total": 0,
            "percentage": 0,
            "results": [],
            "error": str(e)
        }

@router.post("/detailed-results")
async def get_detailed_results(payload: dict, db: Session = Depends(get_db)):
    """Get detailed results with explanations for answered questions"""
    user_answers = payload.get("answers", {})
    
    if not user_answers:
        return []
    
    question_ids = list(user_answers.keys())
    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(question_ids)).all()
    questions_map = {q.id: q for q in questions}
    
    results = []
    for q_id, user_ans_idx in user_answers.items():
        question = questions_map.get(q_id)
        if not question:
            continue
            
        is_correct = (question.correct_answer == user_ans_idx)
        results.append({
            "question_id": q_id,
            "question": question.question,
            "options": question.options,
            "user_answer": user_ans_idx,
            "correct_answer": question.correct_answer,
            "correct": is_correct,
            "explanation": question.answer_explanation,
            "topic": question.topic,
            "category": question.category,
            "difficulty": question.difficulty
        })
    
    return results

@router.get("/proficiency/{user_id}")
async def get_user_proficiency(user_id: str, db: Session = Depends(get_db)):
    """Get user's progress via SQL"""
    progress_records = db.query(UserAptitudeProgress).filter(UserAptitudeProgress.user_id == user_id).all()
    
    raw_data = {}
    for p in progress_records:
        if p.category not in raw_data:
            raw_data[p.category] = {}
        raw_data[p.category][p.topic] = {
            "level": p.current_difficulty,
            "accuracy": f"{(p.questions_correct / p.questions_attempted * 100):.1f}%" if p.questions_attempted > 0 else "0%",
            "total_solved": p.questions_correct
        }
    
    # Sort categories and topics alphabetically
    sorted_data = {}
    for cat in sorted(raw_data.keys()):
        sorted_data[cat] = {}
        for topic in sorted(raw_data[cat].keys()):
            sorted_data[cat][topic] = raw_data[cat][topic]
        
    return {"user_id": user_id, "proficiency": sorted_data}


# ========== PRACTICE MODE ENDPOINTS (IndiaBIX Style) ==========

@router.get("/practice/next-question")
async def get_next_practice_question(
    user_id: str,
    category: str,
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get next unattempted question for practice mode.
    IndiaBIX style: One question at a time, no repetition.
    """
    from services.practice_service import PracticeService
    
    try:
        question = PracticeService.get_next_question(db, user_id, category, topic)
        
        if not question:
            return {
                "has_more_questions": False,
                "message": "You've completed all available questions in this topic! Great job!"
            }
        
        return {
            "has_more_questions": True,
            **question
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get next question: {str(e)}")


@router.post("/practice/submit-answer")
async def submit_practice_answer(payload: dict, db: Session = Depends(get_db)):
    """
    Submit answer and get instant feedback with explanation.
    IndiaBIX style: Immediate correctness, explanation, and adaptive feedback.
    """
    from services.practice_service import PracticeService
    
    user_id = payload.get("user_id")
    question_id = payload.get("question_id")
    user_answer = payload.get("user_answer")
    time_spent = payload.get("time_spent", 0)
    shuffled_options = payload.get("shuffled_options")  # Frontend sends the options it displayed
    
    if not all([user_id, question_id is not None, user_answer is not None]):
        raise HTTPException(
            status_code=400,
            detail="user_id, question_id, and user_answer are required"
        )
    
    try:
        feedback = PracticeService.submit_answer(
            db, user_id, question_id, user_answer, time_spent, shuffled_options
        )
        return feedback
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")


# ========== ELITE ADAPTIVE APTITUDE ENDPOINTS ==========

@router.post("/elite/generate-question")
async def generate_elite_question(payload: dict, db: Session = Depends(get_db)):
    """
    Generate AI-powered elite question based on user profile
    
    Request:
    {
        "user_id": "user123",
        "category": "Quantitative",
        "sub_topic": "Probability",
        "force_regenerate": false
    }
    
    Response:
    {
        "question_id": "generated_uuid",
        "question": "...",
        "options": ["A", "B", "C", "D"],
        "difficulty_level": "Advanced",
        "primary_concepts": ["conditional_probability", "complement_rule"],
        "time_to_solve_sec": 120,
        "metadata": {...}
    }
    """
    from services.elite_question_generator import EliteQuestionGenerator
    import uuid
    import json
    
    try:
        user_id = payload.get("user_id")
        category = payload.get("category")
        sub_topic = payload.get("sub_topic")
        force_regenerate = payload.get("force_regenerate", False)
        
        if not all([user_id, category, sub_topic]):
            raise HTTPException(
                status_code=400,
                detail="user_id, category, and sub_topic are required"
            )
        
        # Get user's adaptive profile
        adaptive_profile = AdaptiveEngine.calculate_multidimensional_difficulty(
            db, user_id, sub_topic, category
        )
        
        # Get performance signals
        performance_signals = AdaptiveEngine.get_performance_signals(
            db, user_id, sub_topic
        )
        
        # Generate question
        generator = EliteQuestionGenerator()
        question_data = generator.generate_question(
            category=category,
            sub_topic=sub_topic,
            difficulty_level=adaptive_profile["difficulty_level"],
            user_level=adaptive_profile.get("user_tier"),
            performance_signals=performance_signals
        )
        
        if not question_data:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate question. Please try again."
            )
        
        # Store in database
        question_id = str(uuid.uuid4())
        new_question = AptitudeQuestion(
            id=question_id,
            question=question_data["question"],
            options=question_data["options"],
            correct_answer=question_data["correct_option"],
            answer_explanation=question_data.get("optimal_solution_strategy", ""),
            topic=sub_topic,
            category=category,
            difficulty=question_data["difficulty_level"],
            source="ai_generated",
            # Elite metadata
            primary_concepts=question_data.get("primary_concepts", []),
            trap_explanation=question_data.get("trap_explanation"),
            optimal_solution_strategy=question_data.get("optimal_solution_strategy"),
            common_mistake=question_data.get("common_mistake"),
            time_to_solve_sec=question_data.get("time_to_solve_sec", 120),
            concept_depth=adaptive_profile.get("concept_depth", "single"),
            cognitive_load=adaptive_profile.get("cognitive_load", "low"),
            trap_density=adaptive_profile.get("trap_density", "low"),
            follow_up_logic=json.dumps(question_data.get("follow_up_logic", {}))
        )
        
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        
        return {
            "question_id": question_id,
            "question": question_data["question"],
            "options": question_data["options"],
            "difficulty_level": question_data["difficulty_level"],
            "primary_concepts": question_data.get("primary_concepts", []),
            "time_to_solve_sec": question_data.get("time_to_solve_sec", 120),
            "metadata": {
                "trap_explanation": question_data.get("trap_explanation"),
                "optimal_strategy": question_data.get("optimal_solution_strategy"),
                "common_mistake": question_data.get("common_mistake"),
                "concept_depth": adaptive_profile.get("concept_depth"),
                "cognitive_load": adaptive_profile.get("cognitive_load"),
                "trap_density": adaptive_profile.get("trap_density")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Elite question generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/elite/adaptive-profile/{user_id}")
async def get_adaptive_profile(
    user_id: str,
    topic: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get user's multi-dimensional adaptive profile
    
    Response:
    {
        "user_tier": "advanced",
        "overall_stats": {...},
        "topic_profiles": {...},
        "strengths": ["Number Systems", "Probability"],
        "weaknesses": ["Seating Arrangements"],
        "error_patterns": {...},
        "recommended_focus": {...}
    }
    """
    try:
        # Get all progress records for user
        progress_records = db.query(UserAptitudeProgress).filter(
            UserAptitudeProgress.user_id == user_id
        ).all()
        
        if not progress_records:
            return {
                "user_tier": "developing",
                "overall_stats": {},
                "topic_profiles": {},
                "message": "No practice history found. Start practicing to build your profile!"
            }
        
        # Calculate overall stats
        total_attempted = sum(p.questions_attempted for p in progress_records)
        total_correct = sum(p.questions_correct for p in progress_records)
        overall_accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
        
        # Calculate average time ratio
        avg_times = [p.average_time_per_question for p in progress_records if p.average_time_per_question > 0]
        avg_time_ratio = (sum(avg_times) / len(avg_times) / 120) if avg_times else 1.0
        
        # Classify user tier
        from services.question_taxonomy import classify_user_tier
        user_tier = classify_user_tier(overall_accuracy, avg_time_ratio)
        
        # Build topic profiles
        topic_profiles = {}
        for p in progress_records:
            topic_accuracy = (p.questions_correct / p.questions_attempted * 100) if p.questions_attempted > 0 else 0
            topic_profiles[p.topic] = {
                "category": p.category,
                "difficulty_level": p.current_difficulty,
                "accuracy": round(topic_accuracy, 2),
                "questions_attempted": p.questions_attempted,
                "user_tier": p.user_tier,
                "concept_depth": p.current_concept_depth,
                "cognitive_load": p.current_cognitive_load,
                "trap_density": p.current_trap_density
            }
        
        # Identify strengths and weaknesses
        sorted_topics = sorted(
            topic_profiles.items(),
            key=lambda x: x[1]["accuracy"],
            reverse=True
        )
        strengths = [t[0] for t in sorted_topics[:3] if t[1]["accuracy"] >= 70]
        weaknesses = [t[0] for t in sorted_topics[-3:] if t[1]["accuracy"] < 60]
        
        # Aggregate error patterns
        total_errors = {
            "conceptual": sum(p.conceptual_errors for p in progress_records),
            "careless": sum(p.careless_errors for p in progress_records),
            "overthinking": sum(p.overthinking_errors for p in progress_records),
            "time_pressure": sum(p.time_pressure_errors for p in progress_records)
        }
        
        # Find dominant error pattern
        dominant_error = max(total_errors.items(), key=lambda x: x[1])
        
        # Generate recommendation
        if weaknesses:
            recommended_topic = weaknesses[0]
            recommended_profile = topic_profiles[recommended_topic]
            recommendation = {
                "category": recommended_profile["category"],
                "sub_topic": recommended_topic,
                "difficulty": recommended_profile["difficulty_level"],
                "reason": f"Low accuracy ({recommended_profile['accuracy']}%) detected. Focus on building fundamentals.",
                "error_focus": dominant_error[0]
            }
        else:
            # No weaknesses, recommend advancing strongest topic
            recommended_topic = strengths[0] if strengths else list(topic_profiles.keys())[0]
            recommendation = {
                "category": topic_profiles[recommended_topic]["category"],
                "sub_topic": recommended_topic,
                "difficulty": "Advanced",
                "reason": "Strong performance. Ready for advanced challenges.",
                "error_focus": "trap_awareness"
            }
        
        return {
            "user_tier": user_tier,
            "overall_stats": {
                "total_attempted": total_attempted,
                "total_correct": total_correct,
                "overall_accuracy": round(overall_accuracy, 2),
                "avg_time_ratio": round(avg_time_ratio, 2)
            },
            "topic_profiles": topic_profiles,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "error_patterns": total_errors,
            "dominant_error": dominant_error[0],
            "recommended_focus": recommendation
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to get adaptive profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/elite/practice-session")
async def start_elite_practice_session(payload: dict, db: Session = Depends(get_db)):
    """
    Start an adaptive practice session with AI-generated questions
    
    Request:
    {
        "user_id": "user123",
        "category": "Quantitative",
        "sub_topic": "Probability",  # optional
        "question_count": 10,
        "target_tier": "auto"  # auto, developing, competent, advanced, elite
    }
    
    Response:
    {
        "session_id": "sess_xyz",
        "questions": [...],
        "adaptive_config": {...}
    }
    """
    from services.elite_question_generator import EliteQuestionGenerator
    import uuid
    
    try:
        user_id = payload.get("user_id")
        category = payload.get("category")
        sub_topic = payload.get("sub_topic")
        question_count = payload.get("question_count", 10)
        target_tier = payload.get("target_tier", "auto")
        
        if not all([user_id, category]):
            raise HTTPException(
                status_code=400,
                detail="user_id and category are required"
            )
        
        # If no sub_topic specified, pick one based on user profile
        if not sub_topic:
            from services.question_taxonomy import get_subtopics
            subtopics = get_subtopics(category)
            if not subtopics:
                raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
            sub_topic = subtopics[0]  # Default to first subtopic
        
        # Get adaptive profile
        adaptive_profile = AdaptiveEngine.calculate_multidimensional_difficulty(
            db, user_id, sub_topic, category
        )
        
        # Generate questions
        generator = EliteQuestionGenerator()
        questions = generator.generate_batch(
            category=category,
            sub_topic=sub_topic,
            difficulty_level=adaptive_profile["difficulty_level"],
            count=min(question_count, 10),  # Limit to 10 per session
            user_level=adaptive_profile.get("user_tier")
        )
        
        if not questions:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate questions. Please try again."
            )
        
        # Store questions in database
        question_ids = []
        for q_data in questions:
            q_id = str(uuid.uuid4())
            new_question = AptitudeQuestion(
                id=q_id,
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=q_data["correct_option"],
                answer_explanation=q_data.get("optimal_solution_strategy", ""),
                topic=sub_topic,
                category=category,
                difficulty=q_data["difficulty_level"],
                source="ai_generated_session",
                primary_concepts=q_data.get("primary_concepts", []),
                trap_explanation=q_data.get("trap_explanation"),
                optimal_solution_strategy=q_data.get("optimal_solution_strategy"),
                common_mistake=q_data.get("common_mistake"),
                time_to_solve_sec=q_data.get("time_to_solve_sec", 120)
            )
            db.add(new_question)
            question_ids.append(q_id)
        
        db.commit()
        
        # Format response
        formatted_questions = []
        for q_data in questions:
            formatted_questions.append({
                "question": q_data["question"],
                "options": q_data["options"],
                "difficulty_level": q_data["difficulty_level"],
                "time_to_solve_sec": q_data.get("time_to_solve_sec", 120)
            })
        
        session_id = str(uuid.uuid4())
        
        return {
            "session_id": session_id,
            "question_count": len(questions),
            "questions": formatted_questions,
            "question_ids": question_ids,
            "adaptive_config": {
                "starting_difficulty": adaptive_profile["difficulty_level"],
                "concept_depth": adaptive_profile["concept_depth"],
                "cognitive_load": adaptive_profile["cognitive_load"],
                "trap_density": adaptive_profile["trap_density"],
                "user_tier": adaptive_profile["user_tier"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to start elite practice session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/elite/error-analysis/{user_id}")
async def get_error_analysis(
    user_id: str,
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get detailed error pattern analysis for a user
    
    Response:
    {
        "total_errors": 45,
        "pattern_distribution": {...},
        "dominant_pattern": "conceptual",
        "recommendation": "...",
        "topic_breakdown": {...}
    }
    """
    try:
        if topic:
            # Analyze specific topic
            analysis = AdaptiveEngine.analyze_error_patterns(db, user_id, topic)
            return analysis
        else:
            # Analyze all topics
            progress_records = db.query(UserAptitudeProgress).filter(
                UserAptitudeProgress.user_id == user_id
            ).all()
            
            if not progress_records:
                return {
                    "message": "No practice history found",
                    "total_errors": 0
                }
            
            # Aggregate across all topics
            topic_analyses = {}
            for p in progress_records:
                analysis = AdaptiveEngine.analyze_error_patterns(db, user_id, p.topic)
                topic_analyses[p.topic] = analysis
            
            # Calculate overall
            total_errors = sum(a["total_errors"] for a in topic_analyses.values())
            overall_distribution = {
                "conceptual": sum(a["pattern_distribution"].get("conceptual", 0) for a in topic_analyses.values()),
                "careless": sum(a["pattern_distribution"].get("careless", 0) for a in topic_analyses.values()),
                "overthinking": sum(a["pattern_distribution"].get("overthinking", 0) for a in topic_analyses.values()),
                "time_pressure": sum(a["pattern_distribution"].get("time_pressure", 0) for a in topic_analyses.values())
            }
            
            dominant = max(overall_distribution.items(), key=lambda x: x[1])
            
            return {
                "total_errors": total_errors,
                "pattern_distribution": overall_distribution,
                "dominant_pattern": dominant[0],
                "topic_breakdown": topic_analyses
            }
            
    except Exception as e:
        print(f"[ERROR] Error analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))