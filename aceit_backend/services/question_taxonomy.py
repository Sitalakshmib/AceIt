"""
Elite Aptitude Question Taxonomy

Structured classification system for CAT/XAT/GMAT/GRE/GATE-level aptitude questions.
Defines categories, sub-topics, difficulty calibration, and concept hierarchies.
"""

# ============================================================================
# APTITUDE TAXONOMY - Comprehensive Category Structure
# ============================================================================

APTITUDE_TAXONOMY = {
    "Quantitative": {
        "Number Systems": {
            "concepts": ["modulo_traps", "remainder_cycles", "divisibility_rules", "prime_factorization", "lcm_gcd_applications"],
            "elite_traps": ["negative_remainders", "chinese_remainder_theorem", "fermat_little_theorem"]
        },
        "Percentages & Ratios": {
            "concepts": ["multi_step_dependency", "reverse_calculation", "successive_percentage", "ratio_proportion_variation"],
            "elite_traps": ["compound_percentage_chains", "inverse_proportionality", "alligation_mixtures"]
        },
        "Averages & Alligation": {
            "concepts": ["weighted_averages", "reverse_average_problems", "alligation_rule", "replacement_scenarios"],
            "elite_traps": ["hidden_weight_distribution", "multi_group_averaging", "time_based_averages"]
        },
        "Time & Work": {
            "concepts": ["variable_efficiency", "hidden_assumptions", "work_equivalence", "negative_work"],
            "elite_traps": ["efficiency_variation_over_time", "partial_work_completion", "group_dynamics"]
        },
        "Time Speed Distance": {
            "concepts": ["relative_motion", "frame_shifting", "circular_tracks", "boats_streams", "trains_platforms"],
            "elite_traps": ["variable_speed", "meeting_point_problems", "average_speed_traps"]
        },
        "Profit Loss Discount": {
            "concepts": ["nested_conditions", "successive_discounts", "marked_price_traps", "false_weights"],
            "elite_traps": ["cost_price_ambiguity", "discount_on_discount", "partnership_profit_sharing"]
        },
        "Simple Compound Interest": {
            "concepts": ["comparison_logic", "time_period_variations", "rate_changes", "installment_problems"],
            "elite_traps": ["compound_frequency_variations", "effective_rate_calculation", "present_value_future_value"]
        },
        "Permutation Combination": {
            "concepts": ["constraint_heavy", "circular_permutations", "selection_with_restrictions", "derangements"],
            "elite_traps": ["identical_objects", "conditional_arrangements", "group_formation"]
        },
        "Probability": {
            "concepts": ["conditional_probability", "bayesian_traps", "complement_logic", "independent_events"],
            "elite_traps": ["bayes_theorem_applications", "geometric_probability", "expectation_variance"]
        },
        "Data Interpretation": {
            "concepts": ["multi_table_inference", "percentage_change_analysis", "ratio_comparison", "trend_analysis"],
            "elite_traps": ["missing_data_inference", "scale_manipulation", "compound_metric_calculation"]
        }
    },
    
    "Logical": {
        "Syllogisms": {
            "concepts": ["venn_diagrams", "logical_negation", "all_some_none", "conclusion_validity"],
            "elite_traps": ["complementary_statements", "possibility_vs_definite", "reverse_logic"]
        },
        "Seating Arrangements": {
            "concepts": ["circular_arrangements", "conditional_constraints", "linear_arrangements", "facing_directions"],
            "elite_traps": ["multiple_constraint_intersection", "negative_constraints", "variable_positions"]
        },
        "Puzzles": {
            "concepts": ["multi_constraint_elimination", "grid_based_logic", "scheduling_problems", "ranking_ordering"],
            "elite_traps": ["hidden_constraints", "mutual_exclusivity", "temporal_logic"]
        },
        "Blood Relations": {
            "concepts": ["tree_inversion", "gender_ambiguity", "generation_gaps", "coded_relations"],
            "elite_traps": ["same_gender_names", "multiple_relationship_paths", "indirect_relations"]
        },
        "Coding Decoding": {
            "concepts": ["pattern_recognition", "rule_switching", "letter_number_substitution", "operation_based_coding"],
            "elite_traps": ["multi_step_encoding", "conditional_rules", "reverse_decoding"]
        },
        "Direction Sense": {
            "concepts": ["coordinate_geometry_style", "displacement_calculation", "shortest_path", "bearing_angles"],
            "elite_traps": ["diagonal_movements", "relative_directions", "3d_movement"]
        },
        "Clocks Calendars": {
            "concepts": ["compound_logic", "angle_calculation", "day_counting", "leap_year_logic"],
            "elite_traps": ["mirror_clock_problems", "calendar_pattern_recognition", "time_zone_variations"]
        },
        "Input Output": {
            "concepts": ["state_transition_logic", "sequential_operations", "pattern_based_transformation"],
            "elite_traps": ["variable_step_patterns", "conditional_transformations", "reverse_engineering"]
        }
    },
    
    "Verbal": {
        "Reading Comprehension": {
            "concepts": ["inference_heavy", "tone_analysis", "author_intent", "implicit_meaning", "contextual_vocabulary"],
            "elite_traps": ["subtle_inference", "tone_vs_content", "exception_identification"]
        },
        "Sentence Correction": {
            "concepts": ["grammar_semantics", "parallelism", "modifier_placement", "verb_tense_consistency"],
            "elite_traps": ["meaning_alteration", "idiomatic_expressions", "conciseness_vs_clarity"]
        },
        "Para Jumbles": {
            "concepts": ["logical_flow", "tone_consistency", "connector_identification", "opening_closing_sentences"],
            "elite_traps": ["similar_opening_sentences", "temporal_vs_logical_order", "pronoun_reference"]
        },
        "Critical Reasoning": {
            "concepts": ["assumptions", "strengthen_weaken", "inference", "paradox_resolution", "bold_face_reasoning"],
            "elite_traps": ["necessary_vs_sufficient", "correlation_causation", "scope_shifts"]
        },
        "Vocabulary in Context": {
            "concepts": ["contextual_meaning", "synonym_antonym_usage", "word_tone", "connotation_denotation"],
            "elite_traps": ["multiple_meanings", "register_appropriateness", "collocation"]
        }
    },
    
    "Data Sufficiency": {
        "Quant Hybrid": {
            "concepts": ["sufficient_data_detection", "minimal_info_reasoning", "statement_combination", "redundant_data_identification"],
            "elite_traps": ["hidden_sufficiency", "statement_dependency", "value_vs_relationship"]
        },
        "Logic Hybrid": {
            "concepts": ["constraint_sufficiency", "logical_deduction", "information_completeness"],
            "elite_traps": ["implicit_constraints", "mutual_exclusivity_detection", "partial_information_traps"]
        }
    }
}


# ============================================================================
# DIFFICULTY CALIBRATION - Multi-Dimensional Difficulty Framework
# ============================================================================

DIFFICULTY_CALIBRATION = {
    "Beginner": {
        "description": "Single concept, guided reasoning, obvious traps",
        "concept_count": 1,
        "reasoning_steps": "1-2",
        "trap_level": "obvious",
        "time_expected_sec": 90,
        "cognitive_load": "low",
        "data_complexity": "minimal",
        "target_accuracy": "70-80%",
        "discriminatory_power": "low"
    },
    "Intermediate": {
        "description": "Two concepts combined, moderate reasoning, subtle traps",
        "concept_count": 2,
        "reasoning_steps": "2-3",
        "trap_level": "moderate",
        "time_expected_sec": 120,
        "cognitive_load": "medium",
        "data_complexity": "moderate",
        "target_accuracy": "50-60%",
        "discriminatory_power": "medium"
    },
    "Advanced": {
        "description": "Hidden constraints, elimination strategy required, expert traps",
        "concept_count": "2-3",
        "reasoning_steps": "3-4",
        "trap_level": "subtle",
        "time_expected_sec": 150,
        "cognitive_load": "high",
        "data_complexity": "complex",
        "target_accuracy": "30-40%",
        "discriminatory_power": "high"
    },
    "Elite": {
        "description": "Reverse reasoning, minimal data, inference-based, CAT/GMAT level",
        "concept_count": "3+",
        "reasoning_steps": "4+",
        "trap_level": "expert",
        "time_expected_sec": 120,  # Requires insight, not brute force
        "cognitive_load": "very_high",
        "data_complexity": "minimal_but_dense",
        "target_accuracy": "15-25%",
        "discriminatory_power": "very_high"
    }
}


# ============================================================================
# CONCEPT DEPTH HIERARCHY
# ============================================================================

CONCEPT_DEPTH_LEVELS = {
    "single": {
        "description": "One primary concept application",
        "example": "Simple percentage calculation",
        "suitable_for": ["Beginner"]
    },
    "dual": {
        "description": "Two concepts combined",
        "example": "Percentage + Ratio combined problem",
        "suitable_for": ["Intermediate", "Advanced"]
    },
    "multi": {
        "description": "Three or more concepts interwoven",
        "example": "Time-Work-Efficiency with variable rates and partial completion",
        "suitable_for": ["Advanced", "Elite"]
    },
    "meta": {
        "description": "Requires meta-reasoning or reverse engineering",
        "example": "Derive the question from answer choices",
        "suitable_for": ["Elite"]
    }
}


# ============================================================================
# TRAP DENSITY CLASSIFICATION
# ============================================================================

TRAP_TYPES = {
    "calculation_trap": {
        "description": "Arithmetic error leads to wrong option",
        "difficulty": "Beginner",
        "example": "Forgetting to multiply by 100 in percentage"
    },
    "conceptual_trap": {
        "description": "Misunderstanding of core concept",
        "difficulty": "Intermediate",
        "example": "Confusing simple vs compound interest"
    },
    "assumption_trap": {
        "description": "Hidden assumption not stated",
        "difficulty": "Advanced",
        "example": "Assuming uniform distribution when not specified"
    },
    "reverse_logic_trap": {
        "description": "Correct logic applied in wrong direction",
        "difficulty": "Elite",
        "example": "Calculating what was asked to be derived, not the actual question"
    },
    "data_sufficiency_trap": {
        "description": "Unnecessary data misleads",
        "difficulty": "Advanced",
        "example": "Extra information that seems relevant but isn't"
    },
    "time_pressure_trap": {
        "description": "Long calculation path exists, but insight shortcut available",
        "difficulty": "Elite",
        "example": "Brute force takes 5 min, pattern recognition takes 30 sec"
    }
}


# ============================================================================
# ERROR PATTERN TAXONOMY
# ============================================================================

ERROR_PATTERNS = {
    "conceptual": {
        "indicators": ["wrong_approach", "formula_misapplication", "logic_error"],
        "remediation": "concept_revision",
        "severity": "high"
    },
    "careless": {
        "indicators": ["calculation_mistake", "sign_error", "unit_conversion_error"],
        "remediation": "practice_accuracy",
        "severity": "low"
    },
    "overthinking": {
        "indicators": ["correct_initial_approach", "complicated_unnecessarily", "second_guessing"],
        "remediation": "confidence_building",
        "severity": "medium"
    },
    "time_pressure": {
        "indicators": ["rushed_answer", "skipped_steps", "incomplete_reasoning"],
        "remediation": "speed_training",
        "severity": "medium"
    },
    "trap_susceptibility": {
        "indicators": ["fell_for_obvious_trap", "didnt_check_options", "pattern_blindness"],
        "remediation": "trap_awareness_training",
        "severity": "high"
    }
}


# ============================================================================
# USER TIER CLASSIFICATION
# ============================================================================

USER_TIERS = {
    "developing": {
        "accuracy_range": "0-40%",
        "avg_time_multiplier": ">1.5x",
        "concept_mastery": "beginner",
        "recommended_difficulty": "Beginner",
        "description": "Building foundational concepts"
    },
    "competent": {
        "accuracy_range": "40-60%",
        "avg_time_multiplier": "1.2-1.5x",
        "concept_mastery": "intermediate",
        "recommended_difficulty": "Intermediate",
        "description": "Solid fundamentals, working on speed"
    },
    "advanced": {
        "accuracy_range": "60-80%",
        "avg_time_multiplier": "0.8-1.2x",
        "concept_mastery": "advanced",
        "recommended_difficulty": "Advanced",
        "description": "Strong conceptual clarity, refining edge cases"
    },
    "elite": {
        "accuracy_range": "80-100%",
        "avg_time_multiplier": "<0.8x",
        "concept_mastery": "expert",
        "recommended_difficulty": "Elite",
        "description": "Top 5% performer, pattern recognition mastery"
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_subtopics(category: str) -> list:
    """Get all subtopics for a given category"""
    if category not in APTITUDE_TAXONOMY:
        return []
    return list(APTITUDE_TAXONOMY[category].keys())


def get_concepts(category: str, subtopic: str) -> list:
    """Get all concepts for a given category and subtopic"""
    if category not in APTITUDE_TAXONOMY:
        return []
    if subtopic not in APTITUDE_TAXONOMY[category]:
        return []
    return APTITUDE_TAXONOMY[category][subtopic].get("concepts", [])


def get_elite_traps(category: str, subtopic: str) -> list:
    """Get elite-level traps for a given category and subtopic"""
    if category not in APTITUDE_TAXONOMY:
        return []
    if subtopic not in APTITUDE_TAXONOMY[category]:
        return []
    return APTITUDE_TAXONOMY[category][subtopic].get("elite_traps", [])


def get_difficulty_specs(difficulty_level: str) -> dict:
    """Get specifications for a difficulty level"""
    return DIFFICULTY_CALIBRATION.get(difficulty_level, DIFFICULTY_CALIBRATION["Beginner"])


def classify_user_tier(accuracy: float, avg_time_ratio: float) -> str:
    """
    Classify user into a tier based on accuracy and time performance
    
    Args:
        accuracy: Overall accuracy percentage (0-100)
        avg_time_ratio: Ratio of user's avg time to expected time
    
    Returns:
        User tier: developing, competent, advanced, elite
    """
    if accuracy >= 80 and avg_time_ratio < 0.8:
        return "elite"
    elif accuracy >= 60 and avg_time_ratio < 1.2:
        return "advanced"
    elif accuracy >= 40 and avg_time_ratio < 1.5:
        return "competent"
    else:
        return "developing"


def get_recommended_difficulty(user_tier: str) -> str:
    """Get recommended difficulty level for a user tier"""
    tier_config = USER_TIERS.get(user_tier, USER_TIERS["developing"])
    return tier_config["recommended_difficulty"]


def validate_category_subtopic(category: str, subtopic: str) -> bool:
    """Validate if category and subtopic combination exists"""
    return (category in APTITUDE_TAXONOMY and 
            subtopic in APTITUDE_TAXONOMY[category])
