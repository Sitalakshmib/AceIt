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
    {"question": "If P is true and Q is false, what is the truth value of \"P AND Q\"?", "options": ["True", "False", "Cannot be determined", "Neither"], "correct_answer": 1, "explanation": "AND is true only if both operands are true.", "difficulty": "easy"},
    {"question": "Statement: \"If it rains, the match is cancelled.\"\nIt is raining. What can be concluded?", "options": ["Match is cancelled", "Match is not cancelled", "Match may or may not be cancelled", "No conclusion"], "correct_answer": 0, "explanation": "Given condition satisfied, so result follows.", "difficulty": "easy"},
    {"question": "\"Either A or B\" is false. If A is false, then B is:", "options": ["True", "False", "Cannot say", "Invalid statement"], "correct_answer": 1, "explanation": "\"Either A or B\" (XOR) false means both have same truth value.", "difficulty": "easy"},
    {"question": "What is the negation of \"All cats are black\"?", "options": ["No cats are black", "Some cats are not black", "Some cats are black", "All cats are not black"], "correct_answer": 1, "explanation": "Negation of \"All S are P\" is \"Some S are not P\".", "difficulty": "easy"},
    {"question": "\"If X, then Y\" is logically equivalent to:", "options": ["If not Y, then not X", "If Y, then X", "If not X, then not Y", "X AND Y"], "correct_answer": 0, "explanation": "Contrapositive is equivalent.", "difficulty": "easy"},
    {"question": "Truth value of \"P OR NOT P\" is always:", "options": ["True", "False", "Depends on P", "Invalid"], "correct_answer": 0, "explanation": "Tautology.", "difficulty": "easy"},
    {"question": "Statement: \"You will pass only if you study hard.\"\nWhich is correct interpretation?", "options": ["If you study hard, you will pass", "If you pass, you studied hard", "Studying hard and passing are same", "None"], "correct_answer": 1, "explanation": "\"A only if B\" means B is necessary for A.", "difficulty": "easy"},
    {"question": "\"If A then B\" is false when:", "options": ["A true, B true", "A true, B false", "A false, B true", "A false, B false"], "correct_answer": 1, "explanation": "Only false when antecedent true, consequent false.", "difficulty": "easy"},
    {"question": "\"P UNLESS Q\" means logically:", "options": ["If not Q, then P", "If Q, then not P", "P OR Q", "P AND Q"], "correct_answer": 0, "explanation": "P unless Q = If not Q, then P.", "difficulty": "easy"},
    {"question": "All roses are flowers. Some flowers fade quickly. Therefore:", "options": ["Some roses fade quickly", "All roses fade quickly", "No conclusion about roses fading", "Some roses do not fade"], "correct_answer": 2, "explanation": "No direct link between roses and fading.", "difficulty": "easy"},
    {"question": "\"None of the students are lazy\" is equivalent to:", "options": ["All students are not lazy", "Some students are lazy", "Some students are not lazy", "All students are lazy"], "correct_answer": 0, "explanation": "\"No S are P\" equals \"All S are not P\".", "difficulty": "easy"},
    {"question": "\"P is necessary for Q\" means:", "options": ["If P, then Q", "If Q, then P", "P if and only if Q", "Neither"], "correct_answer": 1, "explanation": "P necessary for Q means Q cannot happen without P.", "difficulty": "easy"},
    {"question": "Negation of \"Some men are honest\":", "options": ["All men are honest", "No men are honest", "Some men are not honest", "All men are not honest"], "correct_answer": 3, "explanation": "Negation of \"Some S are P\" is \"No S are P\".", "difficulty": "easy"},
    {"question": "\"If and only if\" is true when:", "options": ["Both same truth value", "Both true", "Both false", "Different truth values"], "correct_answer": 0, "explanation": "Biconditional true when both equal.", "difficulty": "easy"},
    {"question": "\"Not (A OR B)\" is equivalent to:", "options": ["Not A OR Not B", "Not A AND Not B", "A AND B", "A OR B"], "correct_answer": 1, "explanation": "De Morgan's Law.", "difficulty": "easy"},
    {"question": "Statement: All athletes are fit. Rohan is fit. Conclusion:", "options": ["Rohan is athlete", "Rohan may or may not be athlete", "Rohan is not athlete", "None"], "correct_answer": 1, "explanation": "Fit does not imply athlete.", "difficulty": "easy"},
    {"question": "\"Either he is guilty or he is not guilty\" is:", "options": ["Tautology", "Contradiction", "Contingency", "Fallacy"], "correct_answer": 0, "explanation": "Always true.", "difficulty": "easy"},
    {"question": "\"All that glitters is gold\" – negation is:", "options": ["Nothing that glitters is gold", "Some that glitter are not gold", "Some gold does not glitter", "None"], "correct_answer": 1, "explanation": "Negation of universal affirmative.", "difficulty": "easy"},
    {"question": "\"If it is a square, then it has four sides\" – contrapositive is:", "options": ["If four sides, then square", "If not square, then not four sides", "If not four sides, then not square", "None"], "correct_answer": 2, "explanation": "Contrapositive of \"If P then Q\" is \"If not Q then not P\".", "difficulty": "easy"},
    {"question": "\"P only if Q\" and \"P if Q\" together mean:", "options": ["P AND Q", "P OR Q", "P if and only if Q", "Not P"], "correct_answer": 2, "explanation": "Both together give biconditional.", "difficulty": "easy"},

    # MEDIUM (20)
    {"question": "Given: If A then B. If B then C. A is true. What follows?", "options": ["C is true", "C is false", "C may be true or false", "B is false"], "correct_answer": 0, "explanation": "Chain: A \u2192 B \u2192 C, A true \u21d2 B true \u21d2 C true.", "difficulty": "medium"},
    {"question": "Statement: All managers are graduates. Some graduates are poets. Conclusion:", "options": ["Some managers are poets", "Some poets are managers", "No manager is poet", "None of the above"], "correct_answer": 3, "explanation": "No direct relation between managers and poets.", "difficulty": "medium"},
    {"question": "\"Unless you work hard, you will fail\" means logically:", "options": ["If you work hard, you will not fail", "If you fail, you did not work hard", "If you do not work hard, you will fail", "Both 2 and 3"], "correct_answer": 2, "explanation": "\"Unless A, B\" means \"If not A, then B\".", "difficulty": "medium"},
    {"question": "If \"All philosophers are thinkers\" is true, which must be false?", "options": ["Some philosophers are not thinkers", "Some thinkers are philosophers", "No philosopher is a thinker", "Some non-thinkers are philosophers"], "correct_answer": 0, "explanation": "Contradicts the given.", "difficulty": "medium"},
    {"question": "\"Either the company innovates or it perishes. It is not perishing.\" What follows?", "options": ["It is innovating", "It is not innovating", "It may innovate", "Cannot say"], "correct_answer": 0, "explanation": "Exclusive OR; one must be true, not perishing \u21d2 innovating.", "difficulty": "medium"},
    {"question": "Given: P \u2192 Q, \u00acQ \u2192 R, \u00acR. What is P?", "options": ["True", "False", "Cannot determine", "Invalid"], "correct_answer": 2, "explanation": "\u00acR true \u21d2 \u00acQ false \u21d2 Q true. If P true then Q true, but Q true already, so P unknown?", "difficulty": "medium"},
    {"question": "\"Not all that is gold glitters\" is equivalent to:", "options": ["Some gold does not glitter", "All gold glitters", "No gold glitters", "Some non-gold glitters"], "correct_answer": 0, "explanation": "\"Not all S are P\" means \"Some S are not P\".", "difficulty": "medium"},
    {"question": "Which is the converse of \"If x is even, then x\u00b2 is even\"?", "options": ["If x\u00b2 is even, then x is even", "If x is not even, then x\u00b2 is not even", "If x\u00b2 is not even, then x is not even", "None"], "correct_answer": 0, "explanation": "Converse swaps antecedent and consequent.", "difficulty": "medium"},
    {"question": "Statements:\n1. Some dogs are animals.\n2. All animals are mortal.\nConclusion: Some dogs are mortal.", "options": ["Valid", "Invalid", "Probably true", "False"], "correct_answer": 0, "explanation": "Valid syllogism.", "difficulty": "medium"},
    {"question": "\"If it snows, roads are blocked. If roads are blocked, schools close. Today schools did not close.\" What follows?", "options": ["It did not snow", "It snowed", "Roads are blocked", "Roads are not blocked"], "correct_answer": 0, "explanation": "Schools not close \u21d2 Roads not blocked \u21d2 Did not snow.", "difficulty": "medium"},
    {"question": "\"Only if he studies, will he pass\" means:", "options": ["If he studies, he passes", "If he passes, he studied", "He passes if and only if he studies", "He studies or he fails"], "correct_answer": 1, "explanation": "\"Only if P, Q\" means Q \u2192 P.", "difficulty": "medium"},
    {"question": "Given: A \u2194 B, B is false. What is A?", "options": ["True", "False", "Either", "Neither"], "correct_answer": 1, "explanation": "Biconditional true when both same. B false \u21d2 A false.", "difficulty": "medium"},
    {"question": "\"All birds fly. Penguins are birds. Therefore penguins fly.\" This is:", "options": ["Valid but unsound", "Invalid", "Sound", "False"], "correct_answer": 0, "explanation": "Valid form, but premise \"All birds fly\" is false in reality.", "difficulty": "medium"},
    {"question": "\"P is sufficient for Q\" means:", "options": ["P \u2192 Q", "Q \u2192 P", "P \u2194 Q", "\u00acP \u2192 \u00acQ"], "correct_answer": 0, "explanation": "Sufficient condition.", "difficulty": "medium"},
    {"question": "Given: Either A or B must be chosen but not both. A is chosen. What about B?", "options": ["Chosen", "Not chosen", "Unknown", "Invalid"], "correct_answer": 1, "explanation": "Exclusive OR.", "difficulty": "medium"},
    {"question": "\"Most lawyers are clever\" \u2013 which cannot be true?", "options": ["Some lawyers are not clever", "All lawyers are clever", "No lawyer is clever", "Some clever people are lawyers"], "correct_answer": 2, "explanation": "\"Most\" implies at least some.", "difficulty": "medium"},
    {"question": "Statements: If it rains, picnic cancelled. Picnic not cancelled. What follows?", "options": ["It rained", "It did not rain", "It may have rained", "No conclusion"], "correct_answer": 1, "explanation": "Contrapositive: Picnic not cancelled \u21d2 did not rain.", "difficulty": "medium"},
    {"question": "\"All A are B. Some B are C.\" What follows?", "options": ["Some A are C", "No A are C", "Some C are A", "None of the above"], "correct_answer": 3, "explanation": "No necessary relation between A and C.", "difficulty": "medium"},
    {"question": "\"Whenever he sings, people applaud. People are not applauding.\" Conclusion:", "options": ["He is not singing", "He is singing", "He may be singing", "Invalid"], "correct_answer": 0, "explanation": "Contrapositive.", "difficulty": "medium"},
    {"question": "\"Not both rich and happy\" means:", "options": ["If rich, then not happy", "If happy, then not rich", "Either not rich or not happy", "All of the above"], "correct_answer": 3, "explanation": "\u00ac(R \u2227 H) \u2261 \u00acR \u2228 \u00acH \u2261 R \u2192 \u00acH \u2261 H \u2192 \u00acR.", "difficulty": "medium"},

    # HARD (20)
    {"question": "Given: (P \u2192 Q) \u2227 (R \u2192 S), \u00acQ \u2228 \u00acS. What can be concluded?", "options": ["\u00acP \u2228 \u00acR", "P \u2227 R", "Q \u2227 S", "\u00acP \u2227 \u00acR"], "correct_answer": 0, "explanation": "From \u00acQ \u2228 \u00acS and implications, we get \u00acP \u2228 \u00acR.", "difficulty": "hard"},
    {"question": "Statements:\n1. Only successful people are happy.\n2. No lazy person is successful.\nConclusion: No lazy person is happy.", "options": ["Valid", "Invalid", "Probably true", "Cannot say"], "correct_answer": 0, "explanation": "Happy \u2192 Successful \u2192 Not lazy. So lazy \u2192 not happy.", "difficulty": "hard"},
    {"question": "\"All men are mortal. Socrates is a man. Therefore Socrates is mortal.\" This exemplifies:", "options": ["Modus Ponens", "Modus Tollens", "Syllogism", "Disjunctive syllogism"], "correct_answer": 2, "explanation": "Categorical syllogism.", "difficulty": "hard"},
    {"question": "If \"Some A are B\" and \"No B are C\", then which is necessarily true?", "options": ["Some A are not C", "No A are C", "Some C are not A", "All A are C"], "correct_answer": 0, "explanation": "Some A are B, No B are C \u21d2 Those A that are B are not C \u21d2 Some A are not C.", "difficulty": "hard"},
    {"question": "Given: (A \u2228 B) \u2192 C, \u00acC. What follows?", "options": ["\u00acA \u2227 \u00acB", "A \u2227 B", "\u00acA \u2228 \u00acB", "A \u2228 B"], "correct_answer": 0, "explanation": "From \u00acC and implication, \u00ac(A \u2228 B) \u21d2 \u00acA \u2227 \u00acB.", "difficulty": "hard"},
    {"question": "\"Either the number is even or it is prime. It is not prime.\" If the statement is true, what must be true?", "options": ["Number is even", "Number is odd", "Number is composite", "Number is not even"], "correct_answer": 0, "explanation": "Logical \"either A or B\" as exclusive OR.", "difficulty": "hard"},
    {"question": "\"If it is a tiger, then it has stripes. That animal has stripes.\" What logically follows?", "options": ["It is a tiger", "It may or may not be a tiger", "It is not a tiger", "No conclusion"], "correct_answer": 1, "explanation": "Affirming the consequent fallacy.", "difficulty": "hard"},
    {"question": "Given premises:\n1. All scientists are researchers.\n2. Some researchers are professors.\n3. No professor is ignorant.\nConclusion: Some scientists are not ignorant.", "options": ["Valid", "Invalid", "Probably true", "False"], "correct_answer": 1, "explanation": "No link between scientists and professors established.", "difficulty": "hard"},
    {"question": "\"P unless Q\" is equivalent to:", "options": ["P \u2228 Q", "\u00acQ \u2192 P", "Q \u2192 \u00acP", "All of the above"], "correct_answer": 3, "explanation": "P unless Q \u2261 If not Q then P \u2261 P \u2228 Q.", "difficulty": "hard"},
    {"question": "\"All that is legal is not necessarily moral.\" Means:", "options": ["Some legal things are immoral", "No legal things are moral", "All moral things are legal", "Some illegal things are moral"], "correct_answer": 0, "explanation": "\"Not necessarily\" means possibly not.", "difficulty": "hard"},
    {"question": "\"If A then B\" and \"If not A then B\" together imply:", "options": ["B is true", "A is true", "B is false", "A is false"], "correct_answer": 0, "explanation": "(A \u2192 B) \u2227 (\u00acA \u2192 B) is a tautology implying B.", "difficulty": "hard"},
    {"question": "Statements:\n1. Only honest people are respected.\n2. Some politicians are respected.\nConclusion: Some politicians are honest.", "options": ["Valid", "Invalid", "Probably true", "False"], "correct_answer": 0, "explanation": "Respected \u2192 Honest. Some politicians respected \u21d2 Some politicians honest.", "difficulty": "hard"},
    {"question": "Given: P \u2192 Q, R \u2192 \u00acQ, S \u2192 P, \u00acQ. What is true?", "options": ["\u00acP", "\u00acR", "\u00acS", "All of above"], "correct_answer": 0, "explanation": "\u00acQ \u21d2 from P\u2192Q, \u00acP. (R unknown).", "difficulty": "hard"},
    {"question": "\"All squares are rectangles. All rectangles are quadrilaterals. Therefore all squares are quadrilaterals.\" This reasoning is:", "options": ["Valid and sound", "Valid but unsound", "Invalid", "Inductive"], "correct_answer": 0, "explanation": "Valid syllogism, premises true.", "difficulty": "hard"},
    {"question": "\"If inflation rises, interest rates increase. If interest rates increase, growth slows. Growth is not slowing.\" What follows?", "options": ["Inflation is not rising", "Interest rates not increasing", "Both 1 and 2", "None"], "correct_answer": 2, "explanation": "Chain: Inflation rise \u2192 Interest increase \u2192 Growth slow. Growth not slow \u21d2 Interest not increase \u21d2 Inflation not rise.", "difficulty": "hard"},
    {"question": "\"Most scientists are rational. Some rational people are philosophers. Therefore some scientists are philosophers.\" This is:", "options": ["Valid", "Invalid", "Probably true", "False"], "correct_answer": 1, "explanation": "\"Most\" doesn't guarantee overlap with philosophers.", "difficulty": "hard"},
    {"question": "Given: (A \u2227 B) \u2192 C, \u00acC, B. What can be concluded about A?", "options": ["A true", "A false", "A unknown", "Contradiction"], "correct_answer": 1, "explanation": "\u00acC \u21d2 \u00ac(A \u2227 B) \u2261 \u00acA \u2228 \u00acB. Given B \u21d2 \u00acA.", "difficulty": "hard"},
    {"question": "\"Not every artist is creative\" is equivalent to:", "options": ["Some artists are not creative", "No artist is creative", "Some creative people are not artists", "All non-artists are creative"], "correct_answer": 0, "explanation": "Same as earlier.", "difficulty": "hard"},
    {"question": "Statement: Only if the board approves, will the project start. The project has started. Conclusion:", "options": ["Board approved", "Board may have approved", "Board did not approve", "Project didn't need approval"], "correct_answer": 0, "explanation": "\"Only if P, Q\" means Q \u2192 P. Project started \u21d2 Board approved.", "difficulty": "hard"},
    {"question": "Given: All managers are executives. Some executives are corrupt. Which is necessarily true?", "options": ["Some managers are corrupt", "Some corrupt are managers", "Some managers are not corrupt", "None of the above"], "correct_answer": 3, "explanation": "No necessary relation.", "difficulty": "hard"}
]

for q_data in questions:
    # Ensure options are exactly as provided (correct index might need adjustment if using 1-based in text but 0-based in code)
    # The user provided 1-based options in text, so I mapped them.
    # Wait, my `correct_answer` values in the list above are ALREADY 0-indexed.
    
    q = AptitudeQuestion(
        id=str(uuid.uuid4()),
        question=q_data["question"],
        options=q_data["options"],
        correct_answer=q_data["correct_answer"],
        answer_explanation=q_data["explanation"],
        topic="Logical Operations",
        category="Analytical Reasoning",
        difficulty=q_data["difficulty"],
        source="hardcoded",
        primary_concepts=["logical_connectives", "syllogisms", "conditional_logic"],
        trap_explanation=None
    )
    session.add(q)

session.commit()
print(f"Successfully seeded {len(questions)} Logical Operations questions.")
session.close()
