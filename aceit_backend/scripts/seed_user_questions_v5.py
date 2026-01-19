"""
Seed User Provided Questions (Extended Categories):
Adds questions for Data Interpretation, Analytical Reasoning, Non-Verbal Reasoning, 
Critical Reasoning, and Decision Making.
"""

import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.aptitude_sql import AptitudeQuestion

EXTENDED_QUESTIONS = [
  {
    "category": "Data Interpretation",
    "topic": "Table",
    "difficulty": "easy",
    "question": "A table shows sales of a company: 2019 = 100, 2020 = 120, 2021 = 150. What is the total sales?",
    "options": ["350", "360", "370", "380"],
    "correct_answer": 2,
    "answer_explanation": "Total = 100 + 120 + 150 = 370."
  },
  {
    "category": "Data Interpretation",
    "topic": "Table",
    "difficulty": "medium",
    "question": "If a company\u2019s profit was \u20b940 lakh in 2020 and \u20b960 lakh in 2021, by what percentage did profit increase?",
    "options": ["40%", "50%", "60%", "75%"],
    "correct_answer": 1,
    "answer_explanation": "Increase = 20. Percentage = (20/40)\u00d7100 = 50%."
  },
  {
    "category": "Data Interpretation",
    "topic": "Bar Graph",
    "difficulty": "hard",
    "question": "If production increases from 200 units to 260 units, what is the percentage increase?",
    "options": ["25%", "30%", "35%", "40%"],
    "correct_answer": 1,
    "answer_explanation": "Increase = 60. Percentage = (60/200)\u00d7100 = 30%."
  },
  {
    "category": "Analytical Reasoning",
    "topic": "Statement and Assumption",
    "difficulty": "easy",
    "question": "Statement: The government should ban plastic bags. Assumption: Plastic bags harm the environment.",
    "options": ["Assumption is implicit", "Assumption is not implicit", "Both true", "Both false"],
    "correct_answer": 0,
    "answer_explanation": "The statement assumes plastic bags are harmful."
  },
  {
    "category": "Analytical Reasoning",
    "topic": "Statement and Conclusion",
    "difficulty": "medium",
    "question": "Statement: All engineers are graduates. Some graduates are teachers. Conclusion: Some engineers are teachers.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 2,
    "answer_explanation": "No direct link between engineers and teachers."
  },
  {
    "category": "Analytical Reasoning",
    "topic": "Cause and Effect",
    "difficulty": "hard",
    "question": "Cause: Heavy rainfall occurred. Effect: Floods damaged crops. Which relation is correct?",
    "options": ["Cause only", "Effect only", "Both are correct", "No relation"],
    "correct_answer": 2,
    "answer_explanation": "Heavy rainfall can cause floods which damage crops."
  },
  {
    "category": "Non-Verbal Reasoning",
    "topic": "Figure Series",
    "difficulty": "easy",
    "question": "In a figure series, a square rotates 90\u00b0 clockwise each step. What is the rotation after 3 steps?",
    "options": ["90\u00b0", "180\u00b0", "270\u00b0", "360\u00b0"],
    "correct_answer": 2,
    "answer_explanation": "90\u00b0 \u00d7 3 = 270\u00b0."
  },
  {
    "category": "Non-Verbal Reasoning",
    "topic": "Mirror Image",
    "difficulty": "medium",
    "question": "Which option represents the mirror image of the word 'CODE'?",
    "options": ["EDOC", "CODE", "OCED", "DOCE"],
    "correct_answer": 0,
    "answer_explanation": "Mirror image reverses the order of letters."
  },
  {
    "category": "Non-Verbal Reasoning",
    "topic": "Paper Folding",
    "difficulty": "hard",
    "question": "A paper is folded twice and a hole is punched. How many holes will appear when unfolded?",
    "options": ["2", "4", "6", "8"],
    "correct_answer": 1,
    "answer_explanation": "Each fold doubles the holes. 2 folds \u2192 4 holes."
  },
  {
    "category": "Critical Reasoning",
    "topic": "Argument Strength",
    "difficulty": "easy",
    "question": "Should mobile phones be banned in classrooms? Argument: Yes, they distract students.",
    "options": ["Strong argument", "Weak argument", "Irrelevant", "Contradictory"],
    "correct_answer": 0,
    "answer_explanation": "Distraction is a valid and strong reason."
  },
  {
    "category": "Critical Reasoning",
    "topic": "Inference",
    "difficulty": "medium",
    "question": "Statement: Some students are athletes. All athletes are disciplined. Inference: Some students are disciplined.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 0,
    "answer_explanation": "Some students belong to athletes, and all athletes are disciplined."
  },
  {
    "category": "Critical Reasoning",
    "topic": "Course of Action",
    "difficulty": "hard",
    "question": "A city faces severe water shortage. What should be the first action?",
    "options": [
      "Increase water tariff",
      "Educate people on water conservation",
      "Do nothing",
      "Ban industries permanently"
    ],
    "correct_answer": 1,
    "answer_explanation": "Awareness and conservation is the most practical first step."
  },
  {
    "category": "Decision Making",
    "topic": "Situational Judgment",
    "difficulty": "easy",
    "question": "You see a colleague struggling with work. What should you do?",
    "options": [
      "Ignore",
      "Report to manager",
      "Offer help",
      "Criticize"
    ],
    "correct_answer": 2,
    "answer_explanation": "Offering help is cooperative and professional."
  },
  {
    "category": "Decision Making",
    "topic": "Ethical Decision",
    "difficulty": "medium",
    "question": "You find a wallet on the road. What is the best action?",
    "options": [
      "Keep it",
      "Leave it",
      "Submit to police",
      "Ask friends"
    ],
    "correct_answer": 2,
    "answer_explanation": "Submitting to authorities is ethical."
  },
  {
    "category": "Decision Making",
    "topic": "Workplace Scenario",
    "difficulty": "hard",
    "question": "Your team misses a deadline due to your mistake. What should you do?",
    "options": [
      "Blame others",
      "Hide the mistake",
      "Accept responsibility",
      "Quit the job"
    ],
    "correct_answer": 2,
    "answer_explanation": "Taking responsibility reflects professionalism."
  },
  {
    "category": "Data Interpretation",
    "topic": "Table",
    "difficulty": "easy",
    "question": "A table shows the number of students in four classes: A=30, B=40, C=50, D=60. What is the total number of students?",
    "options": ["160", "170", "180", "190"],
    "correct_answer": 2,
    "answer_explanation": "Total = 30 + 40 + 50 + 60 = 180."
  },
  {
    "category": "Data Interpretation",
    "topic": "Table",
    "difficulty": "medium",
    "question": "If the income of a person increases from \u20b925,000 to \u20b930,000, what is the percentage increase?",
    "options": ["15%", "18%", "20%", "25%"],
    "correct_answer": 2,
    "answer_explanation": "Increase = 5000. Percentage = (5000/25000)\u00d7100 = 20%."
  },
  {
    "category": "Data Interpretation",
    "topic": "Pie Chart",
    "difficulty": "hard",
    "question": "A pie chart shows expenditure distribution. If food accounts for 90\u00b0 of the chart, what percentage of total expenditure is on food?",
    "options": ["20%", "25%", "30%", "35%"],
    "correct_answer": 1,
    "answer_explanation": "Percentage = (90/360)\u00d7100 = 25%."
  },
  {
    "category": "Analytical Reasoning",
    "topic": "Statement and Assumption",
    "difficulty": "easy",
    "question": "Statement: We should switch off lights when not in use. Assumption: Electricity is limited.",
    "options": ["Assumption is implicit", "Assumption is not implicit", "Both true", "Both false"],
    "correct_answer": 0,
    "answer_explanation": "The statement assumes electricity should be conserved."
  },
  {
    "category": "Analytical Reasoning",
    "topic": "Statement and Conclusion",
    "difficulty": "medium",
    "question": "Statement: All doctors are educated. Some educated people are rich. Conclusion: Some doctors are rich.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 2,
    "answer_explanation": "No direct link between doctors and rich people."
  },
  {
    "category": "Analytical Reasoning",
    "topic": "Cause and Effect",
    "difficulty": "hard",
    "question": "Cause: Prices of fuel increased sharply. Effect: Transport costs increased. Which option is correct?",
    "options": ["Cause only", "Effect only", "Both are correct", "No relation"],
    "correct_answer": 2,
    "answer_explanation": "Increase in fuel prices leads to higher transport costs."
  },
  {
    "category": "Non-Verbal Reasoning",
    "topic": "Figure Series",
    "difficulty": "easy",
    "question": "In a figure series, a triangle gains one side each step. How many sides will the 4th figure have?",
    "options": ["4", "5", "6", "7"],
    "correct_answer": 2,
    "answer_explanation": "Triangle (3 sides) \u2192 +1 each step \u2192 6 sides at 4th step."
  },
  {
    "category": "Non-Verbal Reasoning",
    "topic": "Mirror Image",
    "difficulty": "medium",
    "question": "What happens to the word 'MAP' when seen in a mirror?",
    "options": ["PAM", "MAP", "AMP", "MPA"],
    "correct_answer": 0,
    "answer_explanation": "Mirror image reverses the order of letters."
  },
  {
    "category": "Non-Verbal Reasoning",
    "topic": "Water Image",
    "difficulty": "hard",
    "question": "Which feature changes in a water image?",
    "options": ["Left and right", "Top and bottom", "Both", "None"],
    "correct_answer": 1,
    "answer_explanation": "Water image reverses top and bottom."
  },
  {
    "category": "Critical Reasoning",
    "topic": "Argument Strength",
    "difficulty": "easy",
    "question": "Should plastic usage be reduced? Argument: Plastic causes pollution.",
    "options": ["Strong", "Weak", "Irrelevant", "Contradictory"],
    "correct_answer": 0,
    "answer_explanation": "Pollution is a valid reason."
  },
  {
    "category": "Critical Reasoning",
    "topic": "Inference",
    "difficulty": "medium",
    "question": "Statement: All managers are leaders. Some leaders are strict. Inference: Some managers are strict.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 2,
    "answer_explanation": "No direct link between managers and strict leaders."
  },
  {
    "category": "Critical Reasoning",
    "topic": "Course of Action",
    "difficulty": "hard",
    "question": "There is a sudden increase in road accidents. What should be done first?",
    "options": [
      "Ban all vehicles",
      "Increase traffic awareness",
      "Ignore the issue",
      "Close roads permanently"
    ],
    "correct_answer": 1,
    "answer_explanation": "Awareness and safety education is the most practical first step."
  },
  {
    "category": "Decision Making",
    "topic": "Workplace Scenario",
    "difficulty": "easy",
    "question": "Your teammate is absent and work is pending. What should you do?",
    "options": [
      "Leave the work",
      "Complain immediately",
      "Complete urgent tasks",
      "Ignore deadlines"
    ],
    "correct_answer": 2,
    "answer_explanation": "Completing urgent tasks shows responsibility."
  },
  {
    "category": "Decision Making",
    "topic": "Ethical Scenario",
    "difficulty": "medium",
    "question": "You notice incorrect data in a report submitted by your team. What should you do?",
    "options": [
      "Ignore it",
      "Correct it secretly",
      "Inform the team",
      "Delete the report"
    ],
    "correct_answer": 2,
    "answer_explanation": "Informing the team ensures transparency and accuracy."
  },
  {
    "category": "Decision Making",
    "topic": "Leadership",
    "difficulty": "hard",
    "question": "Your team members disagree strongly during a project discussion. What is the best approach?",
    "options": [
      "Support only one side",
      "Ignore the conflict",
      "Encourage discussion and find consensus",
      "End the meeting"
    ],
    "correct_answer": 2,
    "answer_explanation": "Encouraging discussion helps reach a balanced decision."
  },
  {
    "category": "Data Interpretation",
    "topic": "Bar Graph",
    "difficulty": "easy",
    "question": "A bar graph shows the production of cars in four years as 50, 60, 70, and 80 units. What is the average production?",
    "options": ["60", "65", "70", "75"],
    "correct_answer": 1,
    "answer_explanation": "Average = (50+60+70+80)/4 = 65."
  },
  {
    "category": "Data Interpretation",
    "topic": "Line Graph",
    "difficulty": "medium",
    "question": "If a line graph shows monthly profit as \u20b910k, \u20b915k, \u20b920k, \u20b925k, what is the percentage increase from first to last month?",
    "options": ["100%", "120%", "150%", "200%"],
    "correct_answer": 2,
    "answer_explanation": "Increase = 15k. Percentage = (15/10)\u00d7100 = 150%."
  },
  {
    "category": "Data Interpretation",
    "topic": "Pie Chart",
    "difficulty": "hard",
    "question": "If 120\u00b0 of a pie chart represents \u20b96000 expenditure, what is the total expenditure?",
    "options": ["\u20b912000", "\u20b915000", "\u20b918000", "\u20b920000"],
    "correct_answer": 2,
    "answer_explanation": "Total = (360/120)\u00d76000 = 18000."
  },
  {
    "category": "Analytical Reasoning",
    "topic": "Statement and Assumption",
    "difficulty": "easy",
    "question": "Statement: People should exercise daily. Assumption: Exercise improves health.",
    "options": ["Assumption is implicit", "Assumption is not implicit", "Both false", "Both true"],
    "correct_answer": 0,
    "answer_explanation": "The statement assumes exercise improves health."
  },
  {
    "category": "Analytical Reasoning",
    "topic": "Statement and Conclusion",
    "difficulty": "medium",
    "question": "Statement: Some laptops are expensive. All expensive items are taxed. Conclusion: Some laptops are taxed.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 0,
    "answer_explanation": "Some laptops fall under expensive items, hence taxed."
  },
  {
    "category": "Analytical Reasoning",
    "topic": "Cause and Effect",
    "difficulty": "hard",
    "question": "Cause: Internet services were down. Effect: Online transactions failed. Choose the correct option.",
    "options": ["Cause only", "Effect only", "Both are correct", "No relation"],
    "correct_answer": 2,
    "answer_explanation": "Internet failure can lead to transaction failures."
  },
  {
    "category": "Non-Verbal Reasoning",
    "topic": "Figure Completion",
    "difficulty": "easy",
    "question": "If a circle is divided into 2 equal parts in the first step and each step doubles the divisions, how many parts are there in the 3rd step?",
    "options": ["4", "6", "8", "16"],
    "correct_answer": 2,
    "answer_explanation": "2 \u2192 4 \u2192 8 parts."
  },
  {
    "category": "Non-Verbal Reasoning",
    "topic": "Mirror Image",
    "difficulty": "medium",
    "question": "Which letter looks the same in a mirror image?",
    "options": ["B", "C", "D", "E"],
    "correct_answer": 1,
    "answer_explanation": "The letter C is symmetrical vertically."
  },
  {
    "category": "Non-Verbal Reasoning",
    "topic": "Paper Folding",
    "difficulty": "hard",
    "question": "A paper is folded three times and one hole is punched. How many holes appear when unfolded?",
    "options": ["6", "8", "12", "16"],
    "correct_answer": 1,
    "answer_explanation": "Each fold doubles holes: 2\u00b3 = 8."
  },
  {
    "category": "Critical Reasoning",
    "topic": "Argument Strength",
    "difficulty": "easy",
    "question": "Should online classes continue after the pandemic? Argument: They save travel time.",
    "options": ["Strong", "Weak", "Irrelevant", "Illogical"],
    "correct_answer": 0,
    "answer_explanation": "Saving travel time is a valid argument."
  },
  {
    "category": "Critical Reasoning",
    "topic": "Inference",
    "difficulty": "medium",
    "question": "Statement: All writers are readers. Some readers are poets. Inference: Some writers are poets.",
    "options": ["True", "False", "Cannot be determined", "None"],
    "correct_answer": 2,
    "answer_explanation": "No direct link between writers and poets."
  },
  {
    "category": "Critical Reasoning",
    "topic": "Course of Action",
    "difficulty": "hard",
    "question": "There is a sudden rise in cyber crimes. What should be the immediate action?",
    "options": [
      "Shut down internet",
      "Increase cyber awareness programs",
      "Ignore the issue",
      "Ban all online services"
    ],
    "correct_answer": 1,
    "answer_explanation": "Awareness is the most effective immediate step."
  },
  {
    "category": "Decision Making",
    "topic": "Situational Judgment",
    "difficulty": "easy",
    "question": "You are late to a meeting due to traffic. What should you do?",
    "options": [
      "Stay silent",
      "Blame traffic loudly",
      "Apologize politely",
      "Leave immediately"
    ],
    "correct_answer": 2,
    "answer_explanation": "Apologizing shows professionalism."
  },
  {
    "category": "Decision Making",
    "topic": "Ethical Decision",
    "difficulty": "medium",
    "question": "You receive confidential information by mistake. What is the best action?",
    "options": [
      "Share it",
      "Ignore it",
      "Inform the concerned authority",
      "Delete it secretly"
    ],
    "correct_answer": 2,
    "answer_explanation": "Informing authority maintains ethics."
  },
  {
    "category": "Decision Making",
    "topic": "Crisis Management",
    "difficulty": "hard",
    "question": "A critical system fails just before a deadline. What should you do first?",
    "options": [
      "Panic",
      "Inform stakeholders",
      "Ignore the issue",
      "Blame team members"
    ],
    "correct_answer": 1,
    "answer_explanation": "Immediate communication is crucial in crises."
  }
]

def seed_questions():
    db = SessionLocal()
    try:
        print(f"Seeding {len(EXTENDED_QUESTIONS)} extended category questions...")
        added = 0
        for q_data in EXTENDED_QUESTIONS:
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
