from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services.gd_service import GDService
from typing import Optional
import os
import requests

router = APIRouter()

from services.llm_client import LLMClient

# Initialize LLM Client
llm = LLMClient()

class GDRequest(BaseModel):
    topic: str

class GDSubmitRequest(BaseModel):
    topic: str
    user_input: str
    time_taken: int

import random

# Curated list of high-quality GD topics (Business, Social, Current Affairs, Abstract)
GD_TOPICS = [
    # Business & Economy
    "Gig Economy: Future of Work or a Trend?",
    "Artificial Intelligence: Job Creator or Destroyer?",
    "Cashless Economy: Is India Ready?",
    "Work From Home: Pros and Cons",
    "Impact of 5G on Indian Economy",
    "Startups in India: Boom or Bubble?",
    "Corporate Social Responsibility: Charity or Marketing Strategy?",
    "E-commerce vs Traditional Retail",
    "Is MBA necessary for business success?",
    "Cryptocurrency: Boon or Bane?",
    "Impact of GST on Indian Economy",
    "Privatization of Public Sector Banks",
    
    # Social Issues
    "Social Media: Boon or Bane for Society?",
    "Mental Health in the Workplace",
    "Online Education vs Offline Education",
    "Women Empowerment in India: Reality vs Hype",
    "Climate Change: Individual Responsibility or Corporate?",
    "Brain Drain: Loss or Gain for India?",
    "Is Censorship of OTT Platforms Necessary?",
    "reservation system in India: Needs review?",
    "Joint Family vs Nuclear Family",
    "Impact of technology on human relationships",
    "Freebie Politics: Good or Bad for Economy?",
    "Work-Life Balance: A Myth or Reality?",
    
    # Current Affairs & Technology
    "The Future of Electric Vehicles in India",
    "One Nation, One Election: Feasibility",
    "Digital Privacy: Is Data the New Oil?",
    "Space Exploration: Necessity or Luxury? (Chandrayaan-3)",
    "G20 Summit: Takeaways for India",
    "Make in India: Success or Failure?",
    "Role of Youth in Nation Building",
    "Can India become a $5 Trillion Economy?",
    "Impact of Russia-Ukraine War on Global Economy",
    "Generative AI (ChatGPT) - Ethical Concerns",
    "Deepfakes: Threat to Democracy?",
    "Cybersecurity Challenges in Digital Era",
    
    # Abstract Topics
    "Hard Work vs Smart Work",
    "Change is the Only Constant",
    "Success is a Journey, Not a Destination",
    "Ethics vs Profit",
    "Emotional Intelligence vs IQ",
    "Freedom vs Security",
    "Knowledge is Power",
    "Failures are stepping stones to success",
    "Leader vs Boss",
    "Innovation vs Tradition",
    "Quality vs Quantity",
    "Red vs Blue: Which is better?",
    "Zero: The most powerful number"
]

@router.get("/topic")
def generate_gd_topic():
    """
    Generate a Group Discussion topic using a hybrid approach:
    - 50% chance: Select from curated high-quality list (Standard Topics)
    - 50% chance: Generate fresh topic via Groq AI (Dynamic Topics)
    Fallback to curated list if AI generation fails.
    """
    try:
        # 50% chance to use dynamic generation
        if random.random() < 0.5:
            try:
                prompt = """Generate ONE interesting, modern, and debatable Group Discussion topic for MBA/placement interviews.
                
The topic should be:
- Current and relevant (2024-2025 context)
- Debatable (has clear pro/con sides)
- Different from standard topics like "AI" or "Social Media" if possible
- Use a creative or specific angle (e.g., "Is the gig economy exploiting workers?" instead of just "Gig Economy")

Return ONLY the topic text, nothing else. No quotes."""

                topic = llm.generate_response(prompt)
                
                # Clean up
                topic = topic.replace('"', '').replace("'", "").strip()
                if len(topic) > 10: # Ensure valid topic length
                    return {"topic": topic}
            except Exception as e:
                print(f"[WARN] Dynamic topic generation failed: {e}. Falling back to curated list.")
                # Fallback to curated list logic below

        # Default / Fallback: Select from curated list
        topic = random.choice(GD_TOPICS)
        return {"topic": topic}
        
    except Exception as e:
        print(f"[ERROR] Failed to generate GD topic: {e}")
        # Ultimate fallback
        return {"topic": "Artificial Intelligence: Boon or Bane?"}


@router.post("/submit")
def submit_gd_response(request: GDSubmitRequest):
    """
    Analyze user's Group Discussion response and provide AI feedback.
    """
    user_input = request.user_input.strip() if request.user_input else ""
    if len(user_input) < 20:
        raise HTTPException(status_code=400, detail="Response too short. Please write at least 20 characters.")
    
    try:
        prompt = f"""You are an expert Group Discussion evaluator for MBA and placement interviews.

**Topic:** {request.topic}

**User's Response:**
{request.user_input}

**Time Taken:** {request.time_taken} seconds

Please analyze this response and provide:
1. **Clarity Score** (0-10): How clear and understandable is the response?
2. **Coherence Score** (0-10): How well-structured and logical is the argument?
3. **Relevance Score** (0-10): How relevant is the response to the topic?
4. **Detailed Feedback**: Constructive feedback (2-3 sentences)
5. **Strengths**: List 3 specific strengths
6. **Improvements**: List 3 areas for improvement
7. **Topic Points**: List 4-5 comprehensive study points for this topic. Each point should be a COMPLETE, DETAILED statement (2-3 sentences) that includes:
   - Key concept or fact about the topic
   - Real-world examples, case studies, or company names when relevant
   - Statistics, data, or phrases that can be used in GD
   - Present each as a well-framed, literature-style statement ready to use in discussion

Format your response EXACTLY as:
CLARITY: [score]
COHERENCE: [score]
RELEVANCE: [score]
FEEDBACK: [detailed feedback text]
STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]
IMPROVEMENTS:
- [improvement 1]
- [improvement 2]
- [improvement 3]
TOPIC_POINTS:
- [Detailed point 1 with examples and context - 2-3 sentences]
- [Detailed point 2 with examples and context - 2-3 sentences]
- [Detailed point 3 with examples and context - 2-3 sentences]
- [Detailed point 4 with examples and context - 2-3 sentences]
- [Detailed point 5 with examples and context - 2-3 sentences]
"""

        response_text = llm.generate_response(prompt)
        analysis = response_text.strip()
        
        # Parse the response
        clarity_score = 7
        coherence_score = 7
        relevance_score = 7
        feedback_text = "Your response shows good understanding of the topic."
        strengths = ["Clear expression", "Relevant points"]
        improvements = ["Add more examples", "Structure your arguments better"]
        
        # Try to extract scores
        for line in analysis.split('\n'):
            line = line.strip()
            if line.startswith('CLARITY:'):
                try:
                    clarity_score = int(line.split(':')[1].strip())
                except:
                    pass
            elif line.startswith('COHERENCE:'):
                try:
                    coherence_score = int(line.split(':')[1].strip())
                except:
                    pass
            elif line.startswith('RELEVANCE:'):
                try:
                    relevance_score = int(line.split(':')[1].strip())
                except:
                    pass
            elif line.startswith('FEEDBACK:'):
                feedback_text = line.split(':', 1)[1].strip()
        
        # Extract strengths and improvements
        if 'STRENGTHS:' in analysis:
            strengths_section = analysis.split('STRENGTHS:')[1].split('IMPROVEMENTS:')[0]
            strengths = [s.strip('- ').strip() for s in strengths_section.split('\n') if s.strip().startswith('-')]
            
        if 'IMPROVEMENTS:' in analysis:
            if 'TOPIC_POINTS:' in analysis:
                improvements_section = analysis.split('IMPROVEMENTS:')[1].split('TOPIC_POINTS:')[0]
            else:
                improvements_section = analysis.split('IMPROVEMENTS:')[1]
            improvements = [i.strip('- ').strip() for i in improvements_section.split('\n') if i.strip().startswith('-')]
        
        # Extract topic points
        topic_points = []
        if 'TOPIC_POINTS:' in analysis:
            topic_section = analysis.split('TOPIC_POINTS:')[1]
            topic_points = [t.strip('- ').strip() for t in topic_section.split('\n') if t.strip().startswith('-')]
        
        # Debug: Print the analysis to see what we got
        print(f"[DEBUG] AI Analysis Response:\n{analysis}\n")
        print(f"[DEBUG] Extracted topic_points: {topic_points}")
        
        # Ensure we always have topic points
        if not topic_points or len(topic_points) == 0:
            topic_points = [
                f"Research extensively about '{request.topic}' to understand multiple perspectives. Look for recent news articles, case studies from companies like Google, Apple, or local examples, and statistics from credible sources like World Bank or industry reports to strengthen your arguments.",
                "Identify key stakeholders involved in this topic and analyze their viewpoints. For instance, consider perspectives from government bodies, private enterprises, consumers, environmental groups, and academic experts to present a balanced discussion.",
                "Prepare concrete examples and real-world case studies relevant to this topic. Use phrases like 'For instance, when Tesla implemented...', 'A notable example is Amazon's approach to...' or 'According to a 2023 McKinsey study...' to add credibility.",
                "Understand the economic, social, environmental, and ethical dimensions of this topic. Consider questions like: What are the cost-benefit trade-offs? Who benefits and who might be disadvantaged? What are the long-term implications?",
                "Stay updated with current events and recent developments related to this topic. Reference recent policy changes, technological innovations, or market trends that demonstrate your awareness of contemporary issues and show you're well-informed."
            ]
        
        return {
            "clarity_score": clarity_score,
            "coherence_score": coherence_score,
            "relevance_score": relevance_score,
            "feedback": feedback_text,
            "strengths": strengths if strengths else ["Good effort", "Clear communication"],
            "improvements": improvements if improvements else ["Add more supporting points", "Improve structure"],
            "topic_points": topic_points
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to analyze GD response: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze response. Please try again.")


# Keep the old generate endpoint for backward compatibility
@router.post("/generate")
def generate_gd_points(request: GDRequest):
    """
    Generate For/Against points for a Group Discussion topic.
    Uses Groq or OpenAI (Stateless).
    """
    if not request.topic or len(request.topic.strip()) < 3:
        raise HTTPException(status_code=400, detail="Please enter a valid topic.")
        
    result = GDService.generate_points(request.topic)
    
    if result.get("error"):
        # We return 200 with error info so UI can display it nicely without crashing
        return {
            "status": "error",
            "message": result["message"]
        }
        
    return {
        "status": "success",
        "topic": request.topic,
        "for_points": result["for_points"],
        "against_points": result["against_points"]
    }
