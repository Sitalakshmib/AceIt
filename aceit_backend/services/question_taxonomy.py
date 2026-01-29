"""
Elite Aptitude Question Taxonomy

Structured classification system for CAT/XAT/GMAT/GRE/GATE-level aptitude questions.
Defines categories, sub-topics, difficulty calibration, and concept hierarchies.
"""

# ============================================================================
# APTITUDE TAXONOMY - Comprehensive Category Structure
# ============================================================================

APTITUDE_TAXONOMY = {
    "Analytical Reasoning": {
        "Coding": {
            "concepts": ["binary_coding", "conditional_coding", "substitution_cypher"],
            "elite_traps": ["multi_layer_coding", "reverse_pattern_shift"]
        },
        "Logical Operations": {
            "concepts": ["symbol_substitution", "balanced_equation", "inequality_logic"],
            "elite_traps": ["order_of_operations_ambiguity", "sign_reversal_trap"]
        },
        "Logical Reasoning": {
            "concepts": ["deductive_logic", "inductive_logic", "statement_assumption", "assertion_reason"],
            "elite_traps": ["correlation_vs_causation", "scope_shift_in_conclusion"]
        },
        "Mathematical Operations": {
            "concepts": ["bodmas_rules", "coded_inequalities", "operator_substitution"],
            "elite_traps": ["nested_brackets", "fractional_logic_traps"]
        }
    },

    "Data Interpretation": {
        "Bar Graph": {
            "concepts": ["stacked_bars", "grouped_bars", "percentage_change", "ratio_comparison"],
            "elite_traps": ["scale_manipulation", "cumulative_vs_individual_data"]
        },
        "Line Graph": {
            "concepts": ["trend_analysis", "slope_interpretation", "growth_rate_calculation"],
            "elite_traps": ["intersecting_lines_confusion", "base_year_ambiguity"]
        },
        "Pie Chart": {
            "concepts": ["degree_to_percentage", "multi_pie_comparison", "central_angle"],
            "elite_traps": ["total_value_mismatch", "missing_slice_inference"]
        }
    },

    "Logical Ability": {
        "Arrangement": {
            "concepts": ["linear_sequencing", "height_weight_ordering", "schedule_mapping"],
            "elite_traps": ["indeterminate_position", "conditional_ordering"]
        },
        "Arrangements": {
            "concepts": ["complex_matrix", "multi_variable_grid", "team_selection"],
            "elite_traps": ["mutually_exclusive_constraints", "hidden_pair_dependency"]
        },
        "Blood Relations": {
            "concepts": ["family_tree", "coded_relationships", "generation_gap"],
            "elite_traps": ["gender_ambiguity", "in_law_complexities", "same_name_different_person"]
        },
        "Coding-Decoding": {
            "concepts": ["letter_shifting", "number_coding", "mixed_series_coding"],
            "elite_traps": ["vowel_consonant_logic", "positional_sum_traps"]
        },
        "Data Sufficiency": {
            "concepts": ["statement_independence", "necessity_vs_sufficiency", "variable_elimination"],
            "elite_traps": ["common_conception_trap", "unnecessary_information_distraction"]
        },
        "Direction Sense": {
            "concepts": ["cardinal_directions", "pythagorean_triplets", "shadow_angles"],
            "elite_traps": ["relative_rotation", "final_orientation_vs_starting_point"]
        },
        "Number Series": {
            "concepts": ["arithmetic_progression", "geometric_progression", "prime_intervals", "square_cube_patterns"],
            "elite_traps": ["n_squared_minus_one_patterns", "alternating_series_logic"]
        },
        "Ranking": {
            "concepts": ["position_from_left_right", "interchanging_positions", "total_count_logic"],
            "elite_traps": ["overlapping_ranks", "min_max_people_cases"]
        },
        "Seating Arrangement": {
            "concepts": ["circular_arrangement", "linear_facing_north_south", "square_table"],
            "elite_traps": ["neighbor_constraints", "facing_center_vs_outward"]
        },
        "Syllogism": {
            "concepts": ["venn_diagrams_advanced", "only_few_logic", "possibility_vs_certainty"],
            "elite_traps": ["middle_term_distribution", "universal_negative_inference"]
        }
    },

    "Quantitative Ability": {
        "Algebra": {
            "concepts": ["linear_equations", "quadratic_roots", "polynomials", "identities"],
            "elite_traps": ["extraneous_roots", "sign_errors_in_inequalities"]
        },
        "Averages": {
            "concepts": ["weighted_average", "deviation_method", "replacement_logic"],
            "elite_traps": ["avg_speed_vs_avg_of_speeds", "group_change_impact"]
        },
        "Compound Interest": {
            "concepts": ["compounding_periods", "effective_rate", "amount_calculation"],
            "elite_traps": ["continuous_compounding_approximation", "installment_traps"]
        },
        "Number System": {
            "concepts": ["divisibility", "remainders", "unit_digit", "hcf_lcm"],
            "elite_traps": ["negative_remainders", "cyclicity_exceptions"]
        },
        "Percentages": {
            "concepts": ["percentage_change", "successive_change", "fraction_conversion"],
            "elite_traps": ["base_change_confusion", "reverse_percentage_logic"]
        },
        "Profit and Loss": {
            "concepts": ["cost_price_selling_price", "markup_discount", "profit_margin"],
            "elite_traps": ["false_weight_calculations", "discount_on_selling_price_trap"]
        },
        "Ratio and Proportion": {
            "concepts": ["proportionality", "mean_proportion", "partnership"],
            "elite_traps": ["inverse_ratio_distribution", "mixture_replacement_ratio"]
        },
        "Simple Interest": {
            "concepts": ["principal_rate_time", "linear_growth", "installment_si"],
            "elite_traps": ["time_unit_conversion_months_years", "rate_change_mid_term"]
        },
        "Time Speed Distance": {
            "concepts": ["relative_speed", "average_speed", "trains", "boats"],
            "elite_traps": ["unit_conversion_kmph_mps", "stoppage_time_inclusion"]
        },
        "Time and Work": {
            "concepts": ["efficiency_ratios", "man_days_formula", "pipes_cisterns"],
            "elite_traps": ["negative_efficiency_leaks", "leaving_joining_midway"]
        }
    },

    "Verbal Ability": {
        "Antonyms": {
            "concepts": ["semantic_opposites", "contextual_contrasts", "prefix_negation"],
            "elite_traps": ["near_antonyms", "degree_of_opposition"]
        },
        "Grammar": {
            "concepts": ["subject_verb_agreement", "tenses", "articles", "prepositions"],
            "elite_traps": ["subjunctive_mood", "dangling_modifiers"]
        },
        "Idioms": {
            "concepts": ["figurative_meaning", "cultural_context", "common_usage"],
            "elite_traps": ["literal_interpretation_trap", "similar_sounding_idioms"]
        },
        "One Word Substitution": {
            "concepts": ["root_words", "professional_terms", "phobias_manias"],
            "elite_traps": ["nuance_differences", "archaic_terms"]
        },
        "Reading Comprehension": {
            "concepts": ["main_idea", "inference", "tone_analysis", "detail_retrieval"],
            "elite_traps": ["scope_trap", "out_of_passage_knowledge"]
        },
        "Sentence Completion": {
            "concepts": ["vocabulary_fit", "logical_flow", "connector_logic"],
            "elite_traps": ["double_negatives", "tone_shift_words"]
        },
        "Spelling": {
            "concepts": ["homophones", "silent_letters", "suffix_rules"],
            "elite_traps": ["common_misspellings", "uk_vs_us_spelling"]
        },
        "Synonyms": {
            "concepts": ["semantic_similarity", "connotation", "register"],
            "elite_traps": ["nuance_mismatch", "context_specific_meaning"]
        },
        "Vocabulary": {
            "concepts": ["word_roots", "etymology", "usage_context"],
            "elite_traps": ["secondary_meanings", "confusing_pairs"]
        }
    }
}



# ============================================================================
# DIFFICULTY CALIBRATION - Multi-Dimensional Difficulty Framework
# ============================================================================

DIFFICULTY_CALIBRATION = {
    "Easy": {
        "description": "Single concept, guided reasoning, obvious traps. Direct formula application. Warm-up / confidence builders.",
        "concept_count": 1,
        "reasoning_steps": "1-2",
        "trap_level": "obvious",
        "time_expected_sec": 60,
        "cognitive_load": "low",
        "data_complexity": "minimal",
        "target_accuracy": "70-80%",
        "discriminatory_power": "low"
    },
    "Medium": {
        "description": "Two concepts combined, moderate reasoning, subtle traps. Concept selection + logical reasoning. Cutoff & shortlisting level.",
        "concept_count": 2,
        "reasoning_steps": "2-3",
        "trap_level": "moderate",
        "time_expected_sec": 90,
        "cognitive_load": "medium",
        "data_complexity": "moderate",
        "target_accuracy": "26-60%",
        "discriminatory_power": "medium"
    },
    "Hard": {
        "description": "Hidden constraints, elimination strategy required, expert traps. Multi-step logic, reverse reasoning, inference-based. Top 10-20% filtering.",
        "concept_count": "2-3",
        "reasoning_steps": "3-4",
        "trap_level": "subtle",
        "time_expected_sec": 120,
        "cognitive_load": "high",
        "data_complexity": "complex",
        "target_accuracy": "15-25%",
        "discriminatory_power": "high"
    }
}


# ============================================================================
# CONCEPT DEPTH HIERARCHY
# ============================================================================

CONCEPT_DEPTH_LEVELS = {
    "single": {
        "description": "One primary concept application",
        "example": "Simple percentage calculation",
        "suitable_for": ["Easy"]
    },
    "dual": {
        "description": "Two concepts combined",
        "example": "Percentage + Ratio combined problem",
        "suitable_for": ["Medium", "Hard"]
    },
    "multi": {
        "description": "Three or more concepts interwoven",
        "example": "Time-Work-Efficiency with variable rates and partial completion",
        "suitable_for": ["Hard"]
    },
    "meta": {
        "description": "Requires meta-reasoning or reverse engineering",
        "example": "Derive the question from answer choices",
        "suitable_for": ["Hard"]
    }
}


# ============================================================================
# TRAP DENSITY CLASSIFICATION
# ============================================================================

TRAP_TYPES = {
    "calculation_trap": {
        "description": "Arithmetic error leads to wrong option",
        "difficulty": "Easy",
        "example": "Forgetting to multiply by 100 in percentage"
    },
    "conceptual_trap": {
        "description": "Misunderstanding of core concept",
        "difficulty": "Medium",
        "example": "Confusing simple vs compound interest"
    },
    "assumption_trap": {
        "description": "Hidden assumption not stated",
        "difficulty": "Hard",
        "example": "Assuming uniform distribution when not specified"
    },
    "reverse_logic_trap": {
        "description": "Correct logic applied in wrong direction",
        "difficulty": "Hard",
        "example": "Calculating what was asked to be derived, not the actual question"
    },
    "data_sufficiency_trap": {
        "description": "Unnecessary data misleads",
        "difficulty": "Hard",
        "example": "Extra information that seems relevant but isn't"
    },
    "time_pressure_trap": {
        "description": "Long calculation path exists, but insight shortcut available",
        "difficulty": "Hard",
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
        "recommended_difficulty": "Easy",
        "description": "Building foundational concepts"
    },
    "competent": {
        "accuracy_range": "40-60%",
        "avg_time_multiplier": "1.2-1.5x",
        "concept_mastery": "intermediate",
        "recommended_difficulty": "Medium",
        "description": "Solid fundamentals, working on speed"
    },
    "advanced": {
        "accuracy_range": "60-80%",
        "avg_time_multiplier": "0.8-1.2x",
        "concept_mastery": "advanced",
        "recommended_difficulty": "Hard",
        "description": "Strong conceptual clarity, refining edge cases"
    },
    "elite": {
        "accuracy_range": "80-100%",
        "avg_time_multiplier": "<0.8x",
        "concept_mastery": "expert",
        "recommended_difficulty": "Hard",
        "description": "Top 5% performer, pattern recognition mastery"
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_subtopics(category: str) -> list:
    """Get all subtopics for a given category in alphabetical order"""
    if category not in APTITUDE_TAXONOMY:
        return []
    return sorted(list(APTITUDE_TAXONOMY[category].keys()))


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
    return DIFFICULTY_CALIBRATION.get(difficulty_level, DIFFICULTY_CALIBRATION["Easy"])


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
