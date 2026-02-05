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

# Passage Data Mapping
passages = {
    "P1": "The Sun is the primary source of energy for Earth. It provides light and heat that sustains all life on our planet. Solar energy is clean, renewable, and abundant. Plants use sunlight for photosynthesis, converting it into chemical energy. Humans harness solar energy through solar panels that convert sunlight into electricity. Solar power helps reduce pollution and dependence on fossil fuels.",
    "P2": "John wakes up at 6 AM every morning. He brushes his teeth, takes a shower, and gets dressed. Then he eats breakfast, usually cereal with milk. At 7:30 AM, he leaves for work. He works as an accountant in a company downtown. He returns home at 6 PM, eats dinner, watches TV, and reads before going to bed at 10 PM.",
    "P3": "A library is a place where books, magazines, and other sources of information are kept for people to read or borrow. Modern libraries also provide access to digital resources like e-books and the internet. Libraries are important for education and community growth. People of all ages go to libraries to study, learn, and enjoy reading. It is a quiet place where silence is expected to help others focus.",
    "P4": "The Great Wall of China is one of the most famous structures in the world. It was built over many centuries to protect China from invasions. The wall stretches for thousands of miles across mountains and plains. It is made of stone, brick, and other materials. Today, it is a UNESCO World Heritage site and attracts millions of tourists every year.",
    "P5": "The Industrial Revolution, which began in Britain in the late 18th century, marked a major turning point in history. It transformed agrarian, rural societies into industrial, urban ones. The invention of steam power and new machinery revolutionized manufacturing processes. While it led to unprecedented economic growth and technological advancement, it also resulted in poor working conditions, child labor, and environmental degradation. The revolution spread to Europe and North America, fundamentally altering global economic systems.",
    "P6": "Cognitive dissonance theory, proposed by Leon Festinger in 1957, posits that individuals experience psychological discomfort when they hold two or more contradictory beliefs, ideas, or values simultaneously. This discomfort motivates people to reduce the inconsistency by changing their beliefs, acquiring new information, or minimizing the importance of the conflict. The theory has been widely applied in psychology, marketing, and political science to explain attitude change and decision-making processes.",
    "P7": "Wind energy is a form of renewable energy that uses the power of the wind to generate electricity. Wind turbines, which look like giant fans, capture the kinetic energy of moving air. When the wind blows, the blades turn a generator inside the turbine. Unlike fossil fuels, wind energy does not produce greenhouse gases or air pollution. However, some people are concerned about the visual impact of wind farms and their effect on birds.",
    "P8": "Mars, often called the Red Planet, has long fascinated scientists and the public. It is the fourth planet from the Sun and has a thin atmosphere composed mostly of carbon dioxide. Recent missions have found evidence of liquid water in the past, suggesting that Mars might have once supported life. Space agencies like NASA are planning manned missions to Mars in the coming decades, aiming to establish a human presence on another world.",
    "P9": "Postmodern literary theory emerged in the mid-to-late 20th century as a reaction against modernist claims of universal truth and objective reality. Characterized by skepticism toward grand narratives, postmodernism emphasizes fragmentation, paradox, and the constructed nature of reality. Key theorists like Jacques Derrida, through deconstruction, challenged binary oppositions and hierarchical thought structures. The movement questions the very possibility of fixed meaning, arguing that language is inherently unstable and that texts contain multiple, often contradictory, interpretations. This epistemological relativism has profound implications for how we understand history, identity, and cultural production.",
    "P10": "Quantum entanglement, described by Einstein as 'spooky action at a distance,' represents one of the most counterintuitive phenomena in quantum mechanics. When particles become entangled, the quantum state of each particle cannot be described independently of the others, even when separated by large distances. Measurement of one particle instantaneously affects its entangled partner, violating classical notions of locality and causality. While experimental verification through Bell's theorem inequalities has been conclusive, the interpretation remains contentious. The Copenhagen interpretation, many-worlds hypothesis, and pilot-wave theory offer competing explanations, with profound implications for our understanding of reality, information theory, and potential quantum computing applications.",
    "P11": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. While AI offers immense benefits in healthcare, transportation, and efficiency, it also raises significant ethical concerns. These include bias in algorithms, the potential for job displacement, and the lack of transparency in decision-making processes. As AI becomes more integrated into daily life, developing robust ethical frameworks and regulations is crucial to ensure it benefits all of humanity.",
    "P12": "Existentialism is a philosophical inquiry that explores the nature of the human condition, emphasizing individual freedom, choice, and responsibility. Existentialists argue that the universe has no inherent meaning or purpose, and therefore individuals must create their own meaning through their actions. Philosophers like Jean-Paul Sartre and Albert Camus explored themes of absurdity, angst, and authenticity. Existentialism encourages people to take ownership of their lives and live authentically despite the inherent uncertainties of existence."
}

questions_data = [
    # EASY (20)
    # Passage 1 (Sun)
    {"q": "What is the primary source of energy for Earth according to the passage?", "options": ["Wind", "The Sun", "Fossil fuels", "Water"], "a": 1, "exp": "Directly stated in first sentence: 'The Sun is the primary source of energy for Earth.'", "diff": "easy", "p": "P1"},
    {"q": "What do plants use sunlight for?", "options": ["Respiration", "Photosynthesis", "Transpiration", "Germination"], "a": 1, "exp": "Directly stated: 'Plants use sunlight for photosynthesis.'", "diff": "easy", "p": "P1"},
    {"q": "How do humans harness solar energy?", "options": ["Wind turbines", "Hydroelectric dams", "Solar panels", "Geothermal plants"], "a": 2, "exp": "Directly stated: 'Humans harness solar energy through solar panels.'", "diff": "easy", "p": "P1"},
    {"q": "What is NOT mentioned as a benefit of solar power?", "options": ["Reduces pollution", "Reduces fossil fuel dependence", "Creates jobs", "Is clean and renewable"], "a": 2, "exp": "Job creation is not mentioned; all other benefits are explicitly stated.", "diff": "easy", "p": "P1"},
    {"q": "The word 'abundant' in the passage means:", "options": ["Scarce", "Plentiful", "Expensive", "Complex"], "a": 1, "exp": "Context clue: 'clean, renewable, and abundant' - positive attribute meaning plentiful.", "diff": "easy", "p": "P1"},
    
    # Passage 2 (Daily Routine)
    {"q": "What time does John wake up?", "options": ["5 AM", "6 AM", "7 AM", "8 AM"], "a": 1, "exp": "Directly stated: 'John wakes up at 6 AM every morning.'", "diff": "easy", "p": "P2"},
    {"q": "What does John usually eat for breakfast?", "options": ["Toast and eggs", "Cereal with milk", "Pancakes", "Fruit"], "a": 1, "exp": "Directly stated: 'usually cereal with milk.'", "diff": "easy", "p": "P2"},
    {"q": "What is John's profession?", "options": ["Teacher", "Accountant", "Engineer", "Doctor"], "a": 1, "exp": "Directly stated: 'He works as an accountant.'", "diff": "easy", "p": "P2"},
    {"q": "What time does John go to bed?", "options": ["9 PM", "10 PM", "11 PM", "Midnight"], "a": 1, "exp": "Directly stated: 'going to bed at 10 PM.'", "diff": "easy", "p": "P2"},
    {"q": "Which activity is NOT mentioned in John's evening routine?", "options": ["Eats dinner", "Watches TV", "Reads", "Exercises"], "a": 3, "exp": "Exercise is not mentioned; all other activities are explicitly stated.", "diff": "easy", "p": "P2"},
    
    # Passage 3 (Library)
    {"q": "What is the primary purpose of a library according to the passage?", "options": ["To sell books", "To provide sources of information", "To provide free internet only", "To host parties"], "a": 1, "exp": "The passage states libraries are places where sources of information are kept for people to read or borrow.", "diff": "easy", "p": "P3"},
    {"q": "What modern resources do libraries provide access to?", "options": ["Printed newspapers only", "Digital resources like e-books", "Video game consoles", "Calculators"], "a": 1, "exp": "The passage mentions modern libraries provide access to digital resources like e-books and the internet.", "diff": "easy", "p": "P3"},
    {"q": "Why is silence expected in a library?", "options": ["To save energy", "To help others focus", "To follow ancient traditions", "Because the librarians are strict"], "a": 1, "exp": "The passage says silence is expected to help others focus.", "diff": "easy", "p": "P3"},
    {"q": "Who goes to libraries according to the text?", "options": ["Only students", "Only adults", "People of all ages", "Only children"], "a": 2, "exp": "The passage explicitly says 'People of all ages go to libraries.'", "diff": "easy", "p": "P3"},
    {"q": "What are libraries important for?", "options": ["Entertainment only", "Education and community growth", "Storing old furniture", "Increasing digital divide"], "a": 1, "exp": "The passage states that 'Libraries are important for education and community growth.'", "diff": "easy", "p": "P3"},

    # Passage 4 (Great Wall)
    {"q": "Why was the Great Wall of China built?", "options": ["To attract tourists", "To protect China from invasions", "To connect many cities", "As a place for exercise"], "a": 1, "exp": "The passage says it was built 'to protect China from invasions.'", "diff": "easy", "p": "P4"},
    {"q": "What materials were used to build the Great Wall?", "options": ["Only wood", "Stone, brick, and other materials", "Only modern steel", "Only concrete"], "a": 1, "exp": "The passage states it is 'made of stone, brick, and other materials.'", "diff": "easy", "p": "P4"},
    {"q": "What recognition has the Great Wall received?", "options": ["Tallest wall in history", "UNESCO World Heritage site", "Most expensive wall", "Oldest structure ever"], "a": 1, "exp": "The passage mentions it is a 'UNESCO World Heritage site.'", "diff": "easy", "p": "P4"},
    {"q": "How long has the Great Wall been under construction?", "options": ["Just one year", "Over many centuries", "Exactly a decade", "Since the 20th century"], "a": 1, "exp": "The passage says it was 'built over many centuries.'", "diff": "easy", "p": "P4"},
    {"q": "What does the Great Wall attract today?", "options": ["Invaders", "Millions of tourists", "Only local people", "Ancient soldiers"], "a": 1, "exp": "Today 'it attracts millions of tourists every year.'", "diff": "easy", "p": "P4"},

    # MEDIUM (20)
    # Passage 5 (Industrial Revolution)
    {"q": "Where and when did the Industrial Revolution begin?", "options": ["France, early 18th century", "Britain, late 18th century", "Germany, early 19th century", "USA, late 19th century"], "a": 1, "exp": "Directly stated: 'began in Britain in the late 18th century.'", "diff": "medium", "p": "P5"},
    {"q": "What type of transformation occurred during the Industrial Revolution?", "options": ["Urban to rural", "Industrial to agrarian", "Agrarian to industrial", "Technological to manual"], "a": 2, "exp": "Directly stated: 'transformed agrarian, rural societies into industrial, urban ones.'", "diff": "medium", "p": "P5"},
    {"q": "Which of the following was NOT mentioned as a negative consequence?", "options": ["Poor working conditions", "Child labor", "Environmental degradation", "Increased poverty"], "a": 3, "exp": "Increased poverty is not explicitly mentioned; all others are stated negatives.", "diff": "medium", "p": "P5"},
    {"q": "What can be inferred about pre-industrial societies?", "options": ["They were primarily urban", "They relied on manufacturing", "They were mostly agrarian", "They had advanced technology"], "a": 2, "exp": "Inference from 'transformed agrarian societies into industrial ones' - pre-industrial = agrarian.", "diff": "medium", "p": "P5"},
    {"q": "The word 'unprecedented' in the passage most nearly means:", "options": ["Expected", "Never done or known before", "Gradual", "Limited"], "a": 1, "exp": "Context: 'unprecedented economic growth' means never before seen growth.", "diff": "medium", "p": "P5"},

    # Passage 6 (Cognitive Dissonance)
    {"q": "Who proposed cognitive dissonance theory?", "options": ["Sigmund Freud", "B.F. Skinner", "Leon Festinger", "Carl Jung"], "a": 2, "exp": "Directly stated: 'proposed by Leon Festinger in 1957.'", "diff": "medium", "p": "P6"},
    {"q": "What causes cognitive dissonance according to the passage?", "options": ["Holding consistent beliefs", "Holding contradictory beliefs", "Lacking any beliefs", "Changing beliefs frequently"], "a": 1, "exp": "Directly stated: 'hold two or more contradictory beliefs.'", "diff": "medium", "p": "P6"},
    {"q": "How do people typically reduce cognitive dissonance?", "options": ["By ignoring the conflict", "By changing beliefs or acquiring information", "By increasing the conflict", "By avoiding decision-making"], "a": 1, "exp": "Directly stated: 'changing their beliefs, acquiring new information, or minimizing the importance.'", "diff": "medium", "p": "P6"},
    {"q": "Which field is NOT mentioned as applying cognitive dissonance theory?", "options": ["Psychology", "Marketing", "Political Science", "Education"], "a": 3, "exp": "Education is not mentioned; psychology, marketing, and political science are explicitly stated.", "diff": "medium", "p": "P6"},
    {"q": "The word 'posits' in the passage means:", "options": ["Denies", "Assumes as fact", "Questions", "Forgets"], "a": 1, "exp": "Context: 'theory posits that...' means assumes or proposes as fact.", "diff": "medium", "p": "P6"},

    # Passage 7 (Wind Energy)
    {"q": "How do wind turbines capture energy?", "options": ["By burning air", "By capturing kinetic energy of moving air", "By using magnets in the ground", "By storing heat from the sun"], "a": 1, "exp": "The passage says turbines 'capture the kinetic energy of moving air.'", "diff": "medium", "p": "P7"},
    {"q": "What is one major environmental benefit of wind energy over fossil fuels?", "options": ["It is cheaper to build", "It does not produce greenhouse gases", "It provides habitats for birds", "It works only at night"], "a": 1, "exp": "Unlike fossil fuels, wind energy 'does not produce greenhouse gases or air pollution.'", "diff": "medium", "p": "P7"},
    {"q": "What is a common concern mentioned regarding wind farms?", "options": ["The noise they make", "The visual impact and effect on birds", "The cost of the electricity", "The risk of explosions"], "a": 1, "exp": "The text mentions concerns about 'visual impact of wind farms and their effect on birds.'", "diff": "medium", "p": "P7"},
    {"q": "What part of the turbine turns the generator?", "options": ["The tower", "The blades", "The wind itself directly", "Solar panels"], "a": 1, "exp": "When the wind blows, 'the blades turn a generator inside the turbine.'", "diff": "medium", "p": "P7"},
    {"q": "The word 'renewable' in the context of energy implies:", "options": ["It will run out soon", "It can be used once", "It comes from sources that are naturally replenished", "It is extremely expensive"], "a": 2, "exp": "Wind energy is described as renewable, which means it comes from sources that don't run out.", "diff": "medium", "p": "P7"},

    # Passage 8 (Mars)
    {"q": "What is the primary composition of Mars' thin atmosphere?", "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], "a": 1, "exp": "The passage says the atmosphere is 'composed mostly of carbon dioxide.'", "diff": "medium", "p": "P8"},
    {"q": "Why do scientists think Mars might have once supported life?", "options": ["They found ancient fossils", "They found evidence of liquid water in the past", "They saw aliens moving", "The atmosphere is full of oxygen"], "a": 1, "exp": "Evidence of 'liquid water in the past' suggests it might have supported life.", "diff": "medium", "p": "P8"},
    {"q": "What is NASA's future plan for Mars?", "options": ["To destroy the planet", "To move the Earth closer to it", "Planning manned missions to establish a human presence", "To ignore it and focus on Venus"], "a": 2, "exp": "NASA is 'planning manned missions... aiming to establish a human presence.'", "diff": "medium", "p": "P8"},
    {"q": "Which number planet from the Sun is Mars?", "options": ["Third", "Fourth", "Fifth", "Sixth"], "a": 1, "exp": "The passage states Mars is the 'fourth planet from the Sun.'", "diff": "medium", "p": "P8"},
    {"q": "What is the nickname given to Mars in the passage?", "options": ["The Blue Marble", "The Red Planet", "The Great Giant", "The Evening Star"], "a": 1, "exp": "Mars is 'often called the Red Planet.'", "diff": "medium", "p": "P8"},

    # HARD (20)
    # Passage 9 (Postmodernism)
    {"q": "Postmodernism emerged as a reaction against:", "options": ["Romantic emotionalism", "Modernist universal truth claims", "Classical formalism", "Realist objectivity"], "a": 1, "exp": "Directly stated: 'reaction against modernist claims of universal truth.'", "diff": "hard", "p": "P9"},
    {"q": "According to the passage, what does postmodernism emphasize?", "options": ["Unity and coherence", "Objective reality", "Fragmentation and paradox", "Universal narratives"], "a": 2, "exp": "Directly stated: 'emphasizes fragmentation, paradox, and the constructed nature.'", "diff": "hard", "p": "P9"},
    {"q": "Jacques Derrida is associated with:", "options": ["Structuralism", "Deconstruction", "Formalism", "Phenomenology"], "a": 1, "exp": "Directly stated: 'Jacques Derrida, through deconstruction.'", "diff": "hard", "p": "P9"},
    {"q": "What is the postmodern view of language?", "options": ["Stable and transparent", "Inherently unstable", "Perfectly logical", "Universally comprehensible"], "a": 1, "exp": "Directly stated: 'language is inherently unstable.'", "diff": "hard", "p": "P9"},
    {"q": "The term 'epistemological relativism' in the passage refers to:", "options": ["Absolute knowledge certainty", "Belief that knowledge is context-dependent", "Scientific objectivity", "Empirical verification"], "a": 1, "exp": "Context suggests knowledge is relative, not absolute, consistent with postmodern view.", "diff": "hard", "p": "P9"},

    # Passage 10 (Quantum Entanglement)
    {"q": "How did Einstein characterize quantum entanglement?", "options": ["Perfectly logical", "Spooky action at a distance", "Classical phenomenon", "Mathematical abstraction"], "a": 1, "exp": "Direct quote: 'described by Einstein as \"spooky action at a distance.\"'", "diff": "hard", "p": "P10"},
    {"q": "What does entanglement violate according to the passage?", "options": ["Quantum principles", "Classical locality and causality", "Mathematical consistency", "Experimental protocols"], "a": 1, "exp": "Directly stated: 'violating classical notions of locality and causality.'", "diff": "hard", "p": "P10"},
    {"q": "What has provided experimental verification?", "options": ["Einstein's equations", "Bell's theorem inequalities", "Schrödinger's cat experiment", "Heisenberg's principle"], "a": 1, "exp": "Directly stated: 'experimental verification through Bell's theorem inequalities.'", "diff": "hard", "p": "P10"},
    {"q": "Which interpretation is NOT mentioned?", "options": ["Copenhagen interpretation", "Many-worlds hypothesis", "Pilot-wave theory", "String theory interpretation"], "a": 3, "exp": "String theory is not mentioned; all others are explicitly listed.", "diff": "hard", "p": "P10"},
    {"q": "The passage suggests quantum entanglement has implications for:", "options": ["Only theoretical physics", "Reality understanding and quantum computing", "Classical mechanics only", "Biological systems primarily"], "a": 1, "exp": "Directly stated: 'profound implications for our understanding of reality, information theory, and potential quantum computing.'", "diff": "hard", "p": "P10"},

    # Passage 11 (AI Ethics)
    {"q": "What is one of the ethical concerns raised by AI mentioned in the passage?", "options": ["Lack of power source", "Bias in algorithms", "Too much sunshine", "Improvement in transportation"], "a": 1, "exp": "The passage mentions ethical concerns like 'bias in algorithms.'", "diff": "hard", "p": "P11"},
    {"q": "What does a 'lack of transparency' in AI refer to in this context?", "options": ["Machines being invisible", "The inability to see how decisions are made", "Machines without cameras", "Using too much paper"], "a": 1, "exp": "Lack of transparency in decision-making means it's unclear how AI reaches conclusions.", "diff": "hard", "p": "P11"},
    {"q": "What is suggested as necessary as AI becomes more integrated into life?", "options": ["Replacing all humans with machines", "Developing robust ethical frameworks and regulations", "Banning AI completely", "Using AI only for entertainment"], "a": 1, "exp": "The text says 'developing robust ethical frameworks and regulations is crucial.'", "diff": "hard", "p": "P11"},
    {"q": "How is AI defined in the passage?", "options": ["As a type of robot with feelings", "As the simulation of human intelligence in machines", "As a replacement for the internet", "As a method for better farming"], "a": 1, "exp": "AI is defined as 'the simulation of human intelligence in machines.'", "diff": "hard", "p": "P11"},
    {"q": "What is the intended goal of regulating AI according to the text?", "options": ["To slow down progress", "To ensure it benefits all of humanity", "To make it more expensive", "To limit its use to wealthy nations"], "a": 1, "exp": "Regulations aim to 'ensure it benefits all of humanity.'", "diff": "hard", "p": "P11"},

    # Passage 12 (Existentialism)
    {"q": "What is a central emphasis of existentialism according to the passage?", "options": ["Following established rules", "Individual freedom, choice, and responsibility", "Finding meaning in nature only", "Avoiding all difficult decisions"], "a": 1, "exp": "Existentialism emphasizes 'individual freedom, choice, and responsibility.'", "diff": "hard", "p": "P12"},
    {"q": "What do existentialists believe about the meaning of the universe?", "options": ["It has a hidden meaning waiting to be found", "It has no inherent meaning or purpose", "It is defined by scientific laws only", "It is determined by fate"], "a": 1, "exp": "Existentialists argue the universe has 'no inherent meaning or purpose.'", "diff": "hard", "p": "P12"},
    {"q": "According to the passage, how do individuals create meaning?", "options": ["By studying history", "Through their actions", "By waiting for it to arrive", "By asking others for help"], "a": 1, "exp": "Individuals must 'create their own meaning through their actions.'", "diff": "hard", "p": "P12"},
    {"q": "Which theme was explored by philosophers like Sartre and Camus?", "options": ["Logic and mathematics", "Absurdity, angst, and authenticity", "Economic theory", "Plant biology"], "a": 1, "exp": "They explored themes of 'absurdity, angst, and authenticity.'", "diff": "hard", "p": "P12"},
    {"q": "What does existentialism encourage people to do?", "options": ["Live authentically despite uncertainties", "Follow the crowd", "Ignore their responsibilities", "Seek absolute certainty"], "a": 0, "exp": "It encourages people to 'take ownership of their lives and live authentically despite the inherent uncertainties.'", "diff": "hard", "p": "P12"}
]

for q_data in questions_data:
    q = AptitudeQuestion(
        id=str(uuid.uuid4()),
        question=f"{passages[q_data['p']]}\n\n**Question:** {q_data['q']}",
        options=q_data["options"],
        correct_answer=q_data["a"],
        answer_explanation=q_data["exp"],
        topic="Reading Comprehension",
        category="Verbal Ability",
        difficulty=q_data["diff"],
        source="hardcoded",
        primary_concepts=["reading_comprehension", q_data["p"]],
        trap_explanation=None
    )
    session.add(q)

session.commit()
print(f"Successfully seeded {len(questions_data)} Reading Comprehension questions.")
session.close()
