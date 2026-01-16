from sqlalchemy import Column, Integer, String
from database_postgres import Base


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    domain = Column(String, nullable=False)       # technical / hr
    language = Column(String, nullable=True)      # python / java
    topic = Column(String, nullable=False)        # oops / dsa / dbms
    subtopic = Column(String, nullable=True)      # inheritance / arrays
    difficulty = Column(String, nullable=False)   # easy / medium / hard
