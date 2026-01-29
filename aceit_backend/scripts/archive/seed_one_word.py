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
    {"question": "A person who loves mankind", "options": ["Misanthrope", "Philanthropist", "Patriot", "Humanist"], "correct_answer": 1, "explanation": "Philanthropist = lover of mankind; philanthropist actively helps people.", "difficulty": "easy", "concepts": ["human_relationships"], "traps": ["misanthrope_antonym_confusion"]},
    {"question": "A person who hates mankind", "options": ["Philanthropist", "Misanthrope", "Humanist", "Patriot"], "correct_answer": 1, "explanation": "Misanthrope = hater of mankind.", "difficulty": "easy", "concepts": ["human_relationships"], "traps": ["similar_sounding_words"]},
    {"question": "One who cannot read or write", "options": ["Illiterate", "Ignorant", "Uneducated", "Illogical"], "correct_answer": 0, "explanation": "Illiterate = unable to read or write.", "difficulty": "easy", "concepts": ["education_status"], "traps": ["general_ignorance_confusion"]},
    {"question": "A person who loves himself/herself", "options": ["Narcissist", "Egotist", "Selfish", "Proud"], "correct_answer": 0, "explanation": "Narcissist = person with excessive self-love.", "difficulty": "easy", "concepts": ["self_orientation"], "traps": ["egotist_vs_narcissist_distinction"]},
    {"question": "Government by the people", "options": ["Autocracy", "Democracy", "Oligarchy", "Monarchy"], "correct_answer": 1, "explanation": "Democracy = government by the people.", "difficulty": "easy", "concepts": ["government_types"], "traps": ["similar_sounding_terms"]},
    {"question": "Government by one person", "options": ["Democracy", "Autocracy", "Oligarchy", "Bureaucracy"], "correct_answer": 1, "explanation": "Autocracy = government by one person with absolute power.", "difficulty": "easy", "concepts": ["government_types"], "traps": ["monarchy_vs_autocracy_confusion"]},
    {"question": "A person who travels to work daily", "options": ["Tourist", "Commuter", "Traveler", "Visitor"], "correct_answer": 1, "explanation": "Commuter = person who travels regularly between home and work.", "difficulty": "easy", "concepts": ["daily_activities"], "traps": ["general_travel_terms"]},
    {"question": "A person who looks on the bright side of things", "options": ["Pessimist", "Optimist", "Realist", "Idealist"], "correct_answer": 1, "explanation": "Optimist = person who is hopeful about the future.", "difficulty": "easy", "concepts": ["outlook_types"], "traps": ["pessimist_antonym"]},
    {"question": "A person who looks on the dark side of things", "options": ["Optimist", "Pessimist", "Realist", "Cynic"], "correct_answer": 1, "explanation": "Pessimist = person who expects the worst.", "difficulty": "easy", "concepts": ["outlook_types"], "traps": ["cynic_vs_pessimist_distinction"]},
    {"question": "A place where birds are kept", "options": ["Aquarium", "Aviary", "Zoo", "Sanctuary"], "correct_answer": 1, "explanation": "Aviary = large enclosure for keeping birds.", "difficulty": "easy", "concepts": ["animal_housing"], "traps": ["aquarium_water_confusion"]},
    {"question": "A place where fish are kept", "options": ["Aviary", "Aquarium", "Terrarium", "Vivarium"], "correct_answer": 1, "explanation": "Aquarium = tank for keeping fish and other aquatic life.", "difficulty": "easy", "concepts": ["animal_housing"], "traps": ["terrarium_land_confusion"]},
    {"question": "A person who loves books", "options": ["Bibliophile", "Bibliographer", "Librarian", "Scholar"], "correct_answer": 0, "explanation": "Bibliophile = lover of books.", "difficulty": "easy", "concepts": ["interests_hobbies"], "traps": ["book_related_professions"]},
    {"question": "A person who is present everywhere", "options": ["Omniscient", "Omnipotent", "Omnipresent", "Omnivorous"], "correct_answer": 2, "explanation": "Omnipresent = present everywhere at the same time.", "difficulty": "easy", "concepts": ["divine_attributes"], "traps": ["omni_prefix_confusion"]},
    {"question": "A person who knows everything", "options": ["Omnipresent", "Omnipotent", "Omniscient", "Omnivorous"], "correct_answer": 2, "explanation": "Omniscient = knowing everything.", "difficulty": "easy", "concepts": ["divine_attributes"], "traps": ["omni_prefix_confusion"]},
    {"question": "A person who can eat anything", "options": ["Omniscient", "Omnipotent", "Omnipresent", "Omnivorous"], "correct_answer": 3, "explanation": "Omnivorous = eating both plant and animal food.", "difficulty": "easy", "concepts": ["eating_habits"], "traps": ["omni_prefix_confusion"]},
    {"question": "A person who is all powerful", "options": ["Omniscient", "Omnipotent", "Omnipresent", "Omnivorous"], "correct_answer": 1, "explanation": "Omnipotent = having unlimited power.", "difficulty": "easy", "concepts": ["divine_attributes"], "traps": ["omni_prefix_confusion"]},
    {"question": "A person who lives alone and avoids people", "options": ["Extrovert", "Introvert", "Recluse", "Hermit"], "correct_answer": 3, "explanation": "Hermit = person living in solitude for religious reasons; recluse = person living in solitude.", "difficulty": "easy", "concepts": ["social_behavior"], "traps": ["introvert_extrovert_confusion"]},
    {"question": "A person who speaks many languages", "options": ["Linguist", "Polyglot", "Grammarian", "Translator"], "correct_answer": 1, "explanation": "Polyglot = person who knows and uses several languages.", "difficulty": "easy", "concepts": ["language_ability"], "traps": ["linguist_profession_confusion"]},
    {"question": "A person who is new to a profession", "options": ["Expert", "Novice", "Master", "Veteran"], "correct_answer": 1, "explanation": "Novice = person new to a field or activity.", "difficulty": "easy", "concepts": ["experience_level"], "traps": ["antonym_distraction"]},
    {"question": "A person who is over 100 years old", "options": ["Centenarian", "Nonagenarian", "Octogenarian", "Septuagenarian"], "correct_answer": 0, "explanation": "Centenarian = person who is 100 years old or more.", "difficulty": "easy", "concepts": ["age_terms"], "traps": ["other_age_terms_confusion"]},

    # MEDIUM (20)
    {"question": "A person who pretends to be what he is not", "options": ["Imposter", "Actor", "Hypocrite", "Deceiver"], "correct_answer": 0, "explanation": "Imposter = person who pretends to be someone else; hypocrite = person who pretends to have virtues/morals.", "difficulty": "medium", "concepts": ["deception_types"], "traps": ["hypocrite_moral_pretension"]},
    {"question": "The practice of marrying one person at a time", "options": ["Polygamy", "Monogamy", "Bigamy", "Polyandry"], "correct_answer": 1, "explanation": "Monogamy = practice of marrying one person at a time.", "difficulty": "medium", "concepts": ["marriage_systems"], "traps": ["polygamy_bigamy_confusion"]},
    {"question": "The practice of having multiple spouses", "options": ["Monogamy", "Polygamy", "Bigamy", "Celibacy"], "correct_answer": 1, "explanation": "Polygamy = practice of having multiple spouses.", "difficulty": "medium", "concepts": ["marriage_systems"], "traps": ["bigamy_illegal_specific"]},
    {"question": "The practice of having two wives or husbands", "options": ["Polygamy", "Bigamy", "Monogamy", "Polyandry"], "correct_answer": 1, "explanation": "Bigamy = offense of marrying someone while already married.", "difficulty": "medium", "concepts": ["marriage_systems"], "traps": ["polygamy_general_term"]},
    {"question": "A person who walks in sleep", "options": ["Insomniac", "Somnambulist", "Narcotic", "Dreamer"], "correct_answer": 1, "explanation": "Somnambulist = sleepwalker.", "difficulty": "medium", "concepts": ["sleep_disorders"], "traps": ["latin_root_words"]},
    {"question": "A person who cannot sleep", "options": ["Somnambulist", "Insomniac", "Narcoleptic", "Hypnotic"], "correct_answer": 1, "explanation": "Insomniac = person who cannot sleep.", "difficulty": "medium", "concepts": ["sleep_disorders"], "traps": ["similar_sleep_terms"]},
    {"question": "A person who loves and collects books", "options": ["Bibliographer", "Bibliophile", "Librarian", "Bibliomaniac"], "correct_answer": 3, "explanation": "Bibliomaniac = obsessive collector of books.", "difficulty": "medium", "concepts": ["book_collecting"], "traps": ["bibliophile_lover_not_collector"]},
    {"question": "Fear of closed spaces", "options": ["Claustrophobia", "Agoraphobia", "Acrophobia", "Hydrophobia"], "correct_answer": 0, "explanation": "Claustrophobia = fear of confined spaces.", "difficulty": "medium", "concepts": ["phobias"], "traps": ["agoraphobia_open_spaces"]},
    {"question": "Fear of open spaces", "options": ["Claustrophobia", "Agoraphobia", "Acrophobia", "Xenophobia"], "correct_answer": 1, "explanation": "Agoraphobia = fear of open or public spaces.", "difficulty": "medium", "concepts": ["phobias"], "traps": ["claustrophobia_opposite"]},
    {"question": "Fear of heights", "options": ["Hydrophobia", "Acrophobia", "Agoraphobia", "Claustrophobia"], "correct_answer": 1, "explanation": "Acrophobia = fear of heights.", "difficulty": "medium", "concepts": ["phobias"], "traps": ["similar_sounding_phobias"]},
    {"question": "Fear of water", "options": ["Acrophobia", "Hydrophobia", "Xenophobia", "Agoraphobia"], "correct_answer": 1, "explanation": "Hydrophobia = fear of water (also rabies symptom).", "difficulty": "medium", "concepts": ["phobias"], "traps": ["medical_condition_confusion"]},
    {"question": "Fear of foreigners", "options": ["Xenophobia", "Hydrophobia", "Acrophobia", "Claustrophobia"], "correct_answer": 0, "explanation": "Xenophobia = fear or hatred of foreigners.", "difficulty": "medium", "concepts": ["phobias"], "traps": ["social_attitude_vs_phobia"]},
    {"question": "A person who compiles dictionaries", "options": ["Lexicographer", "Linguist", "Etymologist", "Philologist"], "correct_answer": 0, "explanation": "Lexicographer = compiler of dictionaries.", "difficulty": "medium", "concepts": ["language_professions"], "traps": ["other_language_specialists"]},
    {"question": "A person who studies word origins", "options": ["Lexicographer", "Etymologist", "Philologist", "Linguist"], "correct_answer": 1, "explanation": "Etymologist = person who studies word origins.", "difficulty": "medium", "concepts": ["language_professions"], "traps": ["philologist_language_study"]},
    {"question": "A person who is indifferent to pleasure or pain", "options": ["Hedonist", "Stoic", "Ascetic", "Epicurean"], "correct_answer": 1, "explanation": "Stoic = person indifferent to pleasure or pain.", "difficulty": "medium", "concepts": ["philosophical_attitudes"], "traps": ["ascetic_self_denial"]},
    {"question": "A person who denies himself luxuries", "options": ["Stoic", "Ascetic", "Hedonist", "Epicure"], "correct_answer": 1, "explanation": "Ascetic = person who practices severe self-discipline.", "difficulty": "medium", "concepts": ["lifestyle_choices"], "traps": ["stoic_indifference_vs_ascetic_denial"]},
    {"question": "A person who believes in the existence of God", "options": ["Atheist", "Theist", "Agnostic", "Deist"], "correct_answer": 1, "explanation": "Theist = person who believes in the existence of God/gods.", "difficulty": "medium", "concepts": ["religious_beliefs"], "traps": ["deist_specific_belief"]},
    {"question": "A person who does not believe in the existence of God", "options": ["Theist", "Atheist", "Agnostic", "Deist"], "correct_answer": 1, "explanation": "Atheist = person who does not believe in the existence of God.", "difficulty": "medium", "concepts": ["religious_beliefs"], "traps": ["agnostic_uncertainty"]},
    {"question": "A person who is unsure about God's existence", "options": ["Atheist", "Theist", "Agnostic", "Deist"], "correct_answer": 2, "explanation": "Agnostic = person who believes nothing is known or can be known of God.", "difficulty": "medium", "concepts": ["religious_beliefs"], "traps": ["atheist_theist_binary"]},
    {"question": "A person who believes God created but doesn't intervene", "options": ["Theist", "Deist", "Agnostic", "Pantheist"], "correct_answer": 1, "explanation": "Deist = person who believes God created but doesn't intervene.", "difficulty": "medium", "concepts": ["religious_beliefs"], "traps": ["theist_general_belief"]},

    # HARD (20)
    {"question": "A person who believes God is in everything", "options": ["Deist", "Pantheist", "Polytheist", "Monotheist"], "correct_answer": 1, "explanation": "Pantheist = person who believes God is in everything.", "difficulty": "hard", "concepts": ["religious_beliefs"], "traps": ["polytheist_multiple_gods"]},
    {"question": "Government by the wealthy", "options": ["Plutocracy", "Aristocracy", "Oligarchy", "Timocracy"], "correct_answer": 0, "explanation": "Plutocracy = government by the wealthy.", "difficulty": "hard", "concepts": ["government_types"], "traps": ["aristocracy_nobility"]},
    {"question": "Government by the nobility", "options": ["Plutocracy", "Aristocracy", "Oligarchy", "Theocracy"], "correct_answer": 1, "explanation": "Aristocracy = government by the nobility.", "difficulty": "hard", "concepts": ["government_types"], "traps": ["oligarchy_few_rulers"]},
    {"question": "Government by religious leaders", "options": ["Theocracy", "Plutocracy", "Aristocracy", "Bureaucracy"], "correct_answer": 0, "explanation": "Theocracy = government by religious leaders.", "difficulty": "hard", "concepts": ["government_types"], "traps": ["hierarchy_confusion"]},
    {"question": "A person who is 80-89 years old", "options": ["Septuagenarian", "Octogenarian", "Nonagenarian", "Centenarian"], "correct_answer": 1, "explanation": "Octogenarian = person aged 80-89.", "difficulty": "hard", "concepts": ["age_terms"], "traps": ["other_decade_terms"]},
    {"question": "A person who is 70-79 years old", "options": ["Octogenarian", "Septuagenarian", "Nonagenarian", "Sexagenarian"], "correct_answer": 1, "explanation": "Septuagenarian = person aged 70-79.", "difficulty": "hard", "concepts": ["age_terms"], "traps": ["latin_number_confusion"]},
    {"question": "A person who is 90-99 years old", "options": ["Octogenarian", "Nonagenarian", "Centenarian", "Septuagenarian"], "correct_answer": 1, "explanation": "Nonagenarian = person aged 90-99.", "difficulty": "hard", "concepts": ["age_terms"], "traps": ["centenarian_100_confusion"]},
    {"question": "A person who loves trees", "options": ["Arborist", "Dendrophile", "Botanist", "Horticulturist"], "correct_answer": 1, "explanation": "Dendrophile = lover of trees.", "difficulty": "hard", "concepts": ["nature_lovers"], "traps": ["tree_professions"]},
    {"question": "A person who studies trees", "options": ["Dendrophile", "Dendrologist", "Botanist", "Arborist"], "correct_answer": 1, "explanation": "Dendrologist = person who studies trees.", "difficulty": "hard", "concepts": ["scientific_studies"], "traps": ["dendrophile_lover_not_student"]},
    {"question": "A person who studies rocks", "options": ["Geologist", "Petrologist", "Mineralogist", "Archaeologist"], "correct_answer": 1, "explanation": "Petrologist = person who studies rocks (geology = broader earth study).", "difficulty": "hard", "concepts": ["scientific_studies"], "traps": ["geology_broader_field"]},
    {"question": "A person who studies coins", "options": ["Numismatist", "Philatelist", "Archaeologist", "Historian"], "correct_answer": 0, "explanation": "Numismatist = person who studies or collects coins.", "difficulty": "hard", "concepts": ["collection_studies"], "traps": ["philatelist_stamps_confusion"]},
    {"question": "A person who studies stamps", "options": ["Numismatist", "Philatelist", "Archaeologist", "Epigraphist"], "correct_answer": 1, "explanation": "Philatelist = person who studies or collects stamps.", "difficulty": "hard", "concepts": ["collection_studies"], "traps": ["numismatist_coins_confusion"]},
    {"question": "A person who studies handwriting", "options": ["Calligrapher", "Graphologist", "Typographer", "Palaeographer"], "correct_answer": 1, "explanation": "Graphologist = person who studies handwriting.", "difficulty": "hard", "concepts": ["writing_studies"], "traps": ["calligrapher_artist"]},
    {"question": "A person who studies ancient writing", "options": ["Graphologist", "Palaeographer", "Calligrapher", "Epigraphist"], "correct_answer": 1, "explanation": "Palaeographer = person who studies ancient writing.", "difficulty": "hard", "concepts": ["writing_studies"], "traps": ["epigraphist_inscriptions"]},
    {"question": "A person who eats human flesh", "options": ["Carnivore", "Cannibal", "Herbivore", "Omnivore"], "correct_answer": 1, "explanation": "Cannibal = person who eats human flesh.", "difficulty": "hard", "concepts": ["eating_habits"], "traps": ["carnivore_meat_eater"]},
    {"question": "A person who loves money", "options": ["Miser", "Philanthropist", "Plutocrat", "Avaricious"], "correct_answer": 3, "explanation": "Avaricious = having extreme greed for wealth.", "difficulty": "hard", "concepts": ["wealth_attitudes"], "traps": ["miser_hoarder_not_lover"]},
    {"question": "A person who hates marriage", "options": ["Misogamist", "Misogynist", "Misanthropist", "Monogamist"], "correct_answer": 0, "explanation": "Misogamist = person who hates marriage.", "difficulty": "hard", "concepts": ["marriage_attitudes"], "traps": ["misogynist_women_hater"]},
    {"question": "A person who hates women", "options": ["Misogamist", "Misogynist", "Misanthropist", "Feminist"], "correct_answer": 1, "explanation": "Misogynist = person who hates women.", "difficulty": "hard", "concepts": ["gender_attitudes"], "traps": ["misogamist_marriage_hater"]},
    {"question": "A person who hates men", "options": ["Misandrist", "Misogynist", "Feminist", "Misanthropist"], "correct_answer": 0, "explanation": "Misandrist = person who hates men.", "difficulty": "hard", "concepts": ["gender_attitudes"], "traps": ["feminist_equality_confusion"]},
    {"question": "A person who loves the sound of their own voice", "options": ["Narcissist", "Egotist", "Logophile", "Philologist"], "correct_answer": 1, "explanation": "Egotist = person excessively conceited or absorbed in themselves.", "difficulty": "hard", "concepts": ["self_orientation"], "traps": ["narcissist_self_love_general"]}
]

for q_data in questions:
    q = AptitudeQuestion(
        id=str(uuid.uuid4()),
        question=q_data["question"],
        options=q_data["options"],
        correct_answer=q_data["correct_answer"],
        answer_explanation=q_data["explanation"],
        topic="One Word Substitution",
        category="Verbal Ability",
        difficulty=q_data["difficulty"],
        source="hardcoded",
        primary_concepts=q_data["concepts"],
        trap_explanation=f"Common traps: {', '.join(q_data['traps'])}" if q_data["traps"] else None
    )
    session.add(q)

session.commit()
print(f"Successfully seeded {len(questions)} One Word Substitution questions.")
session.close()
