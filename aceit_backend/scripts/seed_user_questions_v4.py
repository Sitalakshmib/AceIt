"""
Seed User Provided Questions (Verbal Ability Focus):
Adds a set of high-quality manual Verbal Ability questions provided by the user.
"""

import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

VERBAL_QUESTIONS = [
  {
    "category": "Verbal Ability",
    "topic": "Synonyms",
    "difficulty": "easy",
    "question": "Choose the synonym of the word 'Happy'.",
    "options": ["Sad", "Joyful", "Angry", "Tired"],
    "correct_answer": 1,
    "answer_explanation": "'Joyful' means feeling or showing happiness."
  },
  {
    "category": "Verbal Ability",
    "topic": "Antonyms",
    "difficulty": "easy",
    "question": "Choose the antonym of the word 'Brave'.",
    "options": ["Bold", "Fearless", "Cowardly", "Strong"],
    "correct_answer": 2,
    "answer_explanation": "'Cowardly' means lacking courage."
  },
  {
    "category": "Verbal Ability",
    "topic": "Fill in the Blanks",
    "difficulty": "easy",
    "question": "She is very good ___ mathematics.",
    "options": ["at", "in", "on", "with"],
    "correct_answer": 0,
    "answer_explanation": "The correct preposition is 'good at'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Vocabulary",
    "difficulty": "easy",
    "question": "Choose the correct meaning of the word 'Fragile'.",
    "options": ["Strong", "Delicate", "Heavy", "Hard"],
    "correct_answer": 1,
    "answer_explanation": "'Fragile' means easily broken or delicate."
  },
  {
    "category": "Verbal Ability",
    "topic": "Sentence Improvement",
    "difficulty": "easy",
    "question": "He did not knew the answer.",
    "options": [
      "He did not know the answer.",
      "He did not knowing the answer.",
      "He does not knew the answer.",
      "No improvement"
    ],
    "correct_answer": 0,
    "answer_explanation": "After 'did not', base form of verb is used."
  },
  {
    "category": "Verbal Ability",
    "topic": "Synonyms",
    "difficulty": "medium",
    "question": "Choose the synonym of the word 'Abundant'.",
    "options": ["Scarce", "Plenty", "Rare", "Little"],
    "correct_answer": 1,
    "answer_explanation": "'Abundant' means available in large quantities."
  },
  {
    "category": "Verbal Ability",
    "topic": "Antonyms",
    "difficulty": "medium",
    "question": "Choose the antonym of the word 'Transparent'.",
    "options": ["Clear", "Visible", "Opaque", "Bright"],
    "correct_answer": 2,
    "answer_explanation": "'Opaque' means not transparent."
  },
  {
    "category": "Verbal Ability",
    "topic": "Fill in the Blanks",
    "difficulty": "medium",
    "question": "Neither of the answers ___ correct.",
    "options": ["are", "were", "is", "have"],
    "correct_answer": 2,
    "answer_explanation": "'Neither' takes a singular verb."
  },
  {
    "category": "Verbal Ability",
    "topic": "Error Spotting",
    "difficulty": "medium",
    "question": "Identify the error: She has been working here since five years.",
    "options": ["has been", "working", "since", "five years"],
    "correct_answer": 2,
    "answer_explanation": "'Since' is used with a point of time, not a period."
  },
  {
    "category": "Verbal Ability",
    "topic": "Sentence Improvement",
    "difficulty": "medium",
    "question": "The teacher advised the students to work hardly.",
    "options": [
      "to work hard",
      "to work harder",
      "to hardly work",
      "No improvement"
    ],
    "correct_answer": 0,
    "answer_explanation": "'Hardly' means barely; correct word is 'hard'."
  },
  {
    "category": "Verbal Ability",
    "topic": "One Word Substitution",
    "difficulty": "medium",
    "question": "A person who speaks many languages is called:",
    "options": ["Bilingual", "Linguist", "Polyglot", "Translator"],
    "correct_answer": 2,
    "answer_explanation": "'Polyglot' is a person who knows many languages."
  },
  {
    "category": "Verbal Ability",
    "topic": "Reading Comprehension",
    "difficulty": "medium",
    "question": "Reading improves knowledge and vocabulary. It also enhances critical thinking skills. What is the main benefit of reading according to the passage?",
    "options": [
      "Entertainment",
      "Vocabulary only",
      "Knowledge and thinking skills",
      "Writing skills"
    ],
    "correct_answer": 2,
    "answer_explanation": "The passage highlights knowledge and critical thinking."
  },
  {
    "category": "Verbal Ability",
    "topic": "Synonyms",
    "difficulty": "hard",
    "question": "Choose the synonym of the word 'Obsolete'.",
    "options": ["Modern", "Outdated", "Useful", "Current"],
    "correct_answer": 1,
    "answer_explanation": "'Obsolete' means no longer in use or outdated."
  },
  {
    "category": "Verbal Ability",
    "topic": "Antonyms",
    "difficulty": "hard",
    "question": "Choose the antonym of the word 'Concise'.",
    "options": ["Brief", "Short", "Lengthy", "Clear"],
    "correct_answer": 2,
    "answer_explanation": "'Lengthy' is the opposite of concise."
  },
  {
    "category": "Verbal Ability",
    "topic": "Para Jumbles",
    "difficulty": "hard",
    "question": "Rearrange the sentences to form a meaningful paragraph:\nA. He worked hard.\nB. He achieved success.\nC. He had a clear goal.\nD. He planned well.",
    "options": [
      "C-D-A-B",
      "A-C-D-B",
      "D-C-A-B",
      "C-A-D-B"
    ],
    "correct_answer": 0,
    "answer_explanation": "Goal \u2192 planning \u2192 hard work \u2192 success."
  },
  {
    "category": "Verbal Ability",
    "topic": "Error Spotting",
    "difficulty": "hard",
    "question": "Identify the error: Hardly had he reached the station when the train left.",
    "options": ["Hardly", "had he", "reached", "No error"],
    "correct_answer": 3,
    "answer_explanation": "The sentence is grammatically correct."
  },
  {
    "category": "Verbal Ability",
    "topic": "Sentence Completion",
    "difficulty": "hard",
    "question": "No sooner ___ the bell rung than the students left the class.",
    "options": ["had", "has", "did", "was"],
    "correct_answer": 0,
    "answer_explanation": "The structure is 'No sooner had\u2026 than\u2026'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Synonyms",
    "difficulty": "easy",
    "question": "Choose the synonym of the word 'Begin'.",
    "options": ["End", "Start", "Close", "Finish"],
    "correct_answer": 1,
    "answer_explanation": "'Start' means to begin something."
  },
  {
    "category": "Verbal Ability",
    "topic": "Antonyms",
    "difficulty": "easy",
    "question": "Choose the antonym of the word 'Cheap'.",
    "options": ["Costly", "Low", "Easy", "Small"],
    "correct_answer": 0,
    "answer_explanation": "'Costly' is the opposite of cheap."
  },
  {
    "category": "Verbal Ability",
    "topic": "Fill in the Blanks",
    "difficulty": "easy",
    "question": "He is afraid ___ dogs.",
    "options": ["of", "from", "with", "for"],
    "correct_answer": 0,
    "answer_explanation": "The correct preposition is 'afraid of'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Vocabulary",
    "difficulty": "easy",
    "question": "Choose the correct meaning of the word 'Ancient'.",
    "options": ["Modern", "Old", "New", "Future"],
    "correct_answer": 1,
    "answer_explanation": "'Ancient' means very old."
  },
  {
    "category": "Verbal Ability",
    "topic": "Sentence Improvement",
    "difficulty": "easy",
    "question": "She do not like coffee.",
    "options": [
      "She does not like coffee.",
      "She did not like coffee.",
      "She do not likes coffee.",
      "No improvement"
    ],
    "correct_answer": 0,
    "answer_explanation": "Singular subject 'she' takes 'does not'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Synonyms",
    "difficulty": "medium",
    "question": "Choose the synonym of the word 'Reluctant'.",
    "options": ["Eager", "Willing", "Unwilling", "Happy"],
    "correct_answer": 2,
    "answer_explanation": "'Reluctant' means unwilling or hesitant."
  },
  {
    "category": "Verbal Ability",
    "topic": "Antonyms",
    "difficulty": "medium",
    "question": "Choose the antonym of the word 'Permanent'.",
    "options": ["Stable", "Fixed", "Temporary", "Strong"],
    "correct_answer": 2,
    "answer_explanation": "'Temporary' is the opposite of permanent."
  },
  {
    "category": "Verbal Ability",
    "topic": "Fill in the Blanks",
    "difficulty": "medium",
    "question": "He insisted ___ paying the bill himself.",
    "options": ["in", "on", "at", "for"],
    "correct_answer": 1,
    "answer_explanation": "The correct usage is 'insisted on'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Error Spotting",
    "difficulty": "medium",
    "question": "Identify the error: Each of the students have submitted their assignment.",
    "options": ["Each", "of the", "have", "submitted"],
    "correct_answer": 2,
    "answer_explanation": "'Each' is singular, so 'has' should be used."
  },
  {
    "category": "Verbal Ability",
    "topic": "Sentence Improvement",
    "difficulty": "medium",
    "question": "The manager along with his assistants are attending the meeting.",
    "options": [
      "is attending the meeting",
      "were attending the meeting",
      "are attend the meeting",
      "No improvement"
    ],
    "correct_answer": 0,
    "answer_explanation": "Subject is 'manager'; phrase 'along with' does not affect verb."
  },
  {
    "category": "Verbal Ability",
    "topic": "One Word Substitution",
    "difficulty": "medium",
    "question": "A place where books are kept for public reading:",
    "options": ["Museum", "Library", "Archive", "Auditorium"],
    "correct_answer": 1,
    "answer_explanation": "A library is a place for reading and borrowing books."
  },
  {
    "category": "Verbal Ability",
    "topic": "One Word Substitution",
    "difficulty": "medium",
    "question": "One who cannot read or write:",
    "options": ["Scholar", "Illiterate", "Literate", "Reader"],
    "correct_answer": 1,
    "answer_explanation": "Illiterate means unable to read or write."
  },
  {
    "category": "Verbal Ability",
    "topic": "Synonyms",
    "difficulty": "hard",
    "question": "Choose the synonym of the word 'Meticulous'.",
    "options": ["Careless", "Lazy", "Precise", "Hasty"],
    "correct_answer": 2,
    "answer_explanation": "'Meticulous' means very careful and precise."
  },
  {
    "category": "Verbal Ability",
    "topic": "Antonyms",
    "difficulty": "hard",
    "question": "Choose the antonym of the word 'Hostile'.",
    "options": ["Friendly", "Angry", "Rude", "Violent"],
    "correct_answer": 0,
    "answer_explanation": "'Friendly' is the opposite of hostile."
  },
  {
    "category": "Verbal Ability",
    "topic": "Para Jumbles",
    "difficulty": "hard",
    "question": "Rearrange the sentences:\nA. The exam was difficult.\nB. Many students prepared well.\nC. As a result, most students passed.\nD. They studied regularly.",
    "options": [
      "A-B-D-C",
      "B-D-A-C",
      "A-D-B-C",
      "D-B-A-C"
    ],
    "correct_answer": 1,
    "answer_explanation": "Preparation \u2192 study \u2192 difficulty \u2192 result."
  },
  {
    "category": "Verbal Ability",
    "topic": "Error Spotting",
    "difficulty": "hard",
    "question": "Identify the error: Scarcely had the train arrived when the passengers rushed out.",
    "options": ["Scarcely", "had the train", "rushed", "No error"],
    "correct_answer": 3,
    "answer_explanation": "The sentence structure is grammatically correct."
  },
  {
    "category": "Verbal Ability",
    "topic": "Sentence Completion",
    "difficulty": "hard",
    "question": "Had she known about the traffic, she ___ earlier.",
    "options": ["will leave", "would leave", "would have left", "had left"],
    "correct_answer": 2,
    "answer_explanation": "Third conditional: 'would have + past participle'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Synonyms",
    "difficulty": "easy",
    "question": "Choose the synonym of the word 'Quick'.",
    "options": ["Slow", "Rapid", "Late", "Lazy"],
    "correct_answer": 1,
    "answer_explanation": "'Rapid' means fast or quick."
  },
  {
    "category": "Verbal Ability",
    "topic": "Antonyms",
    "difficulty": "easy",
    "question": "Choose the antonym of the word 'Strong'.",
    "options": ["Powerful", "Weak", "Firm", "Healthy"],
    "correct_answer": 1,
    "answer_explanation": "'Weak' is the opposite of strong."
  },
  {
    "category": "Verbal Ability",
    "topic": "Fill in the Blanks",
    "difficulty": "easy",
    "question": "He prefers tea ___ coffee.",
    "options": ["than", "to", "over", "with"],
    "correct_answer": 1,
    "answer_explanation": "The correct usage is 'prefer X to Y'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Vocabulary",
    "difficulty": "easy",
    "question": "Choose the correct meaning of the word 'Generous'.",
    "options": ["Selfish", "Kind", "Greedy", "Angry"],
    "correct_answer": 1,
    "answer_explanation": "'Generous' means kind and willing to give."
  },
  {
    "category": "Verbal Ability",
    "topic": "Sentence Improvement",
    "difficulty": "easy",
    "question": "She did not completed the work.",
    "options": [
      "She did not complete the work.",
      "She has not completed the work.",
      "She did not completing the work.",
      "No improvement"
    ],
    "correct_answer": 0,
    "answer_explanation": "After 'did not', the base form of the verb is used."
  },
  {
    "category": "Verbal Ability",
    "topic": "Synonyms",
    "difficulty": "medium",
    "question": "Choose the synonym of the word 'Cautious'.",
    "options": ["Careless", "Alert", "Brave", "Rude"],
    "correct_answer": 1,
    "answer_explanation": "'Cautious' means careful and alert."
  },
  {
    "category": "Verbal Ability",
    "topic": "Antonyms",
    "difficulty": "medium",
    "question": "Choose the antonym of the word 'Expand'.",
    "options": ["Increase", "Grow", "Contract", "Develop"],
    "correct_answer": 2,
    "answer_explanation": "'Contract' means to become smaller."
  },
  {
    "category": "Verbal Ability",
    "topic": "Fill in the Blanks",
    "difficulty": "medium",
    "question": "No sooner ___ the rain started than the match was stopped.",
    "options": ["did", "had", "has", "was"],
    "correct_answer": 1,
    "answer_explanation": "The correct structure is 'No sooner had\u2026 than\u2026'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Error Spotting",
    "difficulty": "medium",
    "question": "Identify the error: He is one of the best player in the team.",
    "options": ["He is", "one of the", "best player", "in the team"],
    "correct_answer": 2,
    "answer_explanation": "'One of the' should be followed by a plural noun: 'best players'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Sentence Improvement",
    "difficulty": "medium",
    "question": "The news were shocking.",
    "options": [
      "The news was shocking.",
      "The news are shocking.",
      "The news has shocking.",
      "No improvement"
    ],
    "correct_answer": 0,
    "answer_explanation": "'News' is treated as a singular noun."
  },
  {
    "category": "Verbal Ability",
    "topic": "One Word Substitution",
    "difficulty": "medium",
    "question": "A person who writes poems:",
    "options": ["Author", "Poet", "Editor", "Publisher"],
    "correct_answer": 1,
    "answer_explanation": "A poet is someone who writes poems."
  },
  {
    "category": "Verbal Ability",
    "topic": "One Word Substitution",
    "difficulty": "medium",
    "question": "A person who speaks very little:",
    "options": ["Talkative", "Silent", "Taciturn", "Mute"],
    "correct_answer": 2,
    "answer_explanation": "'Taciturn' means habitually silent."
  },
  {
    "category": "Verbal Ability",
    "topic": "Synonyms",
    "difficulty": "hard",
    "question": "Choose the synonym of the word 'Eloquent'.",
    "options": ["Silent", "Confused", "Fluent", "Rough"],
    "correct_answer": 2,
    "answer_explanation": "'Eloquent' means fluent or persuasive in speaking."
  },
  {
    "category": "Verbal Ability",
    "topic": "Antonyms",
    "difficulty": "hard",
    "question": "Choose the antonym of the word 'Scarce'.",
    "options": ["Rare", "Limited", "Abundant", "Few"],
    "correct_answer": 2,
    "answer_explanation": "'Abundant' means plentiful."
  },
  {
    "category": "Verbal Ability",
    "topic": "Para Jumbles",
    "difficulty": "hard",
    "question": "Rearrange the sentences:\nA. He applied for many jobs.\nB. He finally got selected.\nC. He improved his skills.\nD. He faced several rejections.",
    "options": [
      "A-D-C-B",
      "C-A-D-B",
      "A-C-D-B",
      "D-A-C-B"
    ],
    "correct_answer": 2,
    "answer_explanation": "Application \u2192 skill improvement \u2192 rejections \u2192 selection."
  },
  {
    "category": "Verbal Ability",
    "topic": "Error Spotting",
    "difficulty": "hard",
    "question": "Identify the error: The teacher as well as the students were present.",
    "options": ["The teacher", "as well as", "were present", "No error"],
    "correct_answer": 2,
    "answer_explanation": "The verb should agree with 'teacher' \u2192 'was present'."
  },
  {
    "category": "Verbal Ability",
    "topic": "Sentence Completion",
    "difficulty": "hard",
    "question": "Had they informed us earlier, we ___ alternate arrangements.",
    "options": ["will make", "would make", "would have made", "had made"],
    "correct_answer": 2,
    "answer_explanation": "Third conditional requires 'would have + past participle'."
  }
]

def seed_questions():
    db = SessionLocal()
    try:
        print(f"Seeding {len(VERBAL_QUESTIONS)} manual Verbal Ability questions...")
        added = 0
        for q_data in VERBAL_QUESTIONS:
            exists = db.query(AptitudeQuestion).filter(AptitudeQuestion.question == q_data["question"]).first()
            if not exists:
                new_q = AptitudeQuestion(**q_data)
                db.add(new_q)
                added += 1
            
        db.commit()
        print(f"Seeding complete. Added {added} new questions.")
        
        total = db.query(AptitudeQuestion).count()
        print(f"Total questions now in database: {total}")
        
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions()
