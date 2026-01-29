from sqlalchemy.orm import sessionmaker
import sys
import os
import uuid

# Add the parent directory to sys.path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database_postgres import engine
from models.aptitude_sql import AptitudeQuestion

Session = sessionmaker(bind=engine)
session = Session()

questions = [
    # EASY (20)
    {"question": "Choose the correctly spelled word:", "options": ["Accomodate", "Acommodate", "Accommodate", "Acomodate"], "correct_answer": 2, "explanation": "\"Accommodate\" has double 'c' and double 'm'.", "difficulty": "easy", "concepts": ["double_consonants"], "traps": ["phonetic_spelling_error", "omitted_letters"]},
    {"question": "Choose the correctly spelled word:", "options": ["Seperate", "Separate", "Seperete", "Separete"], "correct_answer": 1, "explanation": "\"Separate\" has 'a' after 'p', not 'e'.", "difficulty": "easy", "concepts": ["vowel_confusion"], "traps": ["pronunciation_based_error"]},
    {"question": "Choose the correctly spelled word:", "options": ["Definately", "Definitely", "Definately", "Definitaly"], "correct_answer": 1, "explanation": "\"Definitely\" comes from \"finite\" - remember \"finite\" in the middle.", "difficulty": "easy", "concepts": ["word_origin_clues"], "traps": ["adverbial_ending_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Occasion", "Ocassion", "Occassion", "Ocasion"], "correct_answer": 0, "explanation": "\"Occasion\" has double 'c' but single 's'.", "difficulty": "easy", "concepts": ["c_s_double_consonants"], "traps": ["symmetry_error"]},
    {"question": "Choose the correctly spelled word:", "options": ["Priviledge", "Privilege", "Privelege", "Privilage"], "correct_answer": 1, "explanation": "\"Privilege\" has 'i' after 'v', 'e' after 'l', and 'ge' ending.", "difficulty": "easy", "concepts": ["vowel_sequence"], "traps": ["pronunciation_spelling_mismatch"]},
    {"question": "Choose the correctly spelled word:", "options": ["Neccessary", "Necessary", "Necesary", "Nessessary"], "correct_answer": 1, "explanation": "\"Necessary\" has one 'c' and double 's'.", "difficulty": "easy", "concepts": ["c_s_combination"], "traps": ["double_consonant_overgeneralization"]},
    {"question": "Choose the correctly spelled word:", "options": ["Arguement", "Argument", "Arguemant", "Argumant"], "correct_answer": 1, "explanation": "\"Argument\" drops the 'e' from \"argue\" when adding \"-ment.\"", "difficulty": "easy", "concepts": ["silent_e_dropping"], "traps": ["retained_e_error"]},
    {"question": "Choose the correctly spelled word:", "options": ["Judgement", "Judgment", "Judgemant", "Judgemint"], "correct_answer": 1, "explanation": "Both \"judgment\" (US) and \"judgement\" (UK) are correct, but US spelling is commonly tested.", "difficulty": "easy", "concepts": ["american_british_spelling"], "traps": ["regional_variation_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Mischevious", "Mischievous", "Mischievious", "Mischivous"], "correct_answer": 1, "explanation": "\"Mischievous\" has three syllables, not four. No 'i' after 'v'.", "difficulty": "easy", "concepts": ["syllable_count_awareness"], "traps": ["extra_vowel_insertion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Tounge", "Tongue", "Tung", "Toungee"], "correct_answer": 1, "explanation": "\"Tongue\" has 'o' after 't' and 'ue' ending.", "difficulty": "easy", "concepts": ["silent_letters"], "traps": ["phonetic_spelling"]},
    {"question": "Choose the correctly spelled word:", "options": ["Wierd", "Weird", "Weerd", "Wiered"], "correct_answer": 1, "explanation": "\"Weird\" follows \"i before e except after c\" exception.", "difficulty": "easy", "concepts": ["i_before_e_rule"], "traps": ["rule_exception"]},
    {"question": "Choose the correctly spelled word:", "options": ["Recieve", "Receive", "Recieve", "Receave"], "correct_answer": 1, "explanation": "\"Receive\" follows \"i before e except after c\" rule.", "difficulty": "easy", "concepts": ["i_before_e_rule_application"], "traps": ["rule_violation"]},
    {"question": "Choose the correctly spelled word:", "options": ["Acheive", "Achieve", "Acheeve", "Achive"], "correct_answer": 1, "explanation": "\"Achieve\" has 'ie' after 'ch' (not following \"after c\" rule).", "difficulty": "easy", "concepts": ["i_e_digraphs"], "traps": ["phonetic_spelling_error"]},
    {"question": "Choose the correctly spelled word:", "options": ["Calender", "Calendar", "Calandar", "Calender"], "correct_answer": 1, "explanation": "\"Calendar\" ends with 'ar', not 'er'.", "difficulty": "easy", "concepts": ["ar_er_ending_confusion"], "traps": ["homophone_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Embarrass", "Embarass", "Embarras", "Embaras"], "correct_answer": 0, "explanation": "\"Embarrass\" has double 'r' and double 's'.", "difficulty": "easy", "concepts": ["double_consonants"], "traps": ["insufficient_doubling"]},
    {"question": "Choose the correctly spelled word:", "options": ["Occurrence", "Occurence", "Ocurrence", "Ocurence"], "correct_answer": 0, "explanation": "\"Occurrence\" has double 'c', double 'r', and '-ence' ending.", "difficulty": "easy", "concepts": ["suffix_spelling"], "traps": ["single_vs_double_consonant"]},
    {"question": "Choose the correctly spelled word:", "options": ["Maintainance", "Maintenance", "Maintanance", "Maintenence"], "correct_answer": 1, "explanation": "\"Maintenance\" has 'te' in the middle, not 'ta'.", "difficulty": "easy", "concepts": ["vowel_patterns"], "traps": ["pronunciation_based_spelling"]},
    {"question": "Choose the correctly spelled word:", "options": ["Perseverance", "Perseverence", "Preseverance", "Preseverence"], "correct_answer": 0, "explanation": "\"Perseverance\" has 'a' in the last syllable.", "difficulty": "easy", "concepts": ["ance_ence_endings"], "traps": ["suffix_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Questionnaire", "Questionaire", "Questionnair", "Questionair"], "correct_answer": 0, "explanation": "\"Questionnaire\" has double 'n' and ends with '-aire'.", "difficulty": "easy", "concepts": ["french_loanwords"], "traps": ["simplified_spelling"]},
    {"question": "Choose the correctly spelled word:", "options": ["Restaurant", "Restaraunt", "Restuarant", "Restraunt"], "correct_answer": 0, "explanation": "\"Restaurant\" has 'au' after 't', not 'ua' or 'ara'.", "difficulty": "easy", "concepts": ["vowel_sequence_memorization"], "traps": ["vowel_reversal"]},
    
    # MEDIUM (20)
    {"question": "Choose the correctly spelled word:", "options": ["Conscientious", "Conscientous", "Consciencious", "Conscientius"], "correct_answer": 0, "explanation": "\"Conscientious\" has 't' after 'c' and ends with '-tious'.", "difficulty": "medium", "concepts": ["tious_cious_endings"], "traps": ["suffix_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Fulfill", "Fullfill", "Fulfil", "Fullfill"], "correct_answer": 0, "explanation": "Both \"fulfill\" (US) and \"fulfil\" (UK) are correct, but \"fulfill\" is more common.", "difficulty": "medium", "concepts": ["l_doubling_rules"], "traps": ["regional_variations"]},
    {"question": "Choose the correctly spelled word:", "options": ["Harass", "Harrass", "Harras", "Haras"], "correct_answer": 0, "explanation": "\"Harass\" has one 'r' and double 's'.", "difficulty": "medium", "concepts": ["stress_based_spelling"], "traps": ["double_consonant_overuse"]},
    {"question": "Choose the correctly spelled word:", "options": ["Liaison", "Liason", "Laison", "Liasonn"], "correct_answer": 0, "explanation": "\"Liaison\" has 'i' after 'l' and ends with '-son'.", "difficulty": "medium", "concepts": ["french_derived_spellings"], "traps": ["vowel_omission"]},
    {"question": "Choose the correctly spelled word:", "options": ["Millennium", "Millenium", "Milenium", "Millenneum"], "correct_answer": 0, "explanation": "\"Millennium\" has double 'l' and double 'n'.", "difficulty": "medium", "concepts": ["latin_derived_spellings"], "traps": ["single_consonant_error"]},
    {"question": "Choose the correctly spelled word:", "options": ["Nauseous", "Nausous", "Nauseus", "Nausious"], "correct_answer": 0, "explanation": "\"Nauseous\" has 'e' after 'u' and ends with '-ous'.", "difficulty": "medium", "concepts": ["ous_endings"], "traps": ["vowel_insertion_error"]},
    {"question": "Choose the correctly spelled word:", "options": ["Occasionally", "Occassionally", "Occasionali", "Ocasionally"], "correct_answer": 0, "explanation": "\"Occasionally\" has double 'c', single 's', and double 'l'.", "difficulty": "medium", "concepts": ["adverb_formation"], "traps": ["suffix_addition_errors"]},
    {"question": "Choose the correctly spelled word:", "options": ["Parallelogram", "Paralellogram", "Paralelogram", "Parallellogram"], "correct_answer": 0, "explanation": "\"Parallelogram\" has double 'l', single 'l', then 'logram'.", "difficulty": "medium", "concepts": ["geometric_term_spelling"], "traps": ["symmetry_overgeneralization"]},
    {"question": "Choose the correctly spelled word:", "options": ["Persevere", "Perservere", "Persever", "Perseveer"], "correct_answer": 0, "explanation": "\"Persevere\" has 'se' after 'per' and ends with '-vere'.", "difficulty": "medium", "concepts": ["verb_spelling_patterns"], "traps": ["extra_syllable_insertion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Pharaoh", "Pharoah", "Pharao", "Pharoh"], "correct_answer": 0, "explanation": "\"Pharaoh\" has 'a' before 'o'.", "difficulty": "medium", "concepts": ["historical_term_spelling"], "traps": ["vowel_reversal"]},
    {"question": "Choose the correctly spelled word:", "options": ["Playwright", "Playwrite", "Playright", "Playrite"], "correct_answer": 0, "explanation": "\"Playwright\" ends with '-wright' (craftsman), not '-write'.", "difficulty": "medium", "concepts": ["compound_word_spelling"], "traps": ["homophone_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Pronunciation", "Pronounciation", "Pronouncation", "Pronuncation"], "correct_answer": 0, "explanation": "\"Pronunciation\" comes from \"pronounce\" but drops the 'o'.", "difficulty": "medium", "concepts": ["noun_formation_spelling"], "traps": ["source_word_influence"]},
    {"question": "Choose the correctly spelled word:", "options": ["Renaissance", "Renaissence", "Renaissanse", "Rennaissance"], "correct_answer": 0, "explanation": "\"Renaissance\" has single 'n', double 's', and ends with '-ance'.", "difficulty": "medium", "concepts": ["french_loanword_spelling"], "traps": ["double_consonant_errors"]},
    {"question": "Choose the correctly spelled word:", "options": ["Reservoir", "Resevoir", "Reservior", "Resavoir"], "correct_answer": 0, "explanation": "\"Reservoir\" ends with '-oir' (French pattern).", "difficulty": "medium", "concepts": ["french_endings"], "traps": ["anglicized_spelling_attempt"]},
    {"question": "Choose the correctly spelled word:", "options": ["Rhythm", "Rythm", "Rhythym", "Rythym"], "correct_answer": 0, "explanation": "\"Rhythm\" starts with 'rh', has 'y', then 'thm'.", "difficulty": "medium", "concepts": ["silent_h_patterns"], "traps": ["phonetic_spelling"]},
    {"question": "Choose the correctly spelled word:", "options": ["Siege", "Seige", "Seege", "Sieg"], "correct_answer": 0, "explanation": "\"Siege\" follows \"i before e except after c\" (no 'c' here, so 'ie').", "difficulty": "medium", "concepts": ["i_e_rule_application"], "traps": ["rule_misapplication"]},
    {"question": "Choose the correctly spelled word:", "options": ["Supersede", "Supercede", "Superseed", "Superceed"], "correct_answer": 0, "explanation": "\"Supersede\" is the only English word ending in '-sede' (others are '-ceed' or '-cede').", "difficulty": "medium", "concepts": ["unique_spelling_patterns"], "traps": ["analogical_error"]},
    {"question": "Choose the correctly spelled word:", "options": ["Threshold", "Threshhold", "Thresold", "Threshod"], "correct_answer": 0, "explanation": "\"Threshold\" has 'h' after 's' and ends with 'old'.", "difficulty": "medium", "concepts": ["compound_word_spelling"], "traps": ["redundant_doubling"]},
    {"question": "Choose the correctly spelled word:", "options": ["Tyranny", "Tyrrany", "Tyrany", "Tyrranny"], "correct_answer": 0, "explanation": "\"Tyranny\" has single 'r', double 'n', and ends with 'y'.", "difficulty": "medium", "concepts": ["y_endings"], "traps": ["double_consonant_errors"]},
    {"question": "Choose the correctly spelled word:", "options": ["Vaccuum", "Vacuum", "Vaccum", "Vaccume"], "correct_answer": 1, "explanation": "\"Vacuum\" has one 'c' and double 'u'.", "difficulty": "medium", "concepts": ["latin_derived_spelling"], "traps": ["english_spelling_analogy"]},
    
    # HARD (20)
    {"question": "Choose the correctly spelled word:", "options": ["Abeyance", "Abeyence", "Abyance", "Abeiance"], "correct_answer": 0, "explanation": "\"Abeyance\" has 'e' after 'b' and ends with '-ance'.", "difficulty": "hard", "concepts": ["legal_terms_spelling"], "traps": ["suffix_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Bougainvillea", "Bouganvillea", "Bougainvilla", "Bouganvilia"], "correct_answer": 0, "explanation": "\"Bougainvillea\" has 'gai' in the middle and ends with '-ea'.", "difficulty": "hard", "concepts": ["botanical_names_spelling"], "traps": ["vowel_sequence_errors"]},
    {"question": "Choose the correctly spelled word:", "options": ["Cappuccino", "Capuccino", "Cappucino", "Capuchino"], "correct_answer": 0, "explanation": "\"Cappuccino\" has double 'p', double 'c', and ends with '-ino'.", "difficulty": "hard", "concepts": ["italian_loanwords"], "traps": ["single_consonant_error"]},
    {"question": "Choose the correctly spelled word:", "options": ["Dichotomy", "Dichotamy", "Dikotomy", "Dichotemy"], "correct_answer": 0, "explanation": "\"Dichotomy\" has 'ch' after 'di' and ends with '-tomy'.", "difficulty": "hard", "concepts": ["greek_derived_terms"], "traps": ["vowel_substitution"]},
    {"question": "Choose the correctly spelled word:", "options": ["Efficacy", "Efficasy", "Effacacy", "Eficacy"], "correct_answer": 0, "explanation": "\"Efficacy\" has 'ff', 'c' after 'ff', and ends with '-acy'.", "difficulty": "hard", "concepts": ["medical_technical_terms"], "traps": ["c_k_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Fuchsia", "Fushia", "Fuschia", "Fuchia"], "correct_answer": 0, "explanation": "\"Fuchsia\" has 'ch' after 'u' and ends with '-sia'.", "difficulty": "hard", "concepts": ["proper_name_derivations"], "traps": ["phonetic_spelling_attempt"]},
    {"question": "Choose the correctly spelled word:", "options": ["Gnocchi", "Nocchi", "Gnochi", "Gnoki"], "correct_answer": 0, "explanation": "\"Gnocchi\" starts with silent 'g', has double 'c', and ends with 'hi'.", "difficulty": "hard", "concepts": ["italian_food_terms"], "traps": ["silent_letter_omission"]},
    {"question": "Choose the correctly spelled word:", "options": ["Hemorrhage", "Hemorage", "Hemmorhage", "Hemmorrage"], "correct_answer": 0, "explanation": "\"Hemorrhage\" has double 'r', single 'h', and ends with '-age'.", "difficulty": "hard", "concepts": ["medical_terminology"], "traps": ["consonant_doubling_errors"]},
    {"question": "Choose the correctly spelled word:", "options": ["Idiosyncrasy", "Idiosyncrecy", "Idiosyncracy", "Idiosincrasy"], "correct_answer": 0, "explanation": "\"Idiosyncrasy\" has 'syn' in the middle and ends with '-asy'.", "difficulty": "hard", "concepts": ["psychological_terms"], "traps": ["suffix_variation"]},
    {"question": "Choose the correctly spelled word:", "options": ["Kaleidoscope", "Kaliedoscope", "Kaleidescope", "Kaliedescope"], "correct_answer": 0, "explanation": "\"Kaleidoscope\" has 'ei' after 'l' and ends with '-scope'.", "difficulty": "hard", "concepts": ["greek_compound_words"], "traps": ["i_e_reversal"]},
    {"question": "Choose the correctly spelled word:", "options": ["Labyrinth", "Labyrinth", "Labrynth", "Labirinth"], "correct_answer": 0, "explanation": "\"Labyrinth\" has 'y' after 'b' and ends with 'inth'.", "difficulty": "hard", "concepts": ["mythological_terms"], "traps": ["vowel_substitution"]},
    {"question": "Choose the correctly spelled word:", "options": ["Mnemonic", "Nemonic", "Mnemonik", "Nemonik"], "correct_answer": 0, "explanation": "\"Mnemonic\" starts with silent 'm', has 'ne' after 'm', and ends with '-ic'.", "difficulty": "hard", "concepts": ["silent_consonant_clusters"], "traps": ["initial_silent_letter_omission"]},
    {"question": "Choose the correctly spelled word:", "options": ["Onomatopoeia", "Onomatopeia", "Onomatopoea", "Onomatopoeia"], "correct_answer": 3, "explanation": "\"Onomatopoeia\" ends with '-poeia'.", "difficulty": "hard", "concepts": ["literary_terms"], "traps": ["vowel_sequence_truncation"]},
    {"question": "Choose the correctly spelled word:", "options": ["Paraphernalia", "Paraphenalia", "Paraphernelia", "Paraphernaila"], "correct_answer": 0, "explanation": "\"Paraphernalia\" has 'ph' after 'ara', 'er' after 'ph', and ends with '-nalia'.", "difficulty": "hard", "concepts": ["legal_latin_terms"], "traps": ["ph_f_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Quinoa", "Quinoia", "Keenoa", "Quinoe"], "correct_answer": 0, "explanation": "\"Quinoa\" starts with 'qu', has 'i' after 'qu', and ends with '-oa'.", "difficulty": "hard", "concepts": ["foreign_food_terms"], "traps": ["phonetic_anglicization"]},
    {"question": "Choose the correctly spelled word:", "options": ["Rhododendron", "Rhododrendron", "Rhododedron", "Rhododenderon"], "correct_answer": 0, "explanation": "\"Rhododendron\" has 'do' after 'rho', 'den' after 'do', and ends with '-dron'.", "difficulty": "hard", "concepts": ["botanical_greek_terms"], "traps": ["syllable_repetition_errors"]},
    {"question": "Choose the correctly spelled word:", "options": ["Schipperke", "Shipperke", "Skipperke", "Schiperke"], "correct_answer": 0, "explanation": "\"Schipperke\" has 'sch' start, double 'p', and ends with '-erke'.", "difficulty": "hard", "concepts": ["foreign_breed_names"], "traps": ["english_spelling_analogy"]},
    {"question": "Choose the correctly spelled word:", "options": ["Tchotchke", "Chotchke", "Tchotchkey", "Chotchkey"], "correct_answer": 0, "explanation": "\"Tchotchke\" starts with 'tch', has 'o' after 'tch', and ends with '-ke'.", "difficulty": "hard", "concepts": ["yiddish_loanwords"], "traps": ["initial_consonant_cluster_reduction"]},
    {"question": "Choose the correctly spelled word:", "options": ["Vivisection", "Vivisection", "Vivisection", "Vivisection"], "correct_answer": 0, "explanation": "\"Vivisection\" has 'vi' start, 'vi' again, and ends with '-section'.", "difficulty": "hard", "concepts": ["scientific_terms"], "traps": ["prefix_root_confusion"]},
    {"question": "Choose the correctly spelled word:", "options": ["Xylem", "Zylem", "Xilem", "Zilem"], "correct_answer": 0, "explanation": "\"Xylem\" starts with 'x', has 'y' after 'x', and ends with '-lem'.", "difficulty": "hard", "concepts": ["botanical_scientific_terms"], "traps": ["initial_x_z_confusion"]}
]

for q_data in questions:
    q = AptitudeQuestion(
        id=str(uuid.uuid4()),
        question=q_data["question"],
        options=q_data["options"],
        correct_answer=q_data["correct_answer"],
        answer_explanation=q_data["explanation"],
        topic="Spelling",
        category="Verbal Ability",
        difficulty=q_data["difficulty"],
        source="hardcoded",
        primary_concepts=q_data["concepts"],
        trap_explanation=f"Common traps: {', '.join(q_data['traps'])}" if q_data["traps"] else None
    )
    session.add(q)

session.commit()
print(f"Successfully seeded {len(questions)} Spelling questions.")
session.close()
